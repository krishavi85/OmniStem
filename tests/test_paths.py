from pathlib import Path

import pytest

from omnistem.core.paths import safe_name, validate_input_file


def test_safe_name_removes_cross_platform_invalid_characters() -> None:
    assert safe_name("Artist: Song?/<>") == "Artist_ Song____"


def test_validate_input_file_accepts_audio(tmp_path: Path) -> None:
    audio = tmp_path / "song.wav"
    audio.write_bytes(b"RIFF")
    assert validate_input_file(audio) == audio.resolve()


def test_validate_input_file_rejects_non_audio(tmp_path: Path) -> None:
    file = tmp_path / "song.txt"
    file.write_text("x")
    with pytest.raises(ValueError):
        validate_input_file(file)
