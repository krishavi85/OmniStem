from __future__ import annotations

import shutil
import subprocess
from abc import ABC, abstractmethod
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

from omnistem.core.types import EngineStatus, SeparationJob


class SeparationEngine(ABC):
    engine_id: str
    display_name: str
    executable_candidates: tuple[str, ...]
    package_name: str | None = None
    allow_missing_executable: bool = False

    def detect_installation(self) -> EngineStatus:
        for candidate in self.executable_candidates:
            executable = shutil.which(candidate)
            if executable:
                version = self._read_version(executable)
                return EngineStatus(True, executable, version, "Ready")
        return EngineStatus(False, None, None, self.install_hint())

    def _read_version(self, executable: str) -> str | None:
        if self.package_name:
            try:
                return version(self.package_name)
            except PackageNotFoundError:
                pass
        try:
            result = subprocess.run(
                [executable, "--version"], capture_output=True, text=True, timeout=2, check=False
            )
        except (OSError, subprocess.TimeoutExpired):
            return None
        text = (result.stdout or result.stderr).strip().splitlines()
        return text[0][:160] if text else None

    @abstractmethod
    def install_hint(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def build_command(self, job: SeparationJob) -> list[str]:
        raise NotImplementedError

    def collect_outputs(self, job: SeparationJob) -> list[Path]:
        if not job.output_dir.exists():
            return []
        return sorted(
            path
            for path in job.output_dir.rglob("*")
            if path.is_file()
            and path.suffix.lower() in {".wav", ".flac", ".mp3", ".ogg", ".opus", ".aiff"}
        )

    def executable(self) -> str:
        status = self.detect_installation()
        if status.installed and status.executable:
            return status.executable
        if self.allow_missing_executable:
            return self.executable_candidates[0]
        raise RuntimeError(f"{self.display_name} is not installed. {status.message}")
