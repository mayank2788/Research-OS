from pathlib import Path
from datetime import datetime
import subprocess
import sys


ROOT = Path.cwd()


def run(command: str) -> str:
    try:
        return subprocess.check_output(
            command,
            shell=True,
            text=True,
            stderr=subprocess.STDOUT
        ).strip()
    except Exception as error:
        return f"ERROR: {error}"


def count_files(folder: Path, pattern: str = "*") -> int:
    if not folder.exists():
        return 0
    return len(list(folder.rglob(pattern)))


def status_icon(value: bool) -> str:
    return "✅" if value else "❌"


def main():
    print("=" * 70)
    print("AROS PROJECT STATUS")
    print("=" * 70)
    print()

    print("Generated:", datetime.now().strftime("%d %B %Y, %I:%M %p"))
    print("Project Root:", ROOT)
    print("Python:", sys.version.split()[0])
    print()

    print("Git")
    print("-" * 70)
    print("Branch:", run("git branch --show-current"))
    print("Latest Commit:", run("git log --oneline -1"))
    git_status = run("git status --short")
    print("Working Tree:", "Clean" if not git_status else "Changes present")
    if git_status:
        print(git_status)
    print()

    print("Core Folders")
    print("-" * 70)
    folders = [
        "reader",
        "knowledge",
        "repository",
        "connectors",
        "profile",
        "scout",
        "tools",
        "docs",
    ]
    for folder in folders:
        print(f"{status_icon((ROOT / folder).exists())} {folder}")
    print()

    print("Core Modules")
    print("-" * 70)
    modules = [
        "reader/pdf_reader.py",
        "knowledge/knowledge_object.py",
        "repository/knowledge_repository.py",
        "connectors/base/base_connector.py",
        "connectors/mock/mock_connector.py",
        "profile/profile_manager.py",
        "scout/scout.py",
        "app.py",
    ]
    for module in modules:
        print(f"{status_icon((ROOT / module).exists())} {module}")
    print()

    print("Documentation")
    print("-" * 70)
    print("Module audits:", count_files(ROOT / "docs" / "module-audits", "*.md"))
    print("Handbook files:", count_files(ROOT / "docs" / "handbook", "*.md"))
    print("ChatGPT source files:", count_files(ROOT / "docs" / "chatgpt-project-sources", "*.md"))
    print()

    print("Developer Tools")
    print("-" * 70)
    for tool in sorted((ROOT / "tools").glob("*.py")) if (ROOT / "tools").exists() else []:
        print(f"✅ {tool.name}")
    print()

    print("Verified Module Status")
    print("-" * 70)
    verified = {
        "Reader": "Verified",
        "Knowledge Object": "Verified",
        "Repository": "Verified",
        "Connector Framework": "Verified",
        "Profile": "Pending",
        "Scout": "Pending",
        "app.py": "Pending",
    }
    for name, status in verified.items():
        icon = "✅" if status == "Verified" else "🟡"
        print(f"{icon} {name}: {status}")

    print()
    print("=" * 70)
    print("END OF STATUS REPORT")
    print("=" * 70)


if __name__ == "__main__":
    main()