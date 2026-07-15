import sqlite3
import tempfile
import unittest
from pathlib import Path

from repository.migrations.apply_canonical_migration import (
    apply_migration,
)
from repository import knowledge_repository


class TestApplyCanonicalMigration(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_file = Path(self.temp_dir.name) / "test.db"
        self.report_file = Path(self.temp_dir.name) / "report.json"

        original_db = knowledge_repository.DB_FILE
        knowledge_repository.DB_FILE = self.db_file

        try:
            knowledge_repository.initialize_database()
        finally:
            knowledge_repository.DB_FILE = original_db

        connection = sqlite3.connect(self.db_file)

        common = (
            "OpenAlex",
            "Academic API",
            "Journal Article",
            "Finance",
            '["Author"]',
            "2025",
            "Short abstract",
            '["finance"]',
            "",
            0,
            "",
            "",
            "discovered",
            0.5,
            "2026-01-01T00:00:00",
            "{}",
        )

        connection.execute(
            """
            INSERT INTO knowledge_objects (
                title, source, source_type, document_type,
                research_domain, authors, publication_year,
                doi, abstract, keywords, pdf_link, open_access,
                local_file, ai_summary, status, confidence,
                date_added, raw_json
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            ("Paper",) + common[:6]
            + ("https://doi.org/10.1000/test",)
            + common[6:],
        )

        connection.execute(
            """
            INSERT INTO knowledge_objects (
                title, source, source_type, document_type,
                research_domain, authors, publication_year,
                doi, abstract, keywords, pdf_link, open_access,
                local_file, ai_summary, status, confidence,
                date_added, raw_json
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            ("Paper Improved",) + common[:6]
            + ("10.1000/test",)
            + common[6:],
        )

        connection.commit()
        connection.close()

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_apply_migration(self) -> None:
        result = apply_migration(
            self.db_file,
            self.report_file,
        )

        self.assertEqual(result["rows_before"], 2)
        self.assertEqual(result["rows_after"], 1)
        self.assertEqual(result["redundant_rows_deleted"], 1)
        self.assertEqual(
            result["sqlite_integrity_after"].lower(),
            "ok",
        )
        self.assertTrue(self.report_file.exists())

        connection = sqlite3.connect(self.db_file)

        try:
            count = connection.execute(
                "SELECT COUNT(*) FROM knowledge_objects"
            ).fetchone()[0]

            self.assertEqual(count, 1)

            with self.assertRaises(sqlite3.IntegrityError):
                connection.execute(
                    """
                    INSERT INTO knowledge_objects (
                        title, doi
                    )
                    VALUES (?, ?)
                    """,
                    ("Another duplicate", "10.1000/test"),
                )
        finally:
            connection.close()


if __name__ == "__main__":
    unittest.main()
