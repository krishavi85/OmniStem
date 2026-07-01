# Contributing

1. Create a branch from `main`.
2. Install `pip install -e ".[dev]"`.
3. Add tests for behavior changes.
4. Run `ruff check .` and `pytest`.
5. Keep engine-specific flags inside the corresponding adapter.
6. Never add an unverified model URL, hash, license, or capability.
7. Do not commit model weights or copyrighted test audio.
