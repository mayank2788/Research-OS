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
from mappers.openalex_mapper import map_openalex_record


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

        return [
            map_openalex_record(
                record=item,
                research_domain=query,
                source=self.name,
            )
            for item in data.get("results", [])
        ]
