from __future__ import annotations

import argparse
import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

from repository import knowledge_repository
from repository.migrations import canonical_repository_migration as audit


DEFAULT_REPORT = Path("repository_canonical_migration_applied.json")


def update_canonical_record(
    connection: sqlite3.Connection,
    record_id: int,
    merged: Dict[str, Any],
) -> None:
    connection.execute(
        """
        UPDATE knowledge_objects
        SET
            title = ?,
            source = ?,
            source_type = ?,
            document_type = ?,
            research_domain = ?,
            authors = ?,
            publication_year = ?,
            doi = ?,
            abstract = ?,
            keywords = ?,
            pdf_link = ?,
            open_access = ?,
            local_file = ?,
            ai_summary = ?,
            status = ?,
            confidence = ?,
            date_added = ?,
            raw_json = ?
        WHERE id = ?
        """,
        (
            merged["title"],
            merged["source"],
            merged["source_type"],
            merged["document_type"],
            merged["research_domain"],
            json.dumps(merged["authors"], ensure_ascii=False),
            merged["publication_year"],
            knowledge_repository.normalize_doi(merged["doi"]),
            merged["abstract"],
            json.dumps(merged["keywords"], ensure_ascii=False),
            merged["pdf_link"],
            1 if merged["open_access"] else 0,
            merged["local_file"],
            merged["ai_summary"],
            merged["status"],
            merged["confidence"],
            merged["date_added"],
            json.dumps(merged, ensure_ascii=False),
            record_id,
        ),
    )


def count_duplicate_doi_groups(
    connection: sqlite3.Connection,
) -> int:
    row = connection.execute(
        """
        WITH normalized AS (
            SELECT
                LOWER(
                    TRIM(
                        REPLACE(
                            REPLACE(
                                REPLACE(
                                    REPLACE(
                                        COALESCE(doi, ''),
                                        'https://doi.org/',
                                        ''
                                    ),
                                    'http://doi.org/',
                                    ''
                                ),
                                'http://dx.doi.org/',
                                ''
                            ),
                            'doi:',
                            ''
                        )
                    )
                ) AS normalized_doi
            FROM knowledge_objects
        )
        SELECT COUNT(*)
        FROM (
            SELECT normalized_doi
            FROM normalized
            WHERE normalized_doi <> ''
            GROUP BY normalized_doi
            HAVING COUNT(*) > 1
        )
        """
    ).fetchone()

    return int(row[0])


def count_duplicate_title_groups_without_doi(
    connection: sqlite3.Connection,
) -> int:
    rows = connection.execute(
        """
        SELECT id, title
        FROM knowledge_objects
        WHERE TRIM(COALESCE(doi, '')) = ''
        """
    ).fetchall()

    counts: Dict[str, int] = {}

    for row in rows:
        normalized = knowledge_repository.normalize_title(row["title"])

        if normalized:
            counts[normalized] = counts.get(normalized, 0) + 1

    return sum(1 for count in counts.values() if count > 1)


def create_integrity_indexes(
    connection: sqlite3.Connection,
) -> None:
    connection.execute(
        """
        CREATE UNIQUE INDEX IF NOT EXISTS
        ux_knowledge_objects_normalized_doi
        ON knowledge_objects (
            LOWER(
                TRIM(
                    REPLACE(
                        REPLACE(
                            REPLACE(
                                REPLACE(
                                    COALESCE(doi, ''),
                                    'https://doi.org/',
                                    ''
                                ),
                                'http://doi.org/',
                                ''
                            ),
                            'http://dx.doi.org/',
                            ''
                        ),
                        'doi:',
                        ''
                    )
                )
            )
        )
        WHERE TRIM(COALESCE(doi, '')) <> ''
        """
    )

    connection.execute(
        """
        CREATE INDEX IF NOT EXISTS
        ix_knowledge_objects_normalized_title
        ON knowledge_objects (LOWER(TRIM(title)))
        """
    )


def apply_migration(
    database: Path,
    report_file: Path,
) -> Dict[str, Any]:
    integrity_before = audit.verify_sqlite_integrity(database)

    if integrity_before.lower() != "ok":
        raise RuntimeError(
            f"Pre-migration SQLite integrity failed: {integrity_before}"
        )

    plan = audit.build_migration_plan(database)
    backup_path = audit.create_backup(database)

    connection = audit.connect(database)

    try:
        connection.execute("BEGIN IMMEDIATE")

        for group in plan.duplicate_groups:
            canonical_id = group.record_ids[0]
            merged = audit.merge_duplicate_group(connection, group)

            update_canonical_record(
                connection,
                canonical_id,
                merged,
            )

            redundant_ids = group.record_ids[1:]

            if redundant_ids:
                placeholders = ",".join("?" for _ in redundant_ids)

                connection.execute(
                    f"""
                    DELETE FROM knowledge_objects
                    WHERE id IN ({placeholders})
                    """,
                    redundant_ids,
                )

        create_integrity_indexes(connection)

        rows_after = int(
            connection.execute(
                "SELECT COUNT(*) FROM knowledge_objects"
            ).fetchone()[0]
        )

        duplicate_doi_groups_after = count_duplicate_doi_groups(
            connection
        )
        duplicate_title_groups_after = (
            count_duplicate_title_groups_without_doi(connection)
        )

        if rows_after != plan.projected_rows_after:
            raise RuntimeError(
                "Unexpected post-migration row count: "
                f"expected {plan.projected_rows_after}, got {rows_after}"
            )

        if duplicate_doi_groups_after != 0:
            raise RuntimeError(
                "Duplicate DOI groups remain after migration: "
                f"{duplicate_doi_groups_after}"
            )

        if duplicate_title_groups_after != 0:
            raise RuntimeError(
                "Duplicate title groups without DOI remain: "
                f"{duplicate_title_groups_after}"
            )

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()

    integrity_after = audit.verify_sqlite_integrity(database)

    if integrity_after.lower() != "ok":
        raise RuntimeError(
            f"Post-migration SQLite integrity failed: {integrity_after}"
        )

    result = {
        "mode": "applied",
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "database": str(database),
        "backup": str(backup_path),
        "rows_before": plan.total_rows_before,
        "duplicate_groups_merged": plan.duplicate_group_count,
        "redundant_rows_deleted": plan.redundant_row_count,
        "rows_after": plan.projected_rows_after,
        "duplicate_doi_groups_after": 0,
        "duplicate_title_groups_without_doi_after": 0,
        "unique_normalized_doi_index": (
            "ux_knowledge_objects_normalized_doi"
        ),
        "normalized_title_index": (
            "ix_knowledge_objects_normalized_title"
        ),
        "sqlite_integrity_before": integrity_before,
        "sqlite_integrity_after": integrity_after,
    }

    report_file.write_text(
        json.dumps(result, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--database",
        type=Path,
        default=audit.DEFAULT_DB_FILE,
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=DEFAULT_REPORT,
    )
    parser.add_argument(
        "--apply",
        action="store_true",
    )

    arguments = parser.parse_args()

    if not arguments.apply:
        raise RuntimeError(
            "Migration not applied. Rerun with --apply."
        )

    result = apply_migration(
        database=arguments.database,
        report_file=arguments.report,
    )

    print("=" * 72)
    print("AROS CANONICAL REPOSITORY MIGRATION COMPLETE")
    print("=" * 72)

    for key, value in result.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
