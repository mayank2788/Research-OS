"""
AROS Repository Health and Administration.

Provides:
- SQLite integrity checks;
- repository statistics;
- duplicate identity audits;
- lifecycle distribution;
- metadata quality checks;
- index verification;
- human-readable and JSON reports.
"""

from __future__ import annotations

import argparse
import json
import sqlite3
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Optional

from repository import knowledge_repository


DEFAULT_DB_FILE = Path("data/aros_knowledge.db")
DEFAULT_JSON_REPORT = Path("repository_health_report.json")

EXPECTED_INDEXES = {
    "ux_knowledge_objects_normalized_doi",
    "ix_knowledge_objects_normalized_title",
}

RECOGNISED_STATUSES = {
    "discovered",
    "ingested",
    "downloaded",
    "enriched",
    "evaluated",
    "verified",
}


@dataclass(frozen=True)
class RepositoryHealthReport:
    database: str
    sqlite_integrity: str
    total_rows: int
    rows_with_doi: int
    rows_without_doi: int
    unique_normalized_dois: int
    duplicate_doi_groups: int
    duplicate_title_groups_without_doi: int
    lifecycle_counts: Dict[str, int]
    unknown_status_count: int
    missing_title_count: int
    missing_abstract_count: int
    missing_authors_count: int
    missing_keywords_count: int
    missing_publication_year_count: int
    missing_pdf_link_count: int
    missing_local_file_count: int
    indexes_present: List[str]
    missing_expected_indexes: List[str]
    overall_status: str


def connect(database: Path = DEFAULT_DB_FILE) -> sqlite3.Connection:
    connection = sqlite3.connect(database)
    connection.row_factory = sqlite3.Row
    return connection


def sqlite_integrity(connection: sqlite3.Connection) -> str:
    row = connection.execute("PRAGMA integrity_check").fetchone()
    return str(row[0])


def count_total_rows(connection: sqlite3.Connection) -> int:
    row = connection.execute(
        "SELECT COUNT(*) AS count FROM knowledge_objects"
    ).fetchone()
    return int(row["count"])


def count_rows_with_doi(connection: sqlite3.Connection) -> int:
    row = connection.execute(
        """
        SELECT COUNT(*) AS count
        FROM knowledge_objects
        WHERE TRIM(COALESCE(doi, '')) <> ''
        """
    ).fetchone()
    return int(row["count"])


def count_unique_normalized_dois(
    connection: sqlite3.Connection,
) -> int:
    rows = connection.execute(
        """
        SELECT doi
        FROM knowledge_objects
        WHERE TRIM(COALESCE(doi, '')) <> ''
        """
    ).fetchall()

    values = {
        knowledge_repository.normalize_doi(row["doi"])
        for row in rows
        if knowledge_repository.normalize_doi(row["doi"])
    }

    return len(values)


def count_duplicate_doi_groups(
    connection: sqlite3.Connection,
) -> int:
    rows = connection.execute(
        """
        SELECT id, doi
        FROM knowledge_objects
        WHERE TRIM(COALESCE(doi, '')) <> ''
        """
    ).fetchall()

    counts: Dict[str, int] = {}

    for row in rows:
        normalized = knowledge_repository.normalize_doi(row["doi"])

        if normalized:
            counts[normalized] = counts.get(normalized, 0) + 1

    return sum(1 for value in counts.values() if value > 1)


def count_duplicate_title_groups_without_doi(
    connection: sqlite3.Connection,
) -> int:
    rows = connection.execute(
        """
        SELECT title
        FROM knowledge_objects
        WHERE TRIM(COALESCE(doi, '')) = ''
        """
    ).fetchall()

    counts: Dict[str, int] = {}

    for row in rows:
        normalized = knowledge_repository.normalize_title(row["title"])

        if normalized:
            counts[normalized] = counts.get(normalized, 0) + 1

    return sum(1 for value in counts.values() if value > 1)


