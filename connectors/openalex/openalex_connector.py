from typing import List

from connector_framework.connector_registry import ConnectorRegistry
from connector_framework.credential_manager import (
    ConnectorCredentialManager,
)
from connector_framework.execution_manager import (
    ConnectorExecutionManager,
)
from connectors.base.base_connector import BaseConnector
from knowledge.knowledge_object import KnowledgeObject


class OpenAlexConnector(BaseConnector):
    """
    AROS OpenAlex provider connector.

    Compatibility:
    - Preserves the original no-argument constructor.
    - Preserves search(query, max_results).
    - Continues returning KnowledgeObject instances.

    Infrastructure:
    - Credentials are loaded by ConnectorCredentialManager.
    - HTTP requests pass through ConnectorExecutionManager.
    - Rate limiting, retries and timeouts are centrally managed.
    """

    CONNECTOR_ID = "openalex"

    def __init__(self) -> None:
        super().__init__("OpenAlex")

        self.registry = ConnectorRegistry()
        self.credential_manager = ConnectorCredentialManager(
            self.registry
        )
        self.execution_manager = ConnectorExecutionManager(
            registry=self.registry,
            credential_manager=self.credential_manager,
        )

    @staticmethod
    def _authors(item: dict) -> List[str]:
        authors = []

        for authorship in item.get("authorships", []):
            author = authorship.get("author") or {}
            display_name = author.get("display_name")

            if display_name:
                authors.append(display_name)

        return authors

    @staticmethod
    def _pdf_link(item: dict) -> str:
        locations = [
            item.get("best_oa_location") or {},
            item.get("primary_location") or {},
        ]

        locations.extend(item.get("locations") or [])

        for location in locations:
            pdf_url = location.get("pdf_url")

            if pdf_url:
                return pdf_url

        for location in locations:
            landing_url = location.get("landing_page_url")

            if landing_url:
                return landing_url

        return ""

    @staticmethod
    def _topic_keywords(item: dict, query: str) -> List[str]:
        keywords = [query]

        for topic in item.get("topics", [])[:3]:
            display_name = topic.get("display_name")

            if display_name:
                keywords.append(display_name)

        return list(dict.fromkeys(keywords))

    def health(self) -> dict:
        result = self.execution_manager.request(
            connector_name=self.CONNECTOR_ID,
            operation="list",
            method="GET",
            endpoint="/works",
            params={"per-page": 1},
        )

        return {
            "healthy": result.status_code == 200,
            "status_code": result.status_code,
            "elapsed_seconds": result.elapsed_seconds,
            "rate_limit_remaining": result.rate_limit_remaining,
        }

    def search(
        self,
        query: str,
        max_results: int = 10,
    ) -> List[KnowledgeObject]:
        if not query or not query.strip():
            raise ValueError("OpenAlex search query cannot be empty.")

        if max_results < 1:
            raise ValueError("max_results must be at least 1.")

        page_size = min(max_results, 100)

        data = self.execution_manager.get_json(
            connector_name=self.CONNECTOR_ID,
            operation="list",
            endpoint="/works",
            params={
                "search": query.strip(),
                "per-page": page_size,
            },
        )

        results = []

        for item in data.get("results", []):
            open_access = item.get("open_access") or {}

            knowledge = KnowledgeObject(
                title=item.get("title") or "",
                source=self.name,
                source_type="Academic API",
                document_type=item.get("type") or "Journal Article",
                research_domain=query,
                authors=self._authors(item),
                publication_year=str(
                    item.get("publication_year") or ""
                ),
                doi=item.get("doi") or "",
                abstract="",
                keywords=self._topic_keywords(item, query),
                pdf_link=self._pdf_link(item),
                open_access=bool(
                    open_access.get("is_oa", False)
                ),
                status="discovered",
                confidence=0.85,
            )

            results.append(knowledge)

        return results
