import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

from repository.repository_health import (
    build_health_report,
    determine_overall_status,
)
from repository import knowledge_repository


class TestRepositoryHealth(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_file = Path(self.temp_dir.name) / "health_test.db"

        original_db = knowledge_repository.DB_FILE
        knowledge_repository.DB_FILE = self.db_file

        try:
            knowledge_repository.initialize_database()
        finally:
            knowledge_repository.DB_FILE = original_db

        connection = sqlite3.connect(self.db_file)

        connection.execute(
            """
            INSERT INTO knowledge_objects (
                title,
                source,
                source_type,
                document_type,
                research_domain,
                authors,
                publication_year,
                doi,
                abstract,
                keywords,
                pdf_link,
                open_access,
                local_file,
                ai_summary,
                status,
                confidence,
                date_added,
                raw_json
            )
            VALUES (
                'Paper One',
                'Test',
                'Academic API',
                'Journal Article',
                'Finance',
                '["Author One"]',
                '2025',
                '10.1000/one',
                'Abstract',
                '["finance"]',
                'https://example.org/paper.pdf',
                1,
                '/tmp/paper.pdf',
                '',
                'evaluated',
                0.9,
                '2026-01-01T00:00:00',
                '{}'
            )
            """
        )

        connection.execute(
            """
            CREATE UNIQUE INDEX
            ux_knowledge_objects_normalized_doi
            ON knowledge_objects (
                LOWER(TRIM(doi))
            )
            WHERE TRIM(COALESCE(doi, '')) <> ''
            """
        )

        connection.execute(
            """
            CREATE INDEX
            ix_knowledge_objects_normalized_title
            ON knowledge_objects (LOWER(TRIM(title)))
            """
        )

        connection.commit()
        connection.close()

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_build_healthy_report(self) -> None:
        report = build_health_report(self.db_file)

        self.assertEqual(report.sqlite_integrity.lower(), "ok")
        self.assertEqual(report.total_rows, 1)
        self.assertEqual(report.rows_with_doi, 1)
        self.assertEqual(report.rows_without_doi, 0)
        self.assertEqual(report.duplicate_doi_groups, 0)
        self.assertEqual(
            report.duplicate_title_groups_without_doi,
            0,
        )
        self.assertEqual(report.lifecycle_counts["evaluated"], 1)
        self.assertEqual(report.unknown_status_count, 0)
        self.assertEqual(report.overall_status, "HEALTHY")

    def test_missing_indexes_gives_warning(self) -> None:
        self.assertEqual(
            determine_overall_status(
                integrity="ok",
                duplicate_doi_groups=0,
                duplicate_title_groups_without_doi=0,
                missing_expected_indexes=["missing_index"],
            ),
            "WARNING",
        )

    def test_duplicate_doi_gives_critical(self) -> None:
        self.assertEqual(
            determine_overall_status(
                integrity="ok",
                duplicate_doi_groups=1,
                duplicate_title_groups_without_doi=0,
                missing_expected_indexes=[],
            ),
            "CRITICAL",
        )

    def test_sqlite_failure_gives_critical(self) -> None:
        self.assertEqual(
            determine_overall_status(
                integrity="database disk image is malformed",
                duplicate_doi_groups=0,
                duplicate_title_groups_without_doi=0,
                missing_expected_indexes=[],
            ),
            "CRITICAL",
        )


if __name__ == "__main__":
    unittest.main()
