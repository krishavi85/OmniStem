from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any


class JobStatus(str, Enum):
    QUEUED = "queued"
    VALIDATING = "validating"
    PROCESSING = "processing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    FAILED = "failed"


@dataclass(frozen=True)
class EngineStatus:
    installed: bool
    executable: str | None
    version: str | None = None
    message: str = ""


@dataclass(frozen=True)
class ModelDescriptor:
    id: str
    display_name: str
    engine: str
    architecture: str
    supported_stems: tuple[str, ...]
    license: str
    repository_url: str
    notes: str = ""


@dataclass
class SeparationJob:
    input_file: Path
    output_dir: Path
    engine: str
    model: str | None = None
    stems: tuple[str, ...] = field(default_factory=tuple)
    device: str = "auto"
    output_format: str = "wav"
    overwrite: bool = False
    extra_args: tuple[str, ...] = field(default_factory=tuple)
    job_id: str = ""

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["input_file"] = str(self.input_file)
        data["output_dir"] = str(self.output_dir)
        return data


@dataclass(frozen=True)
class SeparationResult:
    job_id: str
    command: tuple[str, ...]
    return_code: int
    output_files: tuple[Path, ...]
    stdout: str
    stderr: str
    manifest_path: Path

    @property
    def ok(self) -> bool:
        return self.return_code == 0
