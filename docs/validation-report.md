# Validation report — 2026-07-01

OmniStem 0.1.1 was audited against the source currently published on `main`.

## Passed checks

- `python -m compileall -q src tests`
- `ruff check src tests`
- `mypy src/omnistem`
- `pytest -q`: 14 tests passed
- `python -m build`: source distribution and wheel built successfully in isolated build environments
- Clean virtual-environment wheel installation
- `pip check` in the clean virtual environment
- `omnistem --version`
- `omnistem models list --json`
- FastAPI `/health` smoke test
- FastAPI invalid-job validation returned HTTP 400
- Demucs dry-run command resolution
- Open-Unmix dry-run command resolution with `--ext`, `--no-cuda`, and `--residual instrumental`
- Dry runs did not create output directories

## Verified behavior

- Audio Separator receives its selected output format and model filename.
- Demucs validates four-stem, six-stem, and two-stem target requests.
- Spleeter uses the shared executable/module command-prefix mechanism and validates supported stem counts.
- Open-Unmix restricts native input formats to WAV, FLAC, and OGG and supplies the required residual name.
- Non-empty output directories require explicit overwrite permission.
- A process that exits successfully but creates no new audio artifacts is recorded as a failed separation.

## Validation boundary

No full neural separation was executed during this repository audit because doing so requires downloading large third-party checkpoints and, for GPU validation, compatible hardware and drivers. The adapters and generated commands are real; final inference quality and runtime compatibility depend on the exact installed engine, model, framework, operating system, and accelerator.
