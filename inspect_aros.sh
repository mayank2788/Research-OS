#!/usr/bin/env bash
# AROS project inspection — quick health check before development work.
# Usage: ./inspect_aros.sh

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

echo "======================================================================"
echo "AROS INSPECTION"
echo "======================================================================"
echo
echo "Project root: $ROOT"
echo "Date:         $(date '+%d %B %Y, %I:%M %p %Z')"
echo

echo "Environment"
echo "----------------------------------------------------------------------"
if command -v python3 >/dev/null 2>&1; then
  echo "Python:       $(python3 --version 2>&1)"
else
  echo "Python:       not found"
fi

if [[ -f ".env" ]]; then
  echo ".env:         present"
  if grep -q "AROS_CONTACT_EMAIL=" .env && ! grep -q "your_email@example.com" .env; then
    echo "Contact email: configured"
  else
    echo "Contact email: missing or placeholder"
  fi
  if grep -qE '^OPENALEX_API_KEY=.+$' .env; then
    echo "OpenAlex key:  configured"
  else
    echo "OpenAlex key:  missing"
  fi
else
  echo ".env:         missing (copy from .env.example)"
fi
echo

echo "Git"
echo "----------------------------------------------------------------------"
echo "Branch:       $(git branch --show-current 2>/dev/null || echo 'not a git repo')"
echo "Latest commit: $(git log --oneline -1 2>/dev/null || echo 'unavailable')"
if [[ -z "$(git status --porcelain 2>/dev/null || true)" ]]; then
  echo "Working tree: clean"
else
  echo "Working tree: changes present"
  git status --short
fi
echo

echo "Core pipeline folders"
echo "----------------------------------------------------------------------"
for folder in reader knowledge repository connector_framework connectors docs tools; do
  if [[ -d "$folder" ]]; then
    echo "OK  $folder"
  else
    echo "MISSING  $folder"
  fi
done
echo

echo "Repository snapshot"
echo "----------------------------------------------------------------------"
python3 - <<'PY'
import sqlite3
from pathlib import Path

db = Path("data/knowledge_repository.db")
if db.exists():
    conn = sqlite3.connect(db)
    count = conn.execute("SELECT COUNT(*) FROM knowledge_objects").fetchone()[0]
    print(f"SQLite DB:    {db}")
    print(f"Objects:      {count}")
    conn.close()
else:
    print("SQLite DB:    data/knowledge_repository.db not found")

ko_dir = Path("knowledge/objects")
if ko_dir.exists():
    count = len(list(ko_dir.rglob("*.json")))
    print(f"KO JSON files: {count}")
else:
    print("Knowledge objects: knowledge/objects/ not found")
PY
echo

echo "Project status report"
echo "----------------------------------------------------------------------"
if [[ -f "tools/project_status.py" ]]; then
  python3 tools/project_status.py
else
  echo "tools/project_status.py not found"
fi

echo
echo "Done. Next step: Plan -> Inspect -> Understand -> Document -> Implement"
