from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path
from typing import Any, cast


def ffmpeg_status() -> dict[str, str | bool | None]:
    ffmpeg = shutil.which("ffmpeg")
    ffprobe = shutil.which("ffprobe")
    return {"installed": bool(ffmpeg and ffprobe), "ffmpeg": ffmpeg, "ffprobe": ffprobe}


def probe_audio(path: Path) -> dict[str, Any]:
    ffprobe = shutil.which("ffprobe")
    if not ffprobe:
        raise RuntimeError("ffprobe was not found. Install FFmpeg and ensure it is on PATH.")
    result = subprocess.run(
        [ffprobe, "-v", "error", "-show_format", "-show_streams", "-of", "json", str(path)],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "ffprobe failed")
    return cast(dict[str, Any], json.loads(result.stdout))
