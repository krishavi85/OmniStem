from __future__ import annotations

from omnistem.core.types import SeparationJob
from omnistem.engines.base import SeparationEngine


class SpleeterEngine(SeparationEngine):
    engine_id = "spleeter"
    display_name = "Spleeter"
    executable_candidates = ("spleeter",)
    package_name = "spleeter"

    def install_hint(self) -> str:
        return "Install with: pip install spleeter"

    def build_command(self, job: SeparationJob) -> list[str]:
        stem_count = len(job.stems) if job.stems else 2
        if stem_count not in {2, 4, 5}:
            raise ValueError("Spleeter supports 2, 4, or 5-stem presets")
        preset = job.model or f"spleeter:{stem_count}stems"
        command = [
            self.executable(),
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
        return command
