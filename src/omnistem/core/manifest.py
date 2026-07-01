from __future__ import annotations

import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from omnistem import __version__


def write_manifest(path: Path, payload: dict[str, Any]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    enriched = {
        "omnistem_version": __version__,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "platform": platform.platform(),
        "python": sys.version,
        **payload,
    }
    path.write_text(json.dumps(enriched, indent=2, ensure_ascii=False), encoding="utf-8")
    return path
