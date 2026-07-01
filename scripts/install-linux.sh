#!/usr/bin/env bash
set -euo pipefail
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -e ".[dev]"
echo "Core installed. Run: source .venv/bin/activate"
echo "Then install an engine, for example: pip install -U demucs"
