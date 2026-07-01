from __future__ import annotations

from omnistem.engines.audio_separator import AudioSeparatorEngine
from omnistem.engines.base import SeparationEngine
from omnistem.engines.demucs import DemucsEngine
from omnistem.engines.openunmix import OpenUnmixEngine
from omnistem.engines.spleeter import SpleeterEngine


def engine_registry() -> dict[str, SeparationEngine]:
    engines: list[SeparationEngine] = [
        AudioSeparatorEngine(),
        DemucsEngine(),
        SpleeterEngine(),
        OpenUnmixEngine(),
    ]
    return {engine.engine_id: engine for engine in engines}


def get_engine(engine_id: str) -> SeparationEngine:
    try:
        return engine_registry()[engine_id]
    except KeyError as exc:
        supported = ", ".join(sorted(engine_registry()))
        raise ValueError(f"Unknown engine '{engine_id}'. Supported: {supported}") from exc
