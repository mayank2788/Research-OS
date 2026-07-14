from typing import Any, Dict

from connector_framework.base_connector import BaseConnector


class COREConnector(BaseConnector):
    """
    Production CORE API connector for AROS.

    Authentication, retries, rate limiting, and timeouts
    are delegated to the ConnectorExecutionManager.
    """

    CONNECTOR_NAME = "core"

    def __init__(
        self,
        registry: Any,
        credential_manager: Any,
        execution_manager: Any,
    ) -> None:
        super().__init__(
            name=self.CONNECTOR_NAME,
            registry=registry,
            credential_manager=credential_manager,
            execution_manager=execution_manager,
        )

    def health(self) -> Dict[str, Any]:
        result = self.execution_manager.request(
            connector_name=self.CONNECTOR_NAME,
            operation="search",
            method="POST",
            endpoint="/search/works",
            json_body={
                "q": "finance",
                "limit": 1,
            },
        )

        return {
            "healthy": result.status_code == 200,
            "status_code": result.status_code,
            "elapsed_seconds": result.elapsed_seconds,
            "connector": self.CONNECTOR_NAME,
            "rate_limit_remaining": result.rate_limit_remaining,
        }

    def search(
        self,
        query: str,
        limit: int = 10,
        offset: int = 0,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        payload = {
            "q": query,
            "limit": limit,
            "offset": offset,
            **kwargs,
        }

        result = self.execution_manager.request(
            connector_name=self.CONNECTOR_NAME,
            operation="search",
            method="POST",
            endpoint="/search/works",
            json_body=payload,
        )

        return result.response.json()

    def lookup(
        self,
        identifier: str,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        return self.execution_manager.get_json(
            connector_name=self.CONNECTOR_NAME,
            operation="lookup",
            endpoint=f"/works/{identifier}",
        )

    def search_by_doi(
        self,
        doi: str,
        limit: int = 10,
    ) -> Dict[str, Any]:
        clean_doi = doi.replace(
            "https://doi.org/",
            "",
        )

        return self.search(
            query=f'doi:"{clean_doi}"',
            limit=limit,
        )

    def search_by_title(
        self,
        title: str,
        limit: int = 10,
    ) -> Dict[str, Any]:
        return self.search(
            query=f'title:"{title}"',
            limit=limit,
        )
