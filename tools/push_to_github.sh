#!/usr/bin/env bash
# Push the bilingual MindShare_PCIe_Technology_3.0_EN_VS_CN repo to GitHub.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/.." && pwd)"

REMOTE="${REMOTE:-git@github.com:jimwang2050/MindShare_PCIe_Technology_3.0_EN_VS_CN.git}"
MSG="${MSG:-chore: update translation progress}"

cd "$ROOT"

if ! git rev-parse --git-dir >/dev/null 2>&1; then
  git init -q -b main
  git config user.email "translator@mindshare-pcie.local" || true
  git config user.name "MindShare PCIe Translator" || true
fi

# Remote
if git remote get-url origin >/dev/null 2>&1; then
  git remote set-url origin "$REMOTE"
else
  git remote add origin "$REMOTE"
fi

git add -A
git diff --cached --quiet || git commit -q -m "$MSG"
git push -u origin main
echo "Pushed to $REMOTE"
