from typing import Any, Dict, Optional

from connector_framework.base_connector import BaseConnector


class OpenAlexConnector(BaseConnector):
    """
    Production OpenAlex connector for AROS.

    This connector contains only OpenAlex-specific API logic.
    Authentication, retries, rate limiting and HTTP execution
    are delegated to the ConnectorExecutionManager.
    """

    CONNECTOR_NAME = "openalex"

    def __init__(
        self,
        registry,
        credential_manager,
        execution_manager,
    ):
        super().__init__(
            name=self.CONNECTOR_NAME,
            registry=registry,
            credential_manager=credential_manager,
            execution_manager=execution_manager,
        )

    def metadata(self) -> Dict[str, Any]:
        return self.registry.get_connector(self.CONNECTOR_NAME)

    def health(self) -> Dict[str, Any]:
        result = self.execution_manager.request(
            connector_name=self.CONNECTOR_NAME,
            operation="list",
            method="GET",
            endpoint="/works",
            params={
                "per-page": 1
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
        search: str = "",
        filters: Optional[Dict[str, Any]] = None,
        cursor: str = "*",
        per_page: int = 200,
    ) -> Dict[str, Any]:

        params = {
            "search": search,
            "per-page": per_page,
            "cursor": cursor,
        }

        if filters:
            filter_string = ",".join(
                f"{k}:{v}"
                for k, v in filters.items()
            )

            params["filter"] = filter_string

        return self.execution_manager.get_json(
            connector_name=self.CONNECTOR_NAME,
            operation="list",
            endpoint="/works",
            params=params,
        )

    def lookup(self, identifier: str) -> Dict[str, Any]:
        """
        Lookup by OpenAlex Work ID.

        Example:
            https://api.openalex.org/W2741809807
        """

        endpoint = (
            identifier
            if identifier.startswith("/")
            else f"/{identifier}"
        )

        return self.execution_manager.get_json(
            connector_name=self.CONNECTOR_NAME,
            operation="lookup",
            endpoint=endpoint,
        )

    def lookup_doi(
        self,
        doi: str,
    ) -> Dict[str, Any]:
        doi = doi.replace(
            "https://doi.org/",
            "",
        )

        return self.execution_manager.get_json(
            connector_name=self.CONNECTOR_NAME,
            operation="lookup",
            endpoint=f"/works/https://doi.org/{doi}",
        )
