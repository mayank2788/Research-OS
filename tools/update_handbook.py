from pathlib import Path
from datetime import datetime
import subprocess


ROOT = Path.cwd()
HANDBOOK = ROOT / "docs" / "handbook"
SOURCES = ROOT / "docs" / "chatgpt-project-sources"


def run_command(command: str) -> str:
    try:
        return subprocess.check_output(
            command,
            shell=True,
            text=True,
            stderr=subprocess.STDOUT
        ).strip()
    except Exception as error:
        return f"ERROR: {error}"


def write_file(folder: Path, filename: str, content: str) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / filename
    path.write_text(content.strip() + "\n", encoding="utf-8")


def main():
    today = datetime.now().strftime("%d %B %Y")
    git_commit = run_command("git log --oneline -1")
    git_status = run_command("git status --short")
    python_version = run_command("python3 --version")

    documents = {
        "00_EXECUTIVE_SUMMARY.md": f"""
# AROS Executive Summary

Date: {today}

## Project Name

AROS – AI Research Operating System

## Current Stage

Baseline 0.1

## Achieved Till Date

- Cursor IDE operational
- Git and GitHub configured
- Python environment verified
- Research-OS repository created
- Reader module verified
- Knowledge Object module verified
- Repository module verified
- Connector Framework verified
- Module audit documentation started
- Engineering Handbook skeleton created

## Current Git Baseline

{git_commit}

## Development Rule

One objective at a time.

Understand → Document → Implement → Test → Verify → Commit → Push
""",

        "01_DEVELOPMENT_ENVIRONMENT.md": f"""
# AROS Development Environment

Date: {today}

## Verified Tools

- macOS workstation
- Cursor IDE
- Cursor integrated terminal
- Python
- Git
- GitHub
- ChatGPT Project
- Research-Papers folder

## Python Version

{python_version}

## AROS Code Path

/Users/anamika/Documents/GitHub/Projects/Python/Research-OS

## Research Library Path

/Users/anamika/Documents/GitHub/Research-Papers

## Cursor Rule

Use Cursor Integrated Terminal for AROS development.

## Git Status at Generation

{git_status if git_status else "Clean working tree except generated documentation if uncommitted."}
""",

        "02_CURRENT_ARCHITECTURE.md": """
# AROS Current Architecture

## Existing Modules

- reader/
- knowledge/
- repository/
- connectors/
- profile/
- scout/
- app.py

## Current Pipeline

Research-Papers
↓
Reader
↓
Knowledge Object
↓
Repository
↓
Connector Framework
↓
Future Scout / AI Layer

## Verified Modules

- Reader
- Knowledge Object
- Repository
- Connector Framework

## Pending Audit

- Profile
- Scout
- app.py
""",

        "03_MODULE_REGISTRY.md": """
# AROS Module Registry

| Module | Status | Notes |
|---|---|---|
| Reader | Verified | Reads PDF and generates text report |
| Knowledge Object | Verified | Creates structured knowledge object |
| Repository | Verified | Stores knowledge objects in SQLite |
| Connector Framework | Verified | Mock connector works |
| Profile | Pending | Needs audit |
| Scout | Pending | Needs audit |
| app.py | Pending | Needs audit |
""",

        "04_ENGINEERING_STANDARDS.md": """
# AROS Engineering Standards

## Working Rules

1. One objective at a time.
2. Do not open multiple fronts.
3. Audit before rewriting.
4. Verify before committing.
5. Keep documentation synchronized with code.
6. Prefer practical progress toward live research usage.
7. Preserve architecture unless there is a clear reason to change.

## Standard Workflow

Plan
↓
Inspect
↓
Understand
↓
Document
↓
Implement
↓
Test
↓
Verify
↓
Commit
↓
Push
""",

        "05_AI_AGENT_GUIDE.md": """
# AROS AI Agent Guide

Any AI assistant working on AROS must follow these rules:

1. Work on one objective until verified.
2. Do not rewrite existing modules before auditing them.
3. Preserve the pipeline: Source → Connector → Knowledge Object → Repository.
4. Distinguish achieved from proposed.
5. Explain major technical decisions briefly.
6. Prefer speed toward a working live research system.
7. Do not over-engineer early modules.
8. Verify code before recommending commit.
9. Keep documentation updated.
10. Treat AROS as an active research platform, not a finished product.
""",

        "06_ONE_PAGE_SUMMARY.md": f"""
# AROS One Page Summary

Date: {today}

## What We Built

AROS is now a working early-stage AI Research Operating System project with verified core foundations.

## What Is Working

- Cursor IDE
- GitHub repository
- Python 3.12 environment
- Reader module
- Knowledge Object module
- Repository module
- Connector Framework

## What We Verified

- PDF reading from Research-Papers
- Text extraction
- Word count
- Reading time
- Report generation
- Knowledge Object creation
- SQLite storage
- Mock connector ingestion

## Current Git Baseline

{git_commit}

## Current Priority

Prepare ChatGPT Project using structured documentation, then continue fast module audit and live research pipeline creation.

## Next Immediate Work

1. Upload these documents to ChatGPT Project Sources.
2. Complete Profile, Scout and app.py audit.
3. Build first working live research pipeline.
"""
    }

    for filename, content in documents.items():
        write_file(HANDBOOK, filename, content)
        write_file(SOURCES, filename, content)

    print("AROS Handbook and ChatGPT Project Sources generated.")
    print()
    print("Generated source files:")
    for file in sorted(SOURCES.glob("*.md")):
        print(file)


if __name__ == "__main__":
    main()