from __future__ import annotations

import re
from pathlib import Path

SUPPORTED_INPUT_EXTENSIONS = {
    ".wav",
    ".flac",
    ".aiff",
    ".aif",
    ".mp3",
    ".aac",
    ".m4a",
    ".ogg",
    ".opus",
    ".wma",
    ".alac",
    ".caf",
}


def validate_input_file(path: Path) -> Path:
    resolved = path.expanduser().resolve()
    if not resolved.is_file():
        raise FileNotFoundError(f"Input audio file does not exist: {resolved}")
    if resolved.suffix.lower() not in SUPPORTED_INPUT_EXTENSIONS:
        raise ValueError(f"Unsupported audio extension: {resolved.suffix}")
    return resolved


def safe_name(value: str) -> str:
    value = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", value).strip(" .")
    return value or "untitled"


def ensure_output_dir(path: Path) -> Path:
    resolved = path.expanduser().resolve()
    resolved.mkdir(parents=True, exist_ok=True)
    return resolved
