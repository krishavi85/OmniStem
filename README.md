# OmniStem God Mode

OmniStem is a local-first orchestration layer for real open-source music source-separation engines. It does not reimplement the neural networks or bundle third-party checkpoints. It detects installed engines, constructs their native commands safely, runs them without shell interpolation, records job history in SQLite, and writes a reproducible JSON manifest for every run.

## Implemented in 0.1.0

- Unified `omnistem` CLI
- Real adapters for Audio Separator, Demucs, Spleeter, and Open-Unmix
- `doctor`, `env`, model registry, audio inspection, batch separation, dry runs, and JSON output
- Persistent SQLite job history
- Per-run `job-manifest.json`
- Validated weighted waveform ensemble
- Optional FastAPI server
- Optional PySide6 desktop application
- FFmpeg/FFprobe diagnostics
- Unit tests and GitHub Actions
- Docker and Windows/Linux setup scripts

## Important licensing design

OmniStem invokes upstream packages as external engines. It does not vendor their source code or model weights. Code licenses and checkpoint licenses can differ. Review `THIRD_PARTY_LICENSES.md` and `MODEL_LICENSES.md` before distributing outputs or using a model commercially.

## Requirements

- Python 3.10+
- FFmpeg recommended
- At least one supported engine installed

## Install core

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e .
```

Linux/macOS:

```bash
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e .
```

Install one or more engines in the same environment, or use a dedicated environment per engine:

```bash
pip install -U demucs
pip install "audio-separator[cpu]"
pip install spleeter
pip install openunmix
```

Optional OmniStem features:

```bash
pip install -e ".[ensemble]"
pip install -e ".[api]"
pip install -e ".[desktop]"
pip install -e ".[dev]"
```

## First checks

```bash
omnistem --version
omnistem doctor
omnistem env --json
omnistem engines list
omnistem models list
```

## Separate audio

Audio Separator with a verified BS-RoFormer filename:

```bash
omnistem separate song.wav \
  --engine audio-separator \
  --model model_bs_roformer_ep_317_sdr_12.9755.ckpt \
  --stems vocals,instrumental \
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

Spleeter:

```bash
omnistem separate song.mp3 \
  --engine spleeter \
  --model spleeter:4stems \
  --stems vocals,drums,bass,other \
  --output outputs/spleeter
```

Open-Unmix:

```bash
omnistem separate song.wav \
  --engine openunmix \
  --model umxhq \
  --stems vocals,drums,bass,other \
  --output outputs/openunmix
```

Preview the exact command without running it:

```bash
omnistem separate song.wav --engine demucs --model htdemucs_ft --dry-run --json
```

## Batch mode

```bash
omnistem batch ./songs \
  --engine audio-separator \
  --model UVR-MDX-NET-Inst_HQ_3.onnx \
  --output ./separated \
  --recursive
```

## Ensemble aligned stems

Install `omnistem[ensemble]`, then:

```bash
omnistem ensemble model-a/vocals.wav model-b/vocals.wav \
  --weights 0.6,0.4 \
  --output ensemble/vocals.wav
```

The ensemble command rejects mismatched sample rates, channel counts, or durations.

## API

```bash
pip install -e ".[api]"
omnistem serve --host 127.0.0.1 --port 8765
```

Main endpoints:

- `GET /health`
- `GET /engines`
- `GET /models`
- `GET /jobs`
- `POST /jobs`

The API binds to localhost by default. Do not expose it publicly without authentication and network controls.

## Desktop

```bash
pip install -e ".[desktop]"
omnistem desktop
```

The desktop MVP lets users select an audio file, output folder, engine, native model name, and stems; then it streams engine logs and writes a manifest.

## Development

```bash
pip install -e ".[dev]"
ruff check .
pytest
```

## Repository status

This release is a working orchestration MVP. Advanced MSST, MVSEP-MDX23, native BSRoformer.cpp, node pipelines, spectral ensembles, installer generation, and benchmark scoring belong to the next milestones. They are not falsely presented as implemented.
