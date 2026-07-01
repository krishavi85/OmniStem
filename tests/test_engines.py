from pathlib import Path

import pytest

from omnistem.core.types import SeparationJob
from omnistem.engines.audio_separator import AudioSeparatorEngine
from omnistem.engines.demucs import DemucsEngine
from omnistem.engines.openunmix import OpenUnmixEngine
from omnistem.engines.spleeter import SpleeterEngine


def job(**updates):
    values = dict(
        input_file=Path("song.wav"),
        output_dir=Path("outputs"),
        engine="demucs",
        model=None,
        stems=("vocals", "instrumental"),
        device="auto",
        output_format="wav",
    )
    values.update(updates)
    return SeparationJob(**values)


def test_audio_separator_command(monkeypatch: pytest.MonkeyPatch) -> None:
    engine = AudioSeparatorEngine()
    monkeypatch.setattr(engine, "executable", lambda: "audio-separator")
    command = engine.build_command(job(engine="audio-separator", model="model.ckpt"))
    assert command == [
        "audio-separator",
        "song.wav",
        "--output_dir",
        "outputs",
        "--model_filename",
        "model.ckpt",
    ]


def test_demucs_two_stem_command(monkeypatch: pytest.MonkeyPatch) -> None:
    engine = DemucsEngine()
    monkeypatch.setattr(engine, "executable", lambda: "demucs")
    command = engine.build_command(job(model="htdemucs_ft", device="cuda"))
    assert command == [
        "demucs",
        "--out",
        "outputs",
        "--name",
        "htdemucs_ft",
        "--device",
        "cuda",
        "--two-stems",
        "vocals",
        "song.wav",
    ]


def test_spleeter_rejects_unsupported_stem_count(monkeypatch: pytest.MonkeyPatch) -> None:
    engine = SpleeterEngine()
    monkeypatch.setattr(engine, "executable", lambda: "spleeter")
    with pytest.raises(ValueError):
        engine.build_command(job(engine="spleeter", stems=("a", "b", "c")))


def test_openunmix_vocal_residual_command(monkeypatch: pytest.MonkeyPatch) -> None:
    engine = OpenUnmixEngine()
    monkeypatch.setattr(engine, "executable", lambda: "umx")
    command = engine.build_command(job(engine="openunmix", model="umxhq"))
    assert command == [
        "umx",
        "song.wav",
        "--outdir",
        "outputs",
        "--model",
        "umxhq",
        "--targets",
        "vocals",
        "--residual",
    ]
