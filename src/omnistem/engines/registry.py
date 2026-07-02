from __future__ import annotations

from omnistem.core.types import SeparationJob
from omnistem.engines.audio_separator import AudioSeparatorEngine
from omnistem.engines.base import SeparationEngine
from omnistem.engines.demucs import DemucsEngine
from omnistem.engines.openunmix import OpenUnmixEngine
from omnistem.engines.spleeter import SpleeterEngine


class CompatibleSpleeterEngine(SpleeterEngine):
    module_name = "spleeter"
    supported_output_formats = frozenset({"wav", "mp3", "ogg", "m4a", "wma", "flac"})

    def build_command(self, job: SeparationJob) -> list[str]:
        count = len(job.stems) if job.stems else 2
        preset = job.model or f"spleeter:{count}stems"
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


def engine_registry() -> dict[str, SeparationEngine]:
    engines: list[SeparationEngine] = [
        AudioSeparatorEngine(),
        DemucsEngine(),
        CompatibleSpleeterEngine(),
        OpenUnmixEngine(),
    ]
    return {engine.engine_id: engine for engine in engines}


def get_engine(engine_id: str) -> SeparationEngine:
    try:
        return engine_registry()[engine_id]
    except KeyError as exc:
        supported = ", ".join(sorted(engine_registry()))
        raise ValueError(f"Unknown engine '{engine_id}'. Supported: {supported}") from exc
