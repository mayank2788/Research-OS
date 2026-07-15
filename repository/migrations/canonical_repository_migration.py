"""
AROS Canonical Repository Migration.

Milestone 4A:
- identify historical duplicate records;
- select and enrich one canonical record per duplicate group;
- plan redundant-row deletion;
- plan canonical identity columns and unique indexes;
- support safe dry-run before database modification.

The default operation is dry-run. No database changes occur unless
apply_migration() is called explicitly.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sqlite3
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence

from repository import knowledge_repository


DEFAULT_DB_FILE = Path("data/aros_knowledge.db")
DEFAULT_BACKUP_FOLDER = Path("data/backups")


@dataclass(frozen=True)
class DuplicateGroup:
    identity_type: str
    identity_value: str
    record_ids: tuple[int, ...]


@dataclass(frozen=True)
class MigrationPlan:
    total_rows_before: int
    duplicate_groups: tuple[DuplicateGroup, ...]
    redundant_record_ids: tuple[int, ...]
    projected_rows_after: int

    @property
    def duplicate_group_count(self) -> int:
        return len(self.duplicate_groups)

    @property
    def redundant_row_count(self) -> int:
        return len(self.redundant_record_ids)


def connect(db_file: Path = DEFAULT_DB_FILE) -> sqlite3.Connection:
    connection = sqlite3.connect(db_file)
    connection.row_factory = sqlite3.Row
    return connection


def normalize_title_for_identity(title: Optional[str]) -> str:
    return knowledge_repository.normalize_title(title)


def normalize_doi_for_identity(doi: Optional[str]) -> str:
    return knowledge_repository.normalize_doi(doi)


def count_rows(connection: sqlite3.Connection) -> int:
    cursor = connection.execute(
        "SELECT COUNT(*) AS total FROM knowledge_objects"
    )
    return int(cursor.fetchone()["total"])


def read_identity_rows(
    connection: sqlite3.Connection,
) -> List[sqlite3.Row]:
    cursor = connection.execute(
        """
        SELECT id, title, doi
        FROM knowledge_objects
        ORDER BY id ASC
        """
    )
    return list(cursor.fetchall())


def group_duplicate_dois(
    rows: Iterable[sqlite3.Row],
) -> List[DuplicateGroup]:
    groups: Dict[str, List[int]] = {}

    for row in rows:
        normalized_doi = normalize_doi_for_identity(row["doi"])

        if normalized_doi:
            groups.setdefault(normalized_doi, []).append(int(row["id"]))

    return [
        DuplicateGroup(
            identity_type="doi",
            identity_value=identity,
            record_ids=tuple(record_ids),
        )
        for identity, record_ids in sorted(groups.items())
        if len(record_ids) > 1
    ]


def group_duplicate_titles_without_doi(
    rows: Iterable[sqlite3.Row],
) -> List[DuplicateGroup]:
    groups: Dict[str, List[int]] = {}

    for row in rows:
        normalized_doi = normalize_doi_for_identity(row["doi"])

        if normalized_doi:
            continue

        normalized_title = normalize_title_for_identity(row["title"])

        if normalized_title:
            groups.setdefault(normalized_title, []).append(int(row["id"]))

    return [
        DuplicateGroup(
            identity_type="title_without_doi",
            identity_value=identity,
            record_ids=tuple(record_ids),
        )
        for identity, record_ids in sorted(groups.items())
        if len(record_ids) > 1
    ]


def build_migration_plan(
    db_file: Path = DEFAULT_DB_FILE,
) -> MigrationPlan:
    connection = connect(db_file)

    try:
        total_rows = count_rows(connection)
        rows = read_identity_rows(connection)

        duplicate_groups = (
            group_duplicate_dois(rows)
            + group_duplicate_titles_without_doi(rows)
        )

        redundant_ids: List[int] = []

        for group in duplicate_groups:
            # Preserve the oldest repository ID as the canonical record.
            redundant_ids.extend(group.record_ids[1:])

        redundant_ids = sorted(set(redundant_ids))

        return MigrationPlan(
            total_rows_before=total_rows,
            duplicate_groups=tuple(duplicate_groups),
            redundant_record_ids=tuple(redundant_ids),
            projected_rows_after=total_rows - len(redundant_ids),
        )
    finally:
        connection.close()


def get_record(
    connection: sqlite3.Connection,
    record_id: int,
) -> Dict[str, Any]:
    row = connection.execute(
        """
        SELECT *
        FROM knowledge_objects
        WHERE id = ?
        """,
        (record_id,),
    ).fetchone()

    if row is None:
        raise RuntimeError(f"Repository record {record_id} was not found.")

    record = dict(row)

    for field in ("authors", "keywords"):
        try:
            record[field] = json.loads(record.get(field) or "[]")
        except (json.JSONDecodeError, TypeError):
            record[field] = []

    record["open_access"] = bool(record.get("open_access"))

    return record


def merge_duplicate_group(
    connection: sqlite3.Connection,
    group: DuplicateGroup,
) -> Dict[str, Any]:
    records = [
        get_record(connection, record_id)
        for record_id in group.record_ids
    ]

    canonical = records[0]

    for incoming in records[1:]:
        canonical = knowledge_repository.merge_knowledge_object_data(
            canonical,
            incoming,
        )

    return canonical


def verify_sqlite_integrity(
    db_file: Path = DEFAULT_DB_FILE,
) -> str:
    connection = sqlite3.connect(db_file)

    try:
        row = connection.execute("PRAGMA integrity_check").fetchone()
        return str(row[0])
    finally:
        connection.close()


def create_backup(
    db_file: Path = DEFAULT_DB_FILE,
    backup_folder: Path = DEFAULT_BACKUP_FOLDER,
) -> Path:
    backup_folder.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = (
        backup_folder
        / f"aros_knowledge_before_canonical_migration_{timestamp}.db"
    )

    shutil.copy2(db_file, backup_path)

    integrity_result = verify_sqlite_integrity(backup_path)

    if integrity_result.lower() != "ok":
        backup_path.unlink(missing_ok=True)
        raise RuntimeError(
            "Migration backup failed SQLite integrity verification: "
            f"{integrity_result}"
        )

    return backup_path


def print_plan(plan: MigrationPlan) -> None:
    print("=" * 72)
    print("AROS CANONICAL REPOSITORY MIGRATION — DRY RUN")
    print("=" * 72)
    print(f"Rows before migration     : {plan.total_rows_before}")
    print(f"Duplicate groups          : {plan.duplicate_group_count}")
    print(f"Redundant rows identified : {plan.redundant_row_count}")
    print(f"Projected rows after      : {plan.projected_rows_after}")

    print()
    print("Duplicate Groups")
    print("----------------")

    if not plan.duplicate_groups:
        print("None")
        return

    for group in plan.duplicate_groups:
        canonical_id = group.record_ids[0]
        redundant_ids = group.record_ids[1:]

        print(
            f"{group.identity_type:18} | "
            f"{group.identity_value} | "
            f"canonical={canonical_id} | "
            f"remove={list(redundant_ids)}"
        )


def write_plan_report(
    plan: MigrationPlan,
    output_file: Path,
) -> None:
    payload = {
        "mode": "dry-run",
        "total_rows_before": plan.total_rows_before,
        "duplicate_group_count": plan.duplicate_group_count,
        "redundant_row_count": plan.redundant_row_count,
        "projected_rows_after": plan.projected_rows_after,
        "duplicate_groups": [
            {
                "identity_type": group.identity_type,
                "identity_value": group.identity_value,
                "canonical_record_id": group.record_ids[0],
                "redundant_record_ids": list(group.record_ids[1:]),
            }
            for group in plan.duplicate_groups
        ],
    }

    output_file.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit AROS historical repository duplicates."
    )
    parser.add_argument(
        "--database",
        type=Path,
        default=DEFAULT_DB_FILE,
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path(
            "repository_canonical_migration_dry_run.json"
        ),
    )
    return parser.parse_args()


def main() -> None:
    arguments = parse_arguments()

    integrity_result = verify_sqlite_integrity(arguments.database)

    if integrity_result.lower() != "ok":
        raise RuntimeError(
            "SQLite integrity check failed before migration planning: "
            f"{integrity_result}"
        )

    plan = build_migration_plan(arguments.database)
    print_plan(plan)
    write_plan_report(plan, arguments.report)

    print()
    print(f"SQLite integrity          : {integrity_result}")
    print(f"Dry-run report            : {arguments.report}")
    print("Database modified         : NO")


if __name__ == "__main__":
    main()
