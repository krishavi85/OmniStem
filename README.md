# OmniStem Legacy Orchestration MVP

> **Legacy repository — maintenance only.** The canonical OmniStem Studio product repository is [`krishavi85/OmniScript-automation`](https://github.com/krishavi85/OmniScript-automation). New desktop, DAW, AI-worker, model-adapter, persistence, packaging, and release features belong there.

This repository preserves the earlier Python orchestration MVP. It remains useful for local command-line separation, the lightweight FastAPI service, and the basic PySide6 separation form, but it is not the primary OmniStem Studio application.

## What remains available here

- Unified `omnistem` command-line interface
- Audio Separator, Demucs, Spleeter, and Open-Unmix orchestration
- Engine-specific input, output-format, stem, and device validation
- Batch processing and dry runs
- SQLite job history and per-run manifests
- Weighted waveform ensemble
- Optional FastAPI server
- Optional PySide6 desktop separation form
- Docker and setup scripts

## Development policy

- Do not add new OmniStem Studio product features here.
- Apply only critical maintenance, dependency, security, or migration fixes.
- Port reusable orchestration behavior to `OmniScript-automation`.
- Open new feature requests and product pull requests in the canonical repository.

The Audio Separator, Demucs, Spleeter, and Open-Unmix capability definitions and command-validation behavior have begun moving to the canonical worker.

## Legacy installation

```bash
python -m venv .venv
```

Linux or macOS:

```bash
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e .
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e .
```

Install at least one supported separation engine separately.

## Legacy CLI examples

```bash
omnistem --version
omnistem doctor
omnistem engines list
omnistem models list
```

Demucs example:

```bash
omnistem separate song.wav \
  --engine demucs \
  --model htdemucs_ft \
  --stems vocals,drums,bass,other \
  --output outputs/demucs
```

Preview a validated command without running it:

```bash
omnistem separate song.wav --engine demucs --model htdemucs_ft --dry-run --json
```

## Optional legacy interfaces

FastAPI service:

```bash
pip install -e ".[api]"
omnistem serve --host 127.0.0.1 --port 8765
```

PySide6 form:

```bash
pip install -e ".[desktop]"
omnistem desktop
```

## Validation boundary

The repository tests command construction, input and output protections, history, manifests, API validation, packaging, and CLI behavior. Full neural inference depends on separately installed upstream engines, model checkpoints, framework versions, operating-system support, and accelerator drivers.

See `docs/validation-report.md` for the most recent legacy audit.

## Licensing

This repository is MIT licensed. Upstream engines and model checkpoints have their own licenses and redistribution terms. Review `THIRD_PARTY_LICENSES.md` and `MODEL_LICENSES.md` before commercial use or redistribution.
