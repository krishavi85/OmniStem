from __future__ import annotations

from omnistem.core.types import SeparationJob
from omnistem.engines.base import SeparationEngine


class OpenUnmixEngine(SeparationEngine):
    engine_id = "openunmix"
    display_name = "Open-Unmix"
    executable_candidates = ("umx",)
    package_name = "openunmix"
    supported_input_extensions = frozenset({".wav", ".flac", ".ogg"})
    supported_output_formats = frozenset({"wav", "flac", "ogg"})
    native_targets = frozenset({"vocals", "drums", "bass", "other"})

    def install_hint(self) -> str:
        return "Install with: pip install 'openunmix>=1.3,<2'"

    def validate_job(self, job: SeparationJob) -> None:
        super().validate_job(job)
        if job.device not in {"auto", "cpu", "cuda"}:
            raise ValueError("Open-Unmix supports --device auto, cpu, or cuda.")
        requested = set(job.stems)
        if requested == {"vocals", "instrumental"}:
            return
        unsupported = requested - self.native_targets
        if unsupported:
            names = ", ".join(sorted(unsupported))
            raise ValueError(f"Open-Unmix does not expose these native targets: {names}")

    def build_command(self, job: SeparationJob) -> list[str]:
        command = [
            *self.command_prefix(),
            str(job.input_file),
            "--outdir",
            str(job.output_dir),
            "--ext",
            f".{job.output_format.lstrip('.')}",
        ]
        if job.model:
            command += ["--model", job.model]
        if job.device == "cpu":
            command.append("--no-cuda")
        if set(job.stems) == {"vocals", "instrumental"}:
            command += ["--targets", "vocals", "--residual", "instrumental"]
        elif job.stems:
            command += ["--targets", *job.stems]
        command += list(job.extra_args)
        return command
