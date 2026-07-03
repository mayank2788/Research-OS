import json
from pathlib import Path

from connectors.base.base_connector import BaseConnector
from knowledge.knowledge_object import KnowledgeObject


class InstitutionalConnector(BaseConnector):
    """
    Generic Institutional Connector.

    Supports:
    - Regulators
    - Government agencies
    - Professional bodies
    - Multilateral institutions

    Version 1:
    Registry driven discovery foundation.
    """

    def __init__(self, institution):

        super().__init__(institution)

        registry = Path(
            "connectors/institutional/institution_registry.json"
        )

        data = json.loads(registry.read_text())

        self.institution = None

        for item in data["institutions"]:
            if (
                item["short_name"].lower()
                == institution.lower()
            ):
                self.institution = item

        if not self.institution:
            raise ValueError(
                f"Institution not found: {institution}"
            )


    def search(self, query, max_results=10):

        results = []

        knowledge = KnowledgeObject(
            title=f"{query} - {self.institution['name']} Resource",
            source=self.institution["short_name"],
            source_type="Institutional Source",
            document_type="Policy / Report / Regulation",
            research_domain=query,
            authors=[self.institution["name"]],
            publication_year="",
            doi="",
            abstract=(
                f"Research resource discovered from "
                f"{self.institution['name']}"
            ),
            keywords=[
                query,
                self.institution["category"]
            ],
            pdf_link=self.institution["url"],
            open_access=True,
            confidence=0.80,
        )

        results.append(knowledge)

        return results
