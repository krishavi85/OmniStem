from __future__ import annotations

from omnistem.core.types import SeparationJob
from omnistem.engines.base import SeparationEngine


class DemucsEngine(SeparationEngine):
    engine_id = "demucs"
    display_name = "Demucs"
    executable_candidates = ("demucs",)
    package_name = "demucs"

    def install_hint(self) -> str:
        return "Install with: pip install -U demucs"

    def build_command(self, job: SeparationJob) -> list[str]:
        command = [self.executable(), "--out", str(job.output_dir)]
        if job.model:
            command += ["--name", job.model]
        if job.device != "auto":
            command += ["--device", job.device]
        if set(job.stems) == {"vocals", "instrumental"}:
            command += ["--two-stems", "vocals"]
        if job.output_format == "flac":
            command.append("--flac")
        elif job.output_format == "mp3":
            command.append("--mp3")
        command += list(job.extra_args)
        command.append(str(job.input_file))
        return command
