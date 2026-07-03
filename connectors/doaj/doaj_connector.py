from urllib.parse import quote
import requests

from connectors.base.base_connector import BaseConnector
from knowledge.knowledge_object import KnowledgeObject


class DOAJConnector(BaseConnector):
    def __init__(self):
        super().__init__("DOAJ")
        self.base_url = "https://doaj.org/api/search/articles"

    def search(self, query, max_results=10):
        safe_query = quote(query)

        try:
            response = requests.get(
                f"{self.base_url}/{safe_query}",
                params={"pageSize": max_results},
                timeout=30,
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as error:
            print(f"DOAJ request failed: {error}")
            return []

        data = response.json()
        results = []

        for item in data.get("results", []):
            bib = item.get("bibjson", {})

            authors = [
                author.get("name", "")
                for author in bib.get("author", [])
                if author.get("name")
            ]

            links = bib.get("link", [])
            pdf_link = ""
            if links:
                pdf_link = links[0].get("url", "")

            knowledge = KnowledgeObject(
                title=bib.get("title", ""),
                source=self.name,
                source_type="Open Access Connector",
                document_type="Journal Article",
                research_domain=query,
                authors=authors,
                publication_year=str(bib.get("year", "")),
                doi="",
                abstract=bib.get("abstract", ""),
                keywords=[query, "open access"],
                pdf_link=pdf_link,
                open_access=True,
                confidence=0.80,
            )

            results.append(knowledge)

        return results
