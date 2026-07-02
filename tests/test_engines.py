from pathlib import Path

import pytest

from omnistem.core.types import SeparationJob
from omnistem.engines.audio_separator import AudioSeparatorEngine
from omnistem.engines.demucs import DemucsEngine
from omnistem.engines.openunmix import OpenUnmixEngine
from omnistem.engines.registry import CompatibleSpleeterEngine


def job(**updates):
    values = {
        "input_file": Path("song.wav"),
        "output_dir": Path("outputs"),
        "engine": "demucs",
        "model": None,
        "stems": ("vocals", "instrumental"),
        "device": "auto",
        "output_format": "wav",
    }
    values.update(updates)
    return SeparationJob(**values)


def test_audio_separator_command(monkeypatch: pytest.MonkeyPatch) -> None:
    engine = AudioSeparatorEngine()
    monkeypatch.setattr(engine, "command_prefix", lambda: ["audio-separator"])
    command = engine.build_command(job(engine="audio-separator", model="model.ckpt"))
    assert command == [
        "audio-separator",
        "song.wav",
        "--output_dir",
        "outputs",
        "--output_format",
        "WAV",
        "--model_filename",
        "model.ckpt",
    ]


def test_demucs_two_stem_command(monkeypatch: pytest.MonkeyPatch) -> None:
    engine = DemucsEngine()
    monkeypatch.setattr(engine, "command_prefix", lambda: ["demucs"])
    command = engine.build_command(job(model="htdemucs_ft", device="cuda"))
    assert command[-3:] == ["--two-stems", "vocals", "song.wav"]


def test_openunmix_residual_command(monkeypatch: pytest.MonkeyPatch) -> None:
    engine = OpenUnmixEngine()
    monkeypatch.setattr(engine, "command_prefix", lambda: ["umx"])
    command = engine.build_command(job(engine="openunmix", model="umxhq", device="cpu"))
    assert ["--residual", "instrumental"] == command[-2:]
    assert "--no-cuda" in command
    assert command[command.index("--ext") + 1] == ".wav"


def test_openunmix_rejects_mp3_input() -> None:
    engine = OpenUnmixEngine()
    with pytest.raises(ValueError, match="does not accept"):
        engine.validate_job(job(engine="openunmix", input_file=Path("song.mp3")))


def test_spleeter_wrapper_uses_command_prefix(monkeypatch: pytest.MonkeyPatch) -> None:
    engine = CompatibleSpleeterEngine()
    monkeypatch.setattr(engine, "command_prefix", lambda: ["spleeter"])
    command = engine.build_command(job(engine="spleeter"))
    assert command[:4] == ["spleeter", "separate", "-p", "spleeter:2stems"]
