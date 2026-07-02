from __future__ import annotations

from omnistem.core.types import SeparationJob
from omnistem.engines.base import SeparationEngine


class SpleeterEngine(SeparationEngine):
    engine_id = "spleeter"
    display_name = "Spleeter"
    executable_candidates = ("spleeter",)
    package_name = "spleeter"
    module_name = "spleeter"
    supported_output_formats = frozenset({"wav", "mp3", "ogg", "m4a", "wma", "flac"})

    def install_hint(self) -> str:
        return "Install Spleeter in a compatible Python environment."

    def validate_job(self, job: SeparationJob) -> None:
        super().validate_job(job)
        if len(job.stems) not in {2, 4, 5}:
            raise ValueError("Spleeter supports 2, 4, or 5-stem presets")

    def build_command(self, job: SeparationJob) -> list[str]:
        stem_count = len(job.stems) if job.stems else 2
        preset = job.model or f"spleeter:{stem_count}stems"
        return [
            *self.command_prefix(),
            "separate",
            "-p",
            preset,
            "-o",
            str(job.output_dir),
            "-c",
            job.output_format,
            *job.extra_args,
            str(job.input_file),
        ]
