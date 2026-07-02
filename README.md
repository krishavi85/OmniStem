# OmniStem God Mode

OmniStem is a local-first orchestration layer for real open-source music source-separation engines. It does not simulate separation or bundle third-party checkpoints. It validates a job, constructs the selected engine's native command without shell interpolation, runs the external process, records history in SQLite, and writes a reproducible JSON manifest.

## Implemented in 0.1.1

- Unified `omnistem` CLI
- Real adapters for Audio Separator, Demucs, Spleeter, and Open-Unmix
- Engine-specific input, output-format, stem, and device validation
- Batch processing, dry runs, JSON output, environment diagnostics, and model metadata
- Persistent SQLite job history and per-run manifests
- Validated weighted waveform ensemble
- Optional FastAPI server and PySide6 desktop application
- Cross-platform tests and GitHub Actions
- Docker configuration and Windows/Linux setup scripts

## What “real” means

OmniStem invokes the actual upstream command-line programs. A full separation requires the selected package, its runtime dependencies, and its model weights. Model downloads can be large and are handled by the upstream engine.

The test suite validates command construction, input/output protection, manifests, history, packaging, and CLI behavior. It does not download every neural model during CI.

## Requirements

- Python 3.10 or newer for OmniStem core
- FFmpeg and FFprobe recommended
- At least one supported engine installed
- Spleeter 2.4.x requires a Python 3.8-3.11 environment

## Install

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

Install one or more engines:

```bash
pip install -U demucs
pip install "audio-separator[cpu]"
pip install "openunmix>=1.3,<2"
```

Install Spleeter in Python 3.11:

```bash
pip install "spleeter>=2.4,<2.5"
```

Optional application features:

```bash
pip install -e ".[ensemble]"
pip install -e ".[api]"
pip install -e ".[desktop]"
pip install -e ".[dev]"
```

## Diagnose the environment

```bash
omnistem --version
omnistem doctor
omnistem env --json
omnistem engines list
omnistem models list
```

## Separation examples

Audio Separator:

```bash
omnistem separate song.wav \
  --engine audio-separator \
  --model model_bs_roformer_ep_317_sdr_12.9755.ckpt \
  --stems vocals,instrumental \
  --format flac \
  --output outputs/bs-roformer
```

Demucs four stems:

```bash
omnistem separate song.wav \
  --engine demucs \
  --model htdemucs_ft \
  --stems vocals,drums,bass,other \
  --device cuda \
  --output outputs/demucs
```

Demucs six stems:

```bash
omnistem separate song.wav \
  --engine demucs \
  --model htdemucs_6s \
  --stems vocals,drums,bass,guitar,piano,other \
  --output outputs/demucs-6s
```

Spleeter four stems:

```bash
omnistem separate song.mp3 \
  --engine spleeter \
  --model spleeter:4stems \
  --stems vocals,drums,bass,other \
  --output outputs/spleeter
```

Open-Unmix vocals plus instrumental residual:

```bash
omnistem separate song.wav \
  --engine openunmix \
  --model umxhq \
  --stems vocals,instrumental \
  --device cpu \
  --output outputs/openunmix
```

Open-Unmix accepts WAV, FLAC, and OGG input through its native CLI. Convert MP3 or M4A input with FFmpeg first.

Preview the validated command without running it or creating the output directory:

```bash
omnistem separate song.wav --engine demucs --model htdemucs_ft --dry-run --json
```

OmniStem refuses to use a non-empty output directory unless `--overwrite` is supplied.

## Batch mode

```bash
omnistem batch ./songs \
  --engine audio-separator \
  --model UVR-MDX-NET-Inst_HQ_3.onnx \
  --output ./separated \
  --recursive
```

## Ensemble

```bash
pip install -e ".[ensemble]"
omnistem ensemble model-a/vocals.wav model-b/vocals.wav \
  --weights 0.6,0.4 \
  --output ensemble/vocals.wav
```

## API

```bash
pip install -e ".[api]"
omnistem serve --host 127.0.0.1 --port 8765
```

## Desktop

```bash
pip install -e ".[desktop]"
omnistem desktop
```

## Docker

The default image installs Demucs:

```bash
docker build -t omnistem .
docker run --rm omnistem doctor --json
```

## Development

```bash
pip install -e ".[dev,api,ensemble]"
ruff check src tests
mypy src/omnistem
pytest
python -m build
```

See `docs/repository-publication.md` for clone, update, remote, contribution, and verification instructions.

## Licensing and scope

OmniStem does not vendor upstream source code or model weights. Review `THIRD_PARTY_LICENSES.md` and `MODEL_LICENSES.md` before redistribution or commercial checkpoint use.

This release is a working orchestration MVP, not the complete God Mode roadmap. MSST, MVSEP-MDX23, native BSRoformer.cpp, node pipelines, spectral ensembles, signed installers, and reference-dataset benchmarks remain future milestones.
