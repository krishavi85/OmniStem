import json
from pathlib import Path

from omnistem.core.manifest import write_manifest


def test_manifest_contains_runtime_metadata(tmp_path: Path) -> None:
    path = write_manifest(tmp_path / "manifest.json", {"job": {"id": "abc"}})
    data = json.loads(path.read_text())
    assert data["job"]["id"] == "abc"
    assert data["omnistem_version"]
    assert data["created_at"]
