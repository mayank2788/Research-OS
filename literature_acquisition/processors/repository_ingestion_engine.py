import json
import re
from pathlib import Path

from knowledge.knowledge_object import KnowledgeObject
from repository.knowledge_repository import (
    initialize_database,
    add_knowledge_object,
    count_knowledge_objects,
    connect,
)


class RepositoryIngestionEngine:
    """
    AROS Literature Repository Ingestion Engine v1.

    Converts enriched literature Knowledge Objects into the
    existing AROS SQLite repository.

    Duplicate order:
    1. DOI
    2. Normalized title
    """

    def __init__(self):
        self.source_folder = Path("knowledge/objects/literature")

    @staticmethod
    def normalize_title(title):
        value = str(title or "").lower()
        return re.sub(r"[^a-z0-9]+", "", value)

    def load_existing_records(self):
        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT title, doi
            FROM knowledge_objects
        """)

        existing_dois = set()
        existing_titles = set()

        for title, doi in cursor.fetchall():
            normalized_doi = str(doi or "").strip().lower()

            if normalized_doi:
                existing_dois.add(normalized_doi)

            normalized_title = self.normalize_title(title)

            if normalized_title:
                existing_titles.add(normalized_title)

        conn.close()

        return existing_dois, existing_titles

    @staticmethod
    def build_keywords(research_intelligence):
        keywords = []

        for field in [
            "detected_methods",
            "detected_models",
            "detected_variables",
        ]:
            values = research_intelligence.get(field, [])

            if isinstance(values, list):
                keywords.extend(str(value) for value in values if value)

        return sorted(set(keywords))

    def convert_object(self, data):
        metadata = data.get("metadata", {})
        intelligence = data.get("research_intelligence", {})
        source = data.get("source", {})

        title = metadata.get("title", "").strip()

        if not title:
            return None

        return KnowledgeObject(
            title=title,
            source=source.get("origin", "") or "AROS Literature Acquisition",
            source_type="Academic Literature Connector",
            document_type="Journal Article",
            research_domain=metadata.get("domain", ""),
            authors=metadata.get("authors", []),
            publication_year=str(metadata.get("year", "") or ""),
            doi=str(metadata.get("doi", "") or ""),
            abstract=intelligence.get("abstract", "") or "",
            keywords=self.build_keywords(intelligence),
            pdf_link=source.get("resolved_pdf_url", "") or "",
            open_access=True,
            local_file=source.get("pdf_path", "") or "",
            ai_summary="",
            status="enriched",
            confidence=0.70,
        )

    def run(self):
        initialize_database()

        existing_dois, existing_titles = self.load_existing_records()

        inserted = 0
        duplicate_doi = 0
        duplicate_title = 0
        invalid = 0
        failed = 0

        for file in sorted(self.source_folder.glob("*.json")):
            try:
                data = json.loads(file.read_text(encoding="utf-8"))
                obj = self.convert_object(data)

                if obj is None:
                    invalid += 1
                    continue

                doi_key = str(obj.doi or "").strip().lower()
                title_key = self.normalize_title(obj.title)

                if doi_key and doi_key in existing_dois:
                    duplicate_doi += 1
                    continue

                if title_key and title_key in existing_titles:
                    duplicate_title += 1
                    continue

                add_knowledge_object(obj)

                if doi_key:
                    existing_dois.add(doi_key)

                if title_key:
                    existing_titles.add(title_key)

                inserted += 1

            except Exception as error:
                failed += 1
                print("Failed:", file.name, "-", error)

        return {
            "objects_found": len(list(self.source_folder.glob("*.json"))),
            "inserted": inserted,
            "duplicate_doi": duplicate_doi,
            "duplicate_title": duplicate_title,
            "invalid": invalid,
            "failed": failed,
            "repository_total": count_knowledge_objects(),
        }


if __name__ == "__main__":
    result = RepositoryIngestionEngine().run()

    print("=" * 70)
    print("AROS REPOSITORY INGESTION REPORT")
    print("=" * 70)

    for key, value in result.items():
        print(key, ":", value)

    print()
    print("✓ Literature repository ingestion completed")
