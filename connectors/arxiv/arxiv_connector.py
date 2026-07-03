import requests
import xml.etree.ElementTree as ET

from connectors.base.base_connector import BaseConnector
from knowledge.knowledge_object import KnowledgeObject


class ArxivConnector(BaseConnector):
    def __init__(self):
        super().__init__("arXiv")
        self.base_url = "https://export.arxiv.org/api/query"

    def search(self, query, max_results=10):
        try:
            response = requests.get(
                self.base_url,
                params={
                    "search_query": f"all:{query}",
                    "start": 0,
                    "max_results": max_results,
                },
                timeout=30,
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as error:
            print(f"arXiv request failed: {error}")
            return []

        try:
            root = ET.fromstring(response.text)
        except ET.ParseError as error:
            print(f"arXiv XML parse failed: {error}")
            return []

        ns = {"atom": "http://www.w3.org/2005/Atom"}
        results = []

        for entry in root.findall("atom:entry", ns):
            title_node = entry.find("atom:title", ns)
            summary_node = entry.find("atom:summary", ns)
            published_node = entry.find("atom:published", ns)
            id_node = entry.find("atom:id", ns)

            title = title_node.text.strip() if title_node is not None and title_node.text else ""
            abstract = summary_node.text.strip() if summary_node is not None and summary_node.text else ""
            published = published_node.text if published_node is not None and published_node.text else ""
            year = published[:4] if published else ""
            link = id_node.text if id_node is not None and id_node.text else ""
            if "arxiv.org/abs/" in link:
                link = link.replace("arxiv.org/abs/", "arxiv.org/pdf/") + ".pdf"

            authors = []
            for author in entry.findall("atom:author", ns):
                name = author.find("atom:name", ns)
                if name is not None and name.text:
                    authors.append(name.text)

            knowledge = KnowledgeObject(
                title=title,
                source=self.name,
                source_type="Preprint Connector",
                document_type="Preprint",
                research_domain=query,
                authors=authors,
                publication_year=year,
                doi="",
                abstract=abstract,
                keywords=[query, "preprint"],
                pdf_link=link,
                open_access=True,
                confidence=0.80,
            )

            results.append(knowledge)

        return results
