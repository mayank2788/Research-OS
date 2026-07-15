import sqlite3
import tempfile
import unittest
from pathlib import Path

from repository.migrations import canonical_repository_migration
from repository import knowledge_repository


class TestCanonicalRepositoryMigration(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_file = Path(self.temp_dir.name) / "migration_test.db"

        connection = sqlite3.connect(self.db_file)

        connection.execute(
            """
            CREATE TABLE knowledge_objects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                source TEXT,
                source_type TEXT,
                document_type TEXT,
                research_domain TEXT,
                authors TEXT,
                publication_year TEXT,
                doi TEXT,
                abstract TEXT,
                keywords TEXT,
                pdf_link TEXT,
                open_access INTEGER,
                local_file TEXT,
                ai_summary TEXT,
                status TEXT,
                confidence REAL,
                date_added TEXT,
                raw_json TEXT
            )
            """
        )

        rows = [
            (
                "Paper One",
                "https://doi.org/10.1000/example",
            ),
            (
                "Paper One Improved",
                "10.1000/example",
            ),
            (
                "  Title   Without DOI  ",
                "",
            ),
            (
                "Title Without DOI",
                "",
            ),
            (
                "Unique Paper",
                "10.1000/unique",
            ),
        ]

        for title, doi in rows:
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
                    ?, 'Test', 'Test', 'Article', 'Finance',
                    '[]', '2025', ?, '', '[]', '', 0,
                    '', '', 'discovered', 0.5,
                    '2026-01-01T00:00:00', '{}'
                )
                """,
                (title, doi),
            )

        connection.commit()
        connection.close()

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_build_migration_plan(self) -> None:
        plan = canonical_repository_migration.build_migration_plan(
            self.db_file
        )

        self.assertEqual(plan.total_rows_before, 5)
        self.assertEqual(plan.duplicate_group_count, 2)
        self.assertEqual(plan.redundant_row_count, 2)
        self.assertEqual(plan.projected_rows_after, 3)

    def test_oldest_id_is_canonical(self) -> None:
        plan = canonical_repository_migration.build_migration_plan(
            self.db_file
        )

        canonical_ids = [
            group.record_ids[0]
            for group in plan.duplicate_groups
        ]

        self.assertEqual(canonical_ids, [1, 3])

    def test_sqlite_integrity(self) -> None:
        result = (
            canonical_repository_migration.verify_sqlite_integrity(
                self.db_file
            )
        )

        self.assertEqual(result.lower(), "ok")

    def test_normalization_matches_repository(self) -> None:
        self.assertEqual(
            canonical_repository_migration.normalize_doi_for_identity(
                "HTTPS://DOI.ORG/10.1000/Example"
            ),
            knowledge_repository.normalize_doi(
                "HTTPS://DOI.ORG/10.1000/Example"
            ),
        )


if __name__ == "__main__":
    unittest.main()
