from pathlib import Path

from omnistem.core.history import JobHistory


def test_history_upsert_and_list(tmp_path: Path) -> None:
    history = JobHistory(tmp_path / "jobs.sqlite3")
    record = {
        "job_id": "abc",
        "status": "processing",
        "engine": "demucs",
        "model": "htdemucs_ft",
        "input_file": "/tmp/song.wav",
        "output_dir": "/tmp/output",
        "command": ["demucs", "song.wav"],
    }
    history.upsert(record)
    record["status"] = "completed"
    record["manifest_path"] = "/tmp/output/job-manifest.json"
    history.upsert(record)
    rows = history.list()
    assert len(rows) == 1
    assert rows[0]["status"] == "completed"
    assert rows[0]["manifest_path"].endswith("job-manifest.json")
