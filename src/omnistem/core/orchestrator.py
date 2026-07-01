from __future__ import annotations

import uuid
from collections.abc import Callable

from omnistem.core.history import JobHistory
from omnistem.core.manifest import write_manifest
from omnistem.core.paths import prepare_output_dir, validate_input_file
from omnistem.core.subprocess_runner import ProcessOutput, run_command
from omnistem.core.types import JobStatus, SeparationJob, SeparationResult
from omnistem.engines.registry import get_engine


class Orchestrator:
    def __init__(self, history: JobHistory | None = None) -> None:
        self.history = history or JobHistory()

    def prepare(
        self,
        job: SeparationJob,
        *,
        allow_missing_engine: bool = False,
        create_output_dir: bool = True,
    ) -> tuple[SeparationJob, list[str]]:
        job.input_file = validate_input_file(job.input_file)
        job.output_format = job.output_format.lower().lstrip(".")
        job.output_dir = prepare_output_dir(
            job.output_dir, create=create_output_dir, overwrite=job.overwrite
        )
        job.job_id = job.job_id or uuid.uuid4().hex
        engine = get_engine(job.engine)
        engine.validate_job(job)
        engine.allow_missing_executable = allow_missing_engine
        try:
            command = engine.build_command(job)
        finally:
            engine.allow_missing_executable = False
        return job, command

    async def run(
        self, job: SeparationJob, on_line: Callable[[str], None] | None = None
    ) -> SeparationResult:
        job, command = self.prepare(job)
        record = {
            "job_id": job.job_id,
            "status": JobStatus.PROCESSING.value,
            "engine": job.engine,
            "model": job.model,
            "input_file": str(job.input_file),
            "output_dir": str(job.output_dir),
            "command": command,
        }
        self.history.upsert(record)
        engine = get_engine(job.engine)
        before = {path.resolve(): path.stat().st_mtime_ns for path in engine.collect_outputs(job)}
        try:
            output = await run_command(command, on_line=on_line)
        except Exception as exc:
            output = ProcessOutput(127, "", f"{type(exc).__name__}: {exc}")
        discovered = engine.collect_outputs(job)
        artifacts = [
            path
            for path in discovered
            if path.resolve() not in before
            or path.stat().st_mtime_ns != before[path.resolve()]
        ]
        if output.return_code == 0 and not artifacts:
            message = "Engine exited successfully but produced no new audio artifacts."
            stderr = f"{output.stderr}\n{message}".strip()
            output = ProcessOutput(1, output.stdout, stderr)
        manifest = write_manifest(
            job.output_dir / "job-manifest.json",
            {
                "job": job.to_dict(),
                "command": command,
                "return_code": output.return_code,
                "artifacts": [str(path) for path in artifacts],
                "stdout": output.stdout,
                "stderr": output.stderr,
            },
        )
        status = JobStatus.COMPLETED if output.return_code == 0 else JobStatus.FAILED
        record.update(
            status=status.value,
            manifest_path=str(manifest),
            error=None if output.return_code == 0 else output.stderr[-4000:],
        )
        self.history.upsert(record)
        return SeparationResult(
            job_id=job.job_id,
            command=tuple(command),
            return_code=output.return_code,
            output_files=tuple(artifacts),
            stdout=output.stdout,
            stderr=output.stderr,
            manifest_path=manifest,
        )
