import tempfile
import unittest
from pathlib import Path

from importers.bibtex_importer import (
    import_bibtex,
    parse_bibtex_text,
    record_to_knowledge_object,
)
from repository import knowledge_repository


SAMPLE_BIBTEX = r"""
@article{Modigliani1958,
  title={The Cost of Capital, Corporation Finance and the Theory of Investment},
  author={Modigliani, Franco and Miller, Merton H.},
  journal={American Economic Review},
  year={1958},
  volume={48},
  number={3},
  pages={261--297},
  doi={https://doi.org/10.0000/CAPITAL.TEST},
  keywords={capital structure; corporate finance},
  url={https://example.org/paper}
}

@article{DuplicateRecord,
  title={The Cost of Capital, Corporation Finance and the Theory of Investment},
  author={Modigliani, Franco and Miller, Merton H.},
  journal={American Economic Review},
  year={1958},
  doi={10.0000/capital.test}
}
"""


class TestBibtexImporter(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.original_db_file = knowledge_repository.DB_FILE

        knowledge_repository.DB_FILE = (
            Path(self.temp_dir.name)
            / "test_bibtex_import.db"
        )

        knowledge_repository.initialize_database()

    def tearDown(self) -> None:
        knowledge_repository.DB_FILE = (
            self.original_db_file
        )
        self.temp_dir.cleanup()

    def test_parse_multiple_entries(self) -> None:
        records = parse_bibtex_text(SAMPLE_BIBTEX)

        self.assertEqual(len(records), 2)
        self.assertEqual(
            records[0]["journal"],
            "American Economic Review",
        )

    def test_convert_record(self) -> None:
        record = parse_bibtex_text(
            SAMPLE_BIBTEX
        )[0]

        obj = record_to_knowledge_object(
            record,
            research_domain="Corporate Finance",
            source="Google Scholar",
        )

        self.assertEqual(
            obj.source,
            "Google Scholar",
        )
        self.assertEqual(
            obj.doi,
            "https://doi.org/10.0000/CAPITAL.TEST",
        )
        self.assertEqual(
            obj.metadata["journal"],
            "American Economic Review",
        )
        self.assertEqual(len(obj.authors), 2)

    def test_import_uses_duplicate_safe_repository(
        self,
    ) -> None:
        bib_file = (
            Path(self.temp_dir.name)
            / "scholar_export.bib"
        )
        bib_file.write_text(
            SAMPLE_BIBTEX,
            encoding="utf-8",
        )

        result = import_bibtex(
            bib_file,
            research_domain="Corporate Finance",
            source="Google Scholar",
        )

        self.assertEqual(
            result["records_found"],
            2,
        )
        self.assertEqual(
            result["records_processed"],
            2,
        )
        self.assertEqual(
            knowledge_repository.count_knowledge_objects(),
            1,
        )
        self.assertEqual(
            result["record_ids"][0],
            result["record_ids"][1],
        )


if __name__ == "__main__":
    unittest.main()
