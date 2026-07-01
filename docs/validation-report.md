# Validation report — 2026-07-01

Validated in the build environment with Python 3.13:

- `python -m compileall -q src tests`: passed
- `ruff check src tests`: passed
- `pytest -q`: 13 tests passed
- `mypy src/omnistem`: passed for the typed core, CLI, adapters, API-facing code, and ensemble logic; the optional PySide6 UI is excluded because PySide6 is not installed in the validation environment
- Wheel build: `omnistem-0.1.0-py3-none-any.whl` created successfully
- Clean virtual-environment wheel installation: passed
- Installed-wheel smoke tests: `omnistem --version` and `omnistem models list --json` passed
- Runtime diagnostics found FFmpeg/FFprobe and two available upstream engines in the build environment: Demucs and Open-Unmix
- Demucs dry-run command resolution: passed

No full neural separation was executed because that would require downloading large external model checkpoints. The adapters invoke real upstream executables and the tests verify exact command construction, but output quality remains dependent on the installed upstream engine and model.
