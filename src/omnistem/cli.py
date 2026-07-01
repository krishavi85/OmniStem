from __future__ import annotations

import asyncio
import json
import os
import platform
import shutil
import sys
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table
from rich.text import Text

from omnistem import __version__
from omnistem.audio.ffmpeg import ffmpeg_status, probe_audio
from omnistem.core.history import JobHistory
from omnistem.core.model_registry import list_models
from omnistem.core.orchestrator import Orchestrator
from omnistem.core.types import SeparationJob
from omnistem.engines.registry import engine_registry
from omnistem.ensembles.waveform import weighted_waveform_average

app = typer.Typer(
    help="OmniStem God Mode: one CLI for local music stem separation engines.",
    invoke_without_command=True,
)
engines_app = typer.Typer(help="Inspect supported separation engines.")
models_app = typer.Typer(help="Inspect verified model metadata.")
history_app = typer.Typer(help="Inspect persistent job history.")
app.add_typer(engines_app, name="engines")
app.add_typer(models_app, name="models")
app.add_typer(history_app, name="history")
console = Console()


def _emit(payload: object, as_json: bool) -> None:
    if as_json:
        console.print_json(json.dumps(payload, default=str))
    else:
        console.print(payload)


def _version_callback(value: bool) -> None:
    if value:
        console.print(f"omnistem {__version__}")
        raise typer.Exit()


@app.callback()
def root(
    ctx: typer.Context,
    version: Annotated[
        bool,
        typer.Option(
            "--version", help="Show version and exit.", callback=_version_callback, is_eager=True
        ),
    ] = False,
) -> None:
    if ctx.invoked_subcommand is None and not version:
        console.print(ctx.get_help())


@app.command()
def env(json_output: Annotated[bool, typer.Option("--json")] = False) -> None:
    """Show operating system, Python, FFmpeg and accelerator hints."""
    payload = {
        "omnistem": __version__,
        "python": sys.version,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "cpu_count": os.cpu_count(),
        "ffmpeg": ffmpeg_status(),
        "nvidia_smi": shutil.which("nvidia-smi"),
    }
    _emit(payload, json_output)


@app.command()
def doctor(json_output: Annotated[bool, typer.Option("--json")] = False) -> None:
    """Diagnose the local OmniStem runtime."""
    ffmpeg = ffmpeg_status()
    engines = {}
    installed_engine_count = 0
    for engine_id, engine in engine_registry().items():
        status = engine.detect_installation()
        engines[engine_id] = {
            "installed": status.installed,
            "executable": status.executable,
            "version": status.version,
            "message": status.message,
        }
        installed_engine_count += int(status.installed)
    healthy = bool(ffmpeg["installed"] and installed_engine_count > 0)
    payload = {
        "healthy": healthy,
        "ready_to_separate": installed_engine_count > 0,
        "installed_engine_count": installed_engine_count,
        "ffmpeg": ffmpeg,
        "engines": engines,
    }
    _emit(payload, json_output)
    if not healthy:
        raise typer.Exit(code=1)


@engines_app.command("list")
def engines_list(json_output: Annotated[bool, typer.Option("--json")] = False) -> None:
    rows = []
    for engine_id, engine in engine_registry().items():
        status = engine.detect_installation()
        rows.append(
            {
                "id": engine_id,
                "name": engine.display_name,
                "installed": status.installed,
                "executable": status.executable,
                "version": status.version,
                "install_hint": engine.install_hint(),
            }
        )
    if json_output:
        _emit(rows, True)
        return
    table = Table(title="OmniStem engines")
    table.add_column("Engine")
    table.add_column("Installed")
    table.add_column("Executable / action")
    for row in rows:
        table.add_row(
            str(row["id"]),
            "yes" if bool(row["installed"]) else "no",
            Text(str(row["executable"] or row["install_hint"])),
        )
    console.print(table)


@models_app.command("list")
def models_list(
    engine: Annotated[str | None, typer.Option(help="Filter by engine.")] = None,
    query: Annotated[str | None, typer.Option(help="Search ID, name, or stem.")] = None,
    json_output: Annotated[bool, typer.Option("--json")] = False,
) -> None:
    rows = [model.__dict__ for model in list_models(engine, query)]
    if json_output:
        _emit(rows, True)
        return
    table = Table(title="Verified model registry")
    for column in ("ID", "Engine", "Architecture", "Stems", "License note"):
        table.add_column(column)
    for model in list_models(engine, query):
        table.add_row(
            model.id,
            model.engine,
            model.architecture,
            ", ".join(model.supported_stems),
            model.license,
        )
    console.print(table)


@app.command()
def inspect(
    input_file: Annotated[Path, typer.Argument(exists=True, dir_okay=False)],
    json_output: Annotated[bool, typer.Option("--json")] = False,
) -> None:
    """Inspect an audio file through ffprobe."""
    _emit(probe_audio(input_file), json_output)


