import unittest

from mappers.openalex_mapper import (
    extract_pdf_link,
    map_openalex_record,
    reconstruct_abstract,
)


SAMPLE_RECORD = {
    "id": "https://openalex.org/W123456789",
    "doi": "https://doi.org/10.1000/example",
    "title": "Debt Management in Power Utilities",
    "type": "article",
    "publication_year": 2025,
    "publication_date": "2025-03-10",
    "language": "en",
    "abstract_inverted_index": {
        "Debt": [0],
        "management": [1],
        "improves": [2],
        "performance": [3],
    },
    "authorships": [
        {
            "author": {
                "display_name": "Author One"
            }
        },
        {
            "author": {
                "display_name": "Author Two"
            }
        },
    ],
    "keywords": [
        {"display_name": "Debt Management"},
        {"display_name": "Corporate Finance"},
    ],
    "topics": [
        {"display_name": "Power Sector Finance"}
    ],
    "open_access": {
        "is_oa": True,
        "oa_status": "gold",
    },
    "best_oa_location": {
        "pdf_url": "https://example.org/article.pdf",
        "landing_page_url": "https://example.org/article",
    },
    "primary_location": {
        "source": {
            "display_name": "Journal of Finance",
            "issn_l": "1234-5678",
            "issn": ["1234-5678"],
            "host_organization_name": "Example Publisher",
        }
    },
    "ids": {
        "openalex": "https://openalex.org/W123456789",
        "doi": "https://doi.org/10.1000/example",
    },
    "cited_by_count": 25,
    "referenced_works_count": 40,
    "is_retracted": False,
    "has_fulltext": True,
}


class TestOpenAlexMapper(unittest.TestCase):
    def test_reconstruct_abstract(self) -> None:
        abstract = reconstruct_abstract(
            SAMPLE_RECORD["abstract_inverted_index"]
        )

        self.assertEqual(
            abstract,
            "Debt management improves performance",
        )

    def test_extract_pdf_link(self) -> None:
        self.assertEqual(
            extract_pdf_link(SAMPLE_RECORD),
            "https://example.org/article.pdf",
        )

    def test_map_openalex_record(self) -> None:
        obj = map_openalex_record(
            SAMPLE_RECORD,
            research_domain="Corporate Finance",
        )

        self.assertEqual(
            obj.title,
            "Debt Management in Power Utilities",
        )
        self.assertEqual(
            obj.abstract,
            "Debt management improves performance",
        )
        self.assertEqual(len(obj.authors), 2)
        self.assertTrue(obj.open_access)
        self.assertEqual(
            obj.metadata["openalex_id"],
            "https://openalex.org/W123456789",
        )
        self.assertEqual(
            obj.metadata["journal"],
            "Journal of Finance",
        )
        self.assertIn(
            "Power Sector Finance",
            obj.keywords,
        )

    def test_missing_abstract_is_allowed(self) -> None:
        record = dict(SAMPLE_RECORD)
        record["abstract_inverted_index"] = None

        obj = map_openalex_record(record)

        self.assertEqual(obj.abstract, "")


if __name__ == "__main__":
    unittest.main()
