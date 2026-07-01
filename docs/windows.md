# Windows installation

1. Install Python 3.10 or 3.11 and enable `Add Python to PATH`.
2. Install FFmpeg and confirm `ffmpeg -version` and `ffprobe -version`.
3. Run `scripts/install-windows.ps1`.
4. Activate `.venv` and install at least one engine.
5. Run `omnistem doctor`.

GPU packages must match the installed NVIDIA driver and supported CUDA runtime. Follow the selected engine's current installation documentation rather than forcing an arbitrary PyTorch build.
