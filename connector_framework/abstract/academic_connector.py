from abc import ABC, abstractmethod

from connector_framework.base_connector import BaseConnector


class AbstractAcademicConnector(BaseConnector, ABC):
    """
    Common functionality shared by all academic literature connectors.
    """

    DEFAULT_PER_PAGE = 200

    @abstractmethod
    def provider_name(self):
        """Return connector/provider name."""
        raise NotImplementedError

    @abstractmethod
    def build_search_endpoint(self):
        raise NotImplementedError

    @abstractmethod
    def build_lookup_endpoint(self, identifier):
        raise NotImplementedError

    def health(self):
        return self.execution_manager.request(
            connector_name=self.provider_name(),
            operation="health",
            method="GET",
            endpoint=self.build_search_endpoint(),
            params={"per-page": 1},
        )

    def search(
        self,
        search="",
        filters=None,
        cursor="*",
        per_page=None,
    ):
        if per_page is None:
            per_page = self.DEFAULT_PER_PAGE

        params = {
            "search": search,
            "cursor": cursor,
            "per-page": per_page,
        }

        if filters:
            params["filter"] = ",".join(
                f"{k}:{v}" for k, v in filters.items()
            )

        return self.execution_manager.get_json(
            connector_name=self.provider_name(),
            operation="search",
            endpoint=self.build_search_endpoint(),
            params=params,
        )

    def lookup(self, identifier):
        return self.execution_manager.get_json(
            connector_name=self.provider_name(),
            operation="lookup",
            endpoint=self.build_lookup_endpoint(identifier),
        )
