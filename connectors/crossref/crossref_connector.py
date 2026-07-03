import requests

from connectors.base.base_connector import BaseConnector
from knowledge.knowledge_object import KnowledgeObject


class CrossrefConnector(BaseConnector):
    """
    Crossref Academic Connector.

    Purpose:
    - Discover academic papers
    - Retrieve DOI metadata
    - Convert results into AROS Knowledge Objects
    """

    def __init__(self):
        super().__init__("Crossref")

        self.base_url = "https://api.crossref.org/works"


    def search(self, query, max_results=10):

        params = {
            "query": query,
            "rows": max_results,
        }

        headers = {
            "User-Agent": "AROS Research OS (mailto:research@example.com)"
        }

        try:
            response = requests.get(
                self.base_url,
                params=params,
                headers=headers,
                timeout=40,
            )

            response.raise_for_status()

        except requests.exceptions.RequestException as error:
            print(f"Crossref request failed: {error}")
            return []

        data = response.json()

        results = []

        for item in data.get("message", {}).get("items", []):

            title = ""

            if item.get("title"):
                title = item["title"][0]


            authors = []

            for author in item.get("author", []):

                name = " ".join([
                    author.get("given", ""),
                    author.get("family", "")
                ]).strip()

                if name:
                    authors.append(name)


            year = ""

            try:
                year = str(
                    item["published-print"]["date-parts"][0][0]
                )
            except Exception:
                pass


            knowledge = KnowledgeObject(
                title=title,
                source=self.name,
                source_type="Academic Metadata Connector",
                document_type=item.get("type", "Journal Article"),
                research_domain=query,
                authors=authors,
                publication_year=year,
                doi=item.get("DOI", ""),
                abstract=item.get("abstract", ""),
                keywords=[query],
                pdf_link=item.get("URL", ""),
                open_access=False,
                confidence=0.80,
            )

            results.append(knowledge)

        return results
