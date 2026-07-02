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
    value = re.sub(r'[<>:"/\\|?*]', "_", value)
    value = "".join("_" if ord(character) < 32 else character for character in value)
    return value.strip(" .") or "untitled"


def prepare_output_dir(path: Path, *, create: bool, overwrite: bool) -> Path:
    resolved = path.expanduser().resolve()
    if resolved.exists() and not resolved.is_dir():
        raise NotADirectoryError(f"Output path is not a directory: {resolved}")
    if resolved.exists() and not overwrite and any(resolved.iterdir()):
        raise FileExistsError(
            f"Output directory is not empty: {resolved}. "
            "Choose another directory or pass --overwrite."
        )
    if create:
        resolved.mkdir(parents=True, exist_ok=True)
    return resolved
