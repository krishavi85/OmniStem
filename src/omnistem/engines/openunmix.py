from __future__ import annotations

from omnistem.core.types import SeparationJob
from omnistem.engines.base import SeparationEngine


class OpenUnmixEngine(SeparationEngine):
    engine_id = "openunmix"
    display_name = "Open-Unmix"
    executable_candidates = ("umx",)
    package_name = "openunmix"

    def install_hint(self) -> str:
        return "Install with: pip install openunmix"

    def build_command(self, job: SeparationJob) -> list[str]:
        command = [self.executable(), str(job.input_file), "--outdir", str(job.output_dir)]
        if job.model:
            command += ["--model", job.model]
        if job.stems:
            command += ["--targets", *job.stems]
            if set(job.stems) == {"vocals", "instrumental"}:
                command = [self.executable(), str(job.input_file), "--outdir", str(job.output_dir)]
                if job.model:
                    command += ["--model", job.model]
                command += ["--targets", "vocals", "--residual"]
        command += list(job.extra_args)
        return command
