import os
import requests

from dotenv import load_dotenv

from connectors.base.base_connector import BaseConnector
from knowledge.knowledge_object import KnowledgeObject


class OpenAlexConnector(BaseConnector):

    def __init__(self):
        super().__init__("OpenAlex")
        load_dotenv()

        self.api_key = os.getenv("OPENALEX_API_KEY")
        self.base_url = "https://api.openalex.org/works"

    def search(self, query, max_results=10):

        params = {
            "search": query,
            "per-page": max_results
        }

        if self.api_key:
            params["api_key"] = self.api_key

        response = requests.get(
            self.base_url,
            params=params,
            timeout=20
        )

        response.raise_for_status()

        data = response.json()

        results = []

        for item in data.get("results", []):

            authors = []

            for author in item.get("authorships", []):
                author_info = author.get("author", {})
                if author_info.get("display_name"):
                    authors.append(author_info["display_name"])

            knowledge = KnowledgeObject(
                title=item.get("title", ""),
                source=self.name,
                source_type="Academic API",
                document_type="Journal Article",
                research_domain=query,
                authors=authors,
                publication_year=str(item.get("publication_year", "")),
                doi=item.get("doi") or "",
                abstract="",
                keywords=[query],
                pdf_link=item.get("primary_location", {}).get("landing_page_url", ""),
                open_access=item.get("open_access", {}).get("is_oa", False),
                confidence=0.80
            )

            results.append(knowledge)

        return results
