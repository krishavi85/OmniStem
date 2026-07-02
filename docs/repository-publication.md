# OmniStem repository guide

Official repository: `https://github.com/krishavi85/OmniStem`

## Clone

```bash
git clone https://github.com/krishavi85/OmniStem.git
cd OmniStem
```

Confirm the remote and branch:

```bash
git remote -v
git branch --show-current
```

## Update

Commit or stash local work, then update without creating an unintended merge commit:

```bash
git switch main
git fetch origin
git pull --ff-only origin main
```

## Connect an existing local checkout

When `origin` exists:

```bash
git remote set-url origin https://github.com/krishavi85/OmniStem.git
```

When `origin` does not exist:

```bash
git remote add origin https://github.com/krishavi85/OmniStem.git
```

Publish the local main branch only when you have write access:

```bash
git branch -M main
git push -u origin main
```

Use your normal GitHub credential setup. Contributors without direct access should fork the repository, create a feature branch, and open a pull request against `main`.

## Verify before contributing

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e ".[dev,api,ensemble]"
ruff check src tests
mypy src/omnistem
pytest
python -m build
```

On Windows PowerShell, activate with `.venv\Scripts\Activate.ps1` and run the same Python, lint, type-check, test, and build commands.

Do not commit model weights, private or copyrighted audio, virtual environments, local databases, or build output. Use feature branches and pull requests instead of rewriting the shared `main` branch.
