import tempfile
import unittest
from pathlib import Path

from knowledge.knowledge_object import KnowledgeObject
from repository import knowledge_repository


class TestKnowledgeRepository(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.original_db_file = knowledge_repository.DB_FILE

        knowledge_repository.DB_FILE = (
            Path(self.temp_dir.name) / "test_repository.db"
        )
        knowledge_repository.initialize_database()

    def tearDown(self) -> None:
        knowledge_repository.DB_FILE = self.original_db_file
        self.temp_dir.cleanup()

    @staticmethod
    def make_object(
        title: str = "Debt Management in Power Utilities",
        doi: str = "10.1000/example",
    ) -> KnowledgeObject:
        return KnowledgeObject(
            title=title,
            source="OpenAlex",
            source_type="Academic API",
            document_type="Journal Article",
            research_domain="Corporate Finance",
            authors=["Example Author"],
            publication_year="2025",
            doi=doi,
            abstract="Repository duplicate-detection test.",
            keywords=["debt management", "power utilities"],
            status="discovered",
            confidence=0.90,
        )

    def test_normalize_doi(self) -> None:
        self.assertEqual(
            knowledge_repository.normalize_doi(
                " HTTPS://DOI.ORG/10.1000/Example "
            ),
            "10.1000/example",
        )

    def test_duplicate_doi_returns_existing_id(self) -> None:
        first = self.make_object(
            doi="https://doi.org/10.1000/Example"
        )
        second = self.make_object(
            title="A Different Metadata Title",
            doi="10.1000/example",
        )

        first_id = knowledge_repository.save_knowledge_object(first)
        second_id = knowledge_repository.save_knowledge_object(second)

        self.assertEqual(first_id, second_id)
        self.assertEqual(
            knowledge_repository.count_knowledge_objects(),
            1,
        )

    def test_title_duplicate_when_doi_missing(self) -> None:
        first = self.make_object(
            title="  Debt   Management in Power Utilities  ",
            doi="",
        )
        second = self.make_object(
            title="Debt Management in Power Utilities",
            doi="",
        )

        first_id = knowledge_repository.save_knowledge_object(first)
        second_id = knowledge_repository.save_knowledge_object(second)

        self.assertEqual(first_id, second_id)
        self.assertEqual(
            knowledge_repository.count_knowledge_objects(),
            1,
        )

    def test_distinct_dois_are_inserted(self) -> None:
        first = self.make_object(doi="10.1000/first")
        second = self.make_object(doi="10.1000/second")

        first_id = knowledge_repository.save_knowledge_object(first)
        second_id = knowledge_repository.save_knowledge_object(second)

        self.assertNotEqual(first_id, second_id)
        self.assertEqual(
            knowledge_repository.count_knowledge_objects(),
            2,
        )

    def test_add_function_remains_compatible(self) -> None:
        item = self.make_object()

        record_id = knowledge_repository.add_knowledge_object(item)

        self.assertIsInstance(record_id, int)
        self.assertEqual(
            knowledge_repository.count_knowledge_objects(),
            1,
        )


if __name__ == "__main__":
    unittest.main()