@app.command()
def separate(
    input_file: Annotated[Path, typer.Argument(exists=True, dir_okay=False)],
    engine: Annotated[
        str, typer.Option(help="audio-separator, demucs, spleeter, or openunmix")
    ] = "audio-separator",
    model: Annotated[
        str | None, typer.Option(help="Native upstream model name or filename.")
    ] = None,
    stems: Annotated[
        str, typer.Option(help="Comma-separated normalized stems.")
    ] = "vocals,instrumental",
    output: Annotated[Path, typer.Option(help="Output directory.")] = Path("outputs"),
    device: Annotated[
        str, typer.Option(help="auto, cpu, cuda, or an engine-supported device.")
    ] = "auto",
    output_format: Annotated[
        str, typer.Option("--format", help="wav, flac, or mp3 where supported.")
    ] = "wav",
    extra_arg: Annotated[
        list[str] | None,
        typer.Option("--extra-arg", help="Repeat for verified native engine flags."),
    ] = None,
    dry_run: Annotated[bool, typer.Option("--dry-run")] = False,
    json_output: Annotated[bool, typer.Option("--json")] = False,
) -> None:
    """Run one real upstream stem-separation engine."""
    job = SeparationJob(
        input_file=input_file,
        output_dir=output,
        engine=engine,
        model=model,
        stems=tuple(part.strip() for part in stems.split(",") if part.strip()),
        device=device,
        output_format=output_format,
        extra_args=tuple(extra_arg or ()),
    )
    orchestrator = Orchestrator()
    try:
        prepared, command = orchestrator.prepare(job, allow_missing_engine=dry_run)
    except Exception as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=2) from exc
    if dry_run:
        _emit({"job": prepared.to_dict(), "command": command}, json_output)
        return

    def progress(line: str) -> None:
        if not json_output:
            console.print(line)

    result = asyncio.run(orchestrator.run(prepared, on_line=progress))
    payload = {
        "ok": result.ok,
        "job_id": result.job_id,
        "return_code": result.return_code,
        "outputs": [str(path) for path in result.output_files],
        "manifest": str(result.manifest_path),
    }
    _emit(payload, json_output)
    if not result.ok:
        if result.stderr:
            console.print(f"[red]{result.stderr}[/red]")
        raise typer.Exit(code=result.return_code or 1)


@app.command()
def batch(
    folder: Annotated[Path, typer.Argument(exists=True, file_okay=False)],
    engine: Annotated[str, typer.Option()] = "audio-separator",
    model: Annotated[str | None, typer.Option()] = None,
    stems: Annotated[str, typer.Option()] = "vocals,instrumental",
    output: Annotated[Path, typer.Option()] = Path("outputs"),
    recursive: Annotated[bool, typer.Option("--recursive/--no-recursive")] = True,
    dry_run: Annotated[bool, typer.Option("--dry-run")] = False,
) -> None:
    """Process every supported audio file in a folder sequentially."""
    pattern = "**/*" if recursive else "*"
    extensions = {
        ".wav",
        ".flac",
        ".aiff",
        ".aif",
        ".mp3",
        ".aac",
        ".m4a",
        ".ogg",
        ".opus",
        ".wma",
        ".alac",
        ".caf",
    }
    files = sorted(
        path
        for path in folder.glob(pattern)
        if path.is_file() and path.suffix.lower() in extensions
    )
    if not files:
        console.print("[yellow]No supported audio files found.[/yellow]")
        raise typer.Exit(code=1)
    failures = 0
    for path in files:
        target = output / path.stem
        console.rule(path.name)
        job = SeparationJob(path, target, engine, model, tuple(stems.split(",")))
        orchestrator = Orchestrator()
        if dry_run:
            _, command = orchestrator.prepare(job, allow_missing_engine=True)
            console.print(command)
            continue
        result = asyncio.run(orchestrator.run(job, on_line=console.print))
        failures += int(not result.ok)
    if failures:
        raise typer.Exit(code=1)


@app.command()
def ensemble(
    inputs: Annotated[list[Path], typer.Argument(exists=True, dir_okay=False)],
    output: Annotated[Path, typer.Option(help="Output 32-bit float WAV.")],
    weights: Annotated[str | None, typer.Option(help="Comma-separated weights.")] = None,
) -> None:
    """Create a validated weighted waveform ensemble from aligned stems."""
    parsed = [float(value) for value in weights.split(",")] if weights else None
    result = weighted_waveform_average(inputs, output, parsed)
    console.print(f"Created {result}")


@history_app.command("list")
def history_list(
    limit: Annotated[int, typer.Option(min=1, max=1000)] = 50,
    json_output: Annotated[bool, typer.Option("--json")] = False,
) -> None:
    rows = JobHistory().list(limit)
    if json_output:
        _emit(rows, True)
        return
    table = Table(title="OmniStem job history")
    for column in ("Job", "Status", "Engine", "Input", "Updated"):
        table.add_column(column)
    for row in rows:
        table.add_row(
            row["job_id"], row["status"], row["engine"], row["input_file"], row["updated_at"]
        )
    console.print(table)


@app.command()
def serve(
    host: Annotated[str, typer.Option()] = "127.0.0.1",
    port: Annotated[int, typer.Option(min=1, max=65535)] = 8765,
) -> None:
    """Start the optional local FastAPI server."""
    try:
        import uvicorn
    except ImportError as exc:
        raise RuntimeError('Install API support with: pip install "omnistem[api]"') from exc
    uvicorn.run("omnistem.api.app:app", host=host, port=port, reload=False)


@app.command()
def desktop() -> None:
    """Launch the optional PySide6 desktop application."""
    from omnistem.desktop.app import main

    main()
