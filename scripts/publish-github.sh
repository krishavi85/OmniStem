#!/usr/bin/env bash
set -euo pipefail
repository_url="${1:-https://github.com/krishavi85/omnistem-god-mode.git}"
if git remote get-url origin >/dev/null 2>&1; then
  git remote set-url origin "$repository_url"
else
  git remote add origin "$repository_url"
fi
git branch -M main
git push -u origin main