def lifecycle_distribution(
    connection: sqlite3.Connection,
) -> Dict[str, int]:
    rows = connection.execute(
        """
        SELECT LOWER(TRIM(COALESCE(status, ''))) AS status_value,
               COUNT(*) AS count
        FROM knowledge_objects
        GROUP BY LOWER(TRIM(COALESCE(status, '')))
        ORDER BY status_value
        """
    ).fetchall()

    result: Dict[str, int] = {}

    for row in rows:
        status = row["status_value"] or "missing"
        result[str(status)] = int(row["count"])

    return result


def count_unknown_statuses(
    lifecycle_counts: Dict[str, int],
) -> int:
    return sum(
        count
        for status, count in lifecycle_counts.items()
        if status not in RECOGNISED_STATUSES
    )


def count_missing_text(
    connection: sqlite3.Connection,
    column: str,
) -> int:
    allowed_columns = {
        "title",
        "abstract",
        "publication_year",
        "pdf_link",
        "local_file",
    }

    if column not in allowed_columns:
        raise ValueError(f"Unsupported text column: {column}")

    row = connection.execute(
        f"""
        SELECT COUNT(*) AS count
        FROM knowledge_objects
        WHERE TRIM(COALESCE({column}, '')) = ''
        """
    ).fetchone()

    return int(row["count"])


def count_missing_json_array(
    connection: sqlite3.Connection,
    column: str,
) -> int:
    allowed_columns = {"authors", "keywords"}

    if column not in allowed_columns:
        raise ValueError(f"Unsupported JSON column: {column}")

    rows = connection.execute(
        f"SELECT {column} FROM knowledge_objects"
    ).fetchall()

    missing = 0

    for row in rows:
        value = row[column]

        if not value:
            missing += 1
            continue

        try:
            parsed = json.loads(value)
        except (json.JSONDecodeError, TypeError):
            missing += 1
            continue

        if not isinstance(parsed, list) or not parsed:
            missing += 1

    return missing


def list_indexes(connection: sqlite3.Connection) -> List[str]:
    rows = connection.execute(
        "PRAGMA index_list(knowledge_objects)"
    ).fetchall()

    return sorted(str(row["name"]) for row in rows)


def determine_overall_status(
    *,
    integrity: str,
    duplicate_doi_groups: int,
    duplicate_title_groups_without_doi: int,
    missing_expected_indexes: List[str],
) -> str:
    if integrity.lower() != "ok":
        return "CRITICAL"

    if duplicate_doi_groups > 0:
        return "CRITICAL"

    if duplicate_title_groups_without_doi > 0:
        return "WARNING"

    if missing_expected_indexes:
        return "WARNING"

    return "HEALTHY"


def build_health_report(
    database: Path = DEFAULT_DB_FILE,
) -> RepositoryHealthReport:
    connection = connect(database)

    try:
        integrity = sqlite_integrity(connection)
        total_rows = count_total_rows(connection)
        rows_with_doi = count_rows_with_doi(connection)
        lifecycle_counts = lifecycle_distribution(connection)
        indexes_present = list_indexes(connection)

        duplicate_doi_groups = count_duplicate_doi_groups(connection)
        duplicate_title_groups = (
            count_duplicate_title_groups_without_doi(connection)
        )

        missing_expected_indexes = sorted(
            EXPECTED_INDEXES.difference(indexes_present)
        )

        overall_status = determine_overall_status(
            integrity=integrity,
            duplicate_doi_groups=duplicate_doi_groups,
            duplicate_title_groups_without_doi=duplicate_title_groups,
            missing_expected_indexes=missing_expected_indexes,
        )

        return RepositoryHealthReport(
            database=str(database),
            sqlite_integrity=integrity,
            total_rows=total_rows,
            rows_with_doi=rows_with_doi,
            rows_without_doi=total_rows - rows_with_doi,
            unique_normalized_dois=count_unique_normalized_dois(
                connection
            ),
            duplicate_doi_groups=duplicate_doi_groups,
            duplicate_title_groups_without_doi=duplicate_title_groups,
            lifecycle_counts=lifecycle_counts,
            unknown_status_count=count_unknown_statuses(
                lifecycle_counts
            ),
            missing_title_count=count_missing_text(
                connection,
                "title",
            ),
            missing_abstract_count=count_missing_text(
                connection,
                "abstract",
            ),
            missing_authors_count=count_missing_json_array(
                connection,
                "authors",
            ),
            missing_keywords_count=count_missing_json_array(
                connection,
                "keywords",
            ),
            missing_publication_year_count=count_missing_text(
                connection,
                "publication_year",
            ),
            missing_pdf_link_count=count_missing_text(
                connection,
                "pdf_link",
            ),
            missing_local_file_count=count_missing_text(
                connection,
                "local_file",
            ),
            indexes_present=indexes_present,
            missing_expected_indexes=missing_expected_indexes,
            overall_status=overall_status,
        )
    finally:
        connection.close()


