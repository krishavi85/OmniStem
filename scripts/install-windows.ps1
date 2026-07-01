$ErrorActionPreference = "Stop"
python -m venv .venv
& .\.venv\Scripts\python.exe -m pip install --upgrade pip
& .\.venv\Scripts\python.exe -m pip install -e ".[dev]"
Write-Host "Core installed. Activate with: .venv\Scripts\Activate.ps1"
Write-Host "Then install an engine, for example: pip install -U demucs"
