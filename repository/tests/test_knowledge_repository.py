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


    def test_status_inserted(self) -> None:
        item = self.make_object()

        result = knowledge_repository.save_knowledge_object(
            item,
            return_status=True,
        )

        self.assertEqual(result["status"], "inserted")
        self.assertIsInstance(result["record_id"], int)
        self.assertEqual(
            knowledge_repository.count_knowledge_objects(),
            1,
        )

    def test_status_existing(self) -> None:
        first = self.make_object()
        second = self.make_object()

        first_id = knowledge_repository.save_knowledge_object(first)

        result = knowledge_repository.save_knowledge_object(
            second,
            return_status=True,
        )

        self.assertEqual(result["status"], "existing")
        self.assertEqual(result["record_id"], first_id)
        self.assertEqual(
            knowledge_repository.count_knowledge_objects(),
            1,
        )



    def test_lifecycle_status_advances(self) -> None:
        discovered = self.make_object()
        discovered.status = "discovered"
        discovered.abstract = "Short abstract."

        evaluated = self.make_object()
        evaluated.status = "evaluated"
        evaluated.abstract = (
            "A substantially longer and more informative abstract "
            "for lifecycle merge verification."
        )
        evaluated.ai_summary = "Research evaluation completed."
        evaluated.confidence = 0.95

        first_id = knowledge_repository.save_knowledge_object(discovered)

        result = knowledge_repository.save_knowledge_object(
            evaluated,
            return_status=True,
        )

        record = knowledge_repository.get_knowledge_object_record(first_id)

        self.assertEqual(result["status"], "updated")
        self.assertEqual(result["record_id"], first_id)
        self.assertEqual(record["status"], "evaluated")
        self.assertEqual(record["abstract"], evaluated.abstract)
        self.assertEqual(record["ai_summary"], evaluated.ai_summary)
        self.assertEqual(record["confidence"], 0.95)
        self.assertEqual(
            knowledge_repository.count_knowledge_objects(),
            1,
        )

    def test_lifecycle_status_does_not_regress(self) -> None:
        evaluated = self.make_object()
        evaluated.status = "evaluated"
        evaluated.ai_summary = "Completed evaluation."

        discovered = self.make_object()
        discovered.status = "discovered"
        discovered.ai_summary = ""

        record_id = knowledge_repository.save_knowledge_object(evaluated)

        result = knowledge_repository.save_knowledge_object(
            discovered,
            return_status=True,
        )

        record = knowledge_repository.get_knowledge_object_record(record_id)

        self.assertIn(result["status"], {"existing", "updated"})
        self.assertEqual(record["status"], "evaluated")
        self.assertEqual(record["ai_summary"], "Completed evaluation.")
        self.assertEqual(
            knowledge_repository.count_knowledge_objects(),
            1,
        )

    def test_metadata_merge_rules(self) -> None:
        original = self.make_object()
        original.authors = ["Author One"]
        original.keywords = ["debt"]
        original.abstract = "Short."
        original.pdf_link = ""
        original.local_file = ""
        original.open_access = False
        original.confidence = 0.60

        improved = self.make_object()
        improved.authors = ["Author One", "Author Two"]
        improved.keywords = ["debt", "finance"]
        improved.abstract = "A longer and more useful abstract."
        improved.pdf_link = "https://example.org/paper.pdf"
        improved.local_file = "/tmp/paper.pdf"
        improved.open_access = True
        improved.confidence = 0.90
        improved.status = "enriched"

        record_id = knowledge_repository.save_knowledge_object(original)

        result = knowledge_repository.save_knowledge_object(
            improved,
            return_status=True,
        )

        record = knowledge_repository.get_knowledge_object_record(record_id)

        self.assertEqual(result["status"], "updated")
        self.assertEqual(
            record["authors"],
            ["Author One", "Author Two"],
        )
        self.assertEqual(record["keywords"], ["debt", "finance"])
        self.assertEqual(record["abstract"], improved.abstract)
        self.assertEqual(record["pdf_link"], improved.pdf_link)
        self.assertEqual(record["local_file"], improved.local_file)
        self.assertTrue(record["open_access"])
        self.assertEqual(record["confidence"], 0.90)
        self.assertEqual(record["status"], "enriched")



if __name__ == "__main__":
    unittest.main()
