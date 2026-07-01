from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Any

try:
    from fastapi import BackgroundTasks, FastAPI, HTTPException
    from pydantic import BaseModel
except ImportError as exc:  # pragma: no cover
    raise RuntimeError('Install API support with: pip install "omnistem[api]"') from exc

from omnistem import __version__
from omnistem.core.history import JobHistory
from omnistem.core.model_registry import list_models
from omnistem.core.orchestrator import Orchestrator
from omnistem.core.types import SeparationJob
from omnistem.engines.registry import engine_registry

app = FastAPI(title="OmniStem God Mode API", version=__version__)


class JobRequest(BaseModel):
    input_file: str
    output_dir: str = "outputs"
    engine: str = "audio-separator"
    model: str | None = None
    stems: list[str] = ["vocals", "instrumental"]
    device: str = "auto"
    output_format: str = "wav"


async def _execute(job: SeparationJob) -> None:
    await Orchestrator().run(job)


@app.get("/health")
def health() -> dict[str, Any]:
    return {"status": "ok", "version": __version__}


@app.get("/engines")
def engines() -> list[dict[str, Any]]:
    return [
        {
            "id": engine_id,
            "name": engine.display_name,
            "status": engine.detect_installation().__dict__,
            "install_hint": engine.install_hint(),
        }
        for engine_id, engine in engine_registry().items()
    ]


@app.get("/models")
def models(engine: str | None = None, query: str | None = None) -> list[dict[str, Any]]:
    return [model.__dict__ for model in list_models(engine, query)]


@app.post("/jobs", status_code=202)
def create_job(request: JobRequest, background_tasks: BackgroundTasks) -> dict[str, Any]:
    job = SeparationJob(
        input_file=Path(request.input_file),
        output_dir=Path(request.output_dir),
        engine=request.engine,
        model=request.model,
        stems=tuple(request.stems),
        device=request.device,
        output_format=request.output_format,
    )
    try:
        prepared, command = Orchestrator().prepare(job)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    background_tasks.add_task(asyncio.run, _execute(prepared))
    return {"job_id": prepared.job_id, "command": command, "status": "accepted"}


@app.get("/jobs")
def jobs(limit: int = 50) -> list[dict[str, Any]]:
    return JobHistory().list(limit)
