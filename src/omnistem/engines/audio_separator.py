from __future__ import annotations

from omnistem.core.types import SeparationJob
from omnistem.engines.base import SeparationEngine


class AudioSeparatorEngine(SeparationEngine):
    engine_id = "audio-separator"
    display_name = "Audio Separator"
    executable_candidates = ("audio-separator",)
    package_name = "audio-separator"
    supported_output_formats = frozenset(
        {"wav", "flac", "mp3", "ogg", "opus", "m4a", "aac", "wma", "aiff", "aif", "caf"}
    )

    def install_hint(self) -> str:
        return 'Install with: pip install "audio-separator[cpu]"'

    def validate_job(self, job: SeparationJob) -> None:
        super().validate_job(job)
        if job.device != "auto":
            raise ValueError("Audio Separator requires --device auto in OmniStem.")

    def build_command(self, job: SeparationJob) -> list[str]:
        command = [
            *self.command_prefix(),
            str(job.input_file),
            "--output_dir",
            str(job.output_dir),
            "--output_format",
            job.output_format.upper(),
        ]
        if job.model:
            command.extend(["--model_filename", job.model])
        if len(job.stems) == 1:
            command.extend(["--single_stem", job.stems[0].replace("_", " ").title()])
        command.extend(job.extra_args)
        return command
