import requests

from connectors.base.base_connector import BaseConnector
from knowledge.knowledge_object import KnowledgeObject


class SemanticScholarConnector(BaseConnector):
    """
    Semantic Scholar Academic Connector.

    Purpose:
    - Discover academic papers
    - Capture citation-related metadata
    - Convert results into AROS Knowledge Objects
    """

    def __init__(self):
        super().__init__("Semantic Scholar")
        self.base_url = "https://api.semanticscholar.org/graph/v1/paper/search"

    def search(self, query, max_results=10):
        params = {
            "query": query,
            "limit": max_results,
            "fields": "title,abstract,year,authors,citationCount,url,openAccessPdf,externalIds"
        }

        try:
            response = requests.get(
                self.base_url,
                params=params,
                timeout=30,
            )
            response.raise_for_status()

        except requests.exceptions.RequestException as error:
            print(f"Semantic Scholar request failed: {error}")
            return []

        data = response.json()
        results = []

        for item in data.get("data", []):
            authors = [
                author.get("name", "")
                for author in item.get("authors", [])
                if author.get("name")
            ]

            external_ids = item.get("externalIds") or {}
            doi = external_ids.get("DOI", "")

            open_pdf = item.get("openAccessPdf") or {}
            pdf_link = open_pdf.get("url") or item.get("url", "")

            citation_count = item.get("citationCount", 0)

            knowledge = KnowledgeObject(
                title=item.get("title", ""),
                source=self.name,
                source_type="Academic Citation Connector",
                document_type="Journal Article",
                research_domain=query,
                authors=authors,
                publication_year=str(item.get("year") or ""),
                doi=doi,
                abstract=item.get("abstract") or "",
                keywords=[query, f"citations:{citation_count}"],
                pdf_link=pdf_link,
                open_access=True if open_pdf.get("url") else False,
                ai_summary=f"Semantic Scholar citation count: {citation_count}",
                confidence=0.80,
            )

            results.append(knowledge)

        return results
