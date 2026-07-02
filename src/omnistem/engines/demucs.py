from __future__ import annotations

from omnistem.core.types import SeparationJob
from omnistem.engines.base import SeparationEngine


class DemucsEngine(SeparationEngine):
    engine_id = "demucs"
    display_name = "Demucs"
    executable_candidates = ("demucs",)
    package_name = "demucs"
    module_name = "demucs"
    supported_output_formats = frozenset({"wav", "flac", "mp3"})

    def install_hint(self) -> str:
        return "Install with: pip install -U demucs"

    def validate_job(self, job: SeparationJob) -> None:
        super().validate_job(job)
        requested = set(job.stems)
        if not requested:
            return
        if "instrumental" in requested and len(requested) == 2:
            target = next(iter(requested - {"instrumental"}))
            if target not in {"vocals", "drums", "bass", "other", "guitar", "piano"}:
                raise ValueError(f"Demucs cannot create a two-stem split for '{target}'.")
            return
        expected = (
            {"vocals", "drums", "bass", "guitar", "piano", "other"}
            if job.model == "htdemucs_6s"
            else {"vocals", "drums", "bass", "other"}
        )
        if requested != expected:
            raise ValueError(
                "Demucs requires all selected-model stems or one target plus instrumental."
            )

    def build_command(self, job: SeparationJob) -> list[str]:
        command = [*self.command_prefix(), "--out", str(job.output_dir)]
        if job.model:
            command.extend(["--name", job.model])
        if job.device != "auto":
            command.extend(["--device", job.device])
        requested = set(job.stems)
        if "instrumental" in requested and len(requested) == 2:
            command.extend(["--two-stems", next(iter(requested - {"instrumental"}))])
        if job.output_format == "flac":
            command.append("--flac")
        elif job.output_format == "mp3":
            command.append("--mp3")
        command.extend(job.extra_args)
        command.append(str(job.input_file))
        return command
