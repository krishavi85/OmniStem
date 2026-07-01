# Linux installation

```bash
sudo apt-get update
sudo apt-get install -y python3-venv ffmpeg libsndfile1
bash scripts/install-linux.sh
source .venv/bin/activate
pip install -U demucs
omnistem doctor
```
