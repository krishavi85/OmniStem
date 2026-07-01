from pathlib import Path

import pytest

from omnistem.core.history import JobHistory
from omnistem.core.orchestrator import Orchestrator
from omnistem.core.types import SeparationJob
from omnistem.engines.demucs import DemucsEngine


def test_prepare_validates_and_builds_command(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    audio = tmp_path / "song.wav"
    audio.write_bytes(b"RIFF")
    output = tmp_path / "outputs"
    monkeypatch.setattr(DemucsEngine, "executable", lambda self: "demucs")
    orchestrator = Orchestrator(JobHistory(tmp_path / "jobs.sqlite3"))
    prepared, command = orchestrator.prepare(
        SeparationJob(
            input_file=audio,
            output_dir=output,
            engine="demucs",
            model="htdemucs_ft",
            stems=("vocals", "drums", "bass", "other"),
        )
    )
    assert prepared.job_id
    assert prepared.input_file == audio.resolve()
    assert command[-1] == str(audio.resolve())
    assert output.exists()