def print_health_report(report: RepositoryHealthReport) -> None:
    print("=" * 72)
    print("AROS REPOSITORY HEALTH")
    print("=" * 72)

    print()
    print("Repository")
    print("----------")
    print(f"Database                         : {report.database}")
    print(f"SQLite integrity                 : {report.sqlite_integrity}")
    print(f"Overall status                   : {report.overall_status}")

    print()
    print("Identity")
    print("--------")
    print(f"Total rows                       : {report.total_rows}")
    print(f"Rows with DOI                    : {report.rows_with_doi}")
    print(f"Rows without DOI                 : {report.rows_without_doi}")
    print(
        "Unique normalized DOIs           : "
        f"{report.unique_normalized_dois}"
    )
    print(
        "Duplicate DOI groups             : "
        f"{report.duplicate_doi_groups}"
    )
    print(
        "Duplicate title groups (no DOI)  : "
        f"{report.duplicate_title_groups_without_doi}"
    )

    print()
    print("Lifecycle")
    print("---------")

    for status, count in sorted(report.lifecycle_counts.items()):
        print(f"{status:32}: {count}")

    print(f"{'unknown or missing statuses':32}: {report.unknown_status_count}")

    print()
    print("Metadata Quality")
    print("----------------")
    print(f"Missing title                    : {report.missing_title_count}")
    print(
        f"Missing abstract                 : "
        f"{report.missing_abstract_count}"
    )
    print(
        f"Missing authors                  : "
        f"{report.missing_authors_count}"
    )
    print(
        f"Missing keywords                 : "
        f"{report.missing_keywords_count}"
    )
    print(
        f"Missing publication year         : "
        f"{report.missing_publication_year_count}"
    )
    print(
        f"Missing PDF link                 : "
        f"{report.missing_pdf_link_count}"
    )
    print(
        f"Missing local file               : "
        f"{report.missing_local_file_count}"
    )

    print()
    print("Indexes")
    print("-------")

    for index_name in report.indexes_present:
        print(f"Present: {index_name}")

    if report.missing_expected_indexes:
        for index_name in report.missing_expected_indexes:
            print(f"Missing: {index_name}")
    else:
        print("All expected repository indexes are present.")

    print()
    if report.overall_status == "HEALTHY":
        print("✓ Repository integrity and identity checks passed.")
    elif report.overall_status == "WARNING":
        print("⚠ Repository is operational but requires attention.")
    else:
        print("✗ Repository integrity requires immediate attention.")


def write_json_report(
    report: RepositoryHealthReport,
    output_file: Path,
) -> None:
    output_file.write_text(
        json.dumps(
            asdict(report),
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate an AROS repository health report."
    )
    parser.add_argument(
        "--database",
        type=Path,
        default=DEFAULT_DB_FILE,
    )
    parser.add_argument(
    "--json-report",
        type=Path,
        default=None,
    )

    return parser.parse_args()


def main() -> None:
    arguments = parse_arguments()
    report = build_health_report(arguments.database)
    print_health_report(report)

    if arguments.json_report:
        write_json_report(report, arguments.json_report)
        print()
        print(f"JSON report: {arguments.json_report}")


if __name__ == "__main__":
    main()
