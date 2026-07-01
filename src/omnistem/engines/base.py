from __future__ import annotations

import shutil
import subprocess
import sys
from abc import ABC, abstractmethod
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

from omnistem.core.types import EngineStatus, SeparationJob


class SeparationEngine(ABC):
    engine_id: str
    display_name: str
    executable_candidates: tuple[str, ...]
    package_name: str | None = None
    module_name: str | None = None
    supported_input_extensions: frozenset[str] | None = None
    supported_output_formats: frozenset[str] | None = None
    allow_missing_executable: bool = False

    def detect_installation(self) -> EngineStatus:
        package_version = self._package_version()
        for candidate in self.executable_candidates:
            executable = shutil.which(candidate)
            if executable:
                detected_version = package_version or self._read_executable_version(executable)
                return EngineStatus(True, executable, detected_version, "Ready")
        if package_version and self.module_name:
            command = f"{sys.executable} -m {self.module_name}"
            return EngineStatus(True, command, package_version, "Ready through Python module")
        return EngineStatus(False, None, package_version, self.install_hint())

    def _package_version(self) -> str | None:
        if not self.package_name:
            return None
        try:
            return version(self.package_name)
        except PackageNotFoundError:
            return None

    @staticmethod
    def _read_executable_version(executable: str) -> str | None:
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

    def validate_job(self, job: SeparationJob) -> None:
        if self.supported_input_extensions is not None:
            extension = job.input_file.suffix.lower()
            if extension not in self.supported_input_extensions:
                supported = ", ".join(sorted(self.supported_input_extensions))
                raise ValueError(
                    f"{self.display_name} does not accept '{extension}' input. "
                    f"Supported: {supported}"
                )
        if self.supported_output_formats is not None:
            output_format = job.output_format.lower().lstrip(".")
            if output_format not in self.supported_output_formats:
                supported = ", ".join(sorted(self.supported_output_formats))
                raise ValueError(
                    f"{self.display_name} cannot export '{job.output_format}'. "
                    f"Supported: {supported}"
                )

    @abstractmethod
    def build_command(self, job: SeparationJob) -> list[str]:
        raise NotImplementedError

    def collect_outputs(self, job: SeparationJob) -> list[Path]:
        if not job.output_dir.exists():
            return []
        input_path = job.input_file.resolve()
        return sorted(
            path
            for path in job.output_dir.rglob("*")
            if path.is_file()
            and path.resolve() != input_path
            and path.suffix.lower()
            in {
                ".wav",
                ".flac",
                ".mp3",
                ".ogg",
                ".opus",
                ".aiff",
                ".aif",
                ".m4a",
                ".aac",
                ".wma",
                ".caf",
            }
        )

    def command_prefix(self) -> list[str]:
        for candidate in self.executable_candidates:
            executable = shutil.which(candidate)
            if executable:
                return [executable]
        if self._package_version() and self.module_name:
            return [sys.executable, "-m", self.module_name]
        if self.allow_missing_executable:
            return [self.executable_candidates[0]]
        raise RuntimeError(f"{self.display_name} is not installed. {self.install_hint()}")
