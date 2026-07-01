from __future__ import annotations

from omnistem.core.types import SeparationJob
from omnistem.engines.base import SeparationEngine


class AudioSeparatorEngine(SeparationEngine):
    engine_id = "audio-separator"
    display_name = "Audio Separator"
    executable_candidates = ("audio-separator",)
    package_name = "audio-separator"

    def install_hint(self) -> str:
        return (
            'Install CPU: pip install "audio-separator[cpu]"; '
            'GPU: pip install "audio-separator[gpu]"'
        )

    def build_command(self, job: SeparationJob) -> list[str]:
        command = [self.executable(), str(job.input_file), "--output_dir", str(job.output_dir)]
        if job.model:
            command += ["--model_filename", job.model]
        command += list(job.extra_args)
        return command
