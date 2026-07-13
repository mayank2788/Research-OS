from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class BaseConnector(ABC):
    """
    Common interface for every AROS external connector.

    External connector implementations should inherit from this class.
    """

    def __init__(
        self,
        name: str,
        registry: Any,
        credential_manager: Any,
        execution_manager: Optional[Any] = None,
    ) -> None:
        self.name = name
        self.registry = registry
        self.credential_manager = credential_manager
        self.execution_manager = execution_manager

    @abstractmethod
    def search(self, query: str, **kwargs: Any) -> Any:
        """Search the external source."""

    @abstractmethod
    def lookup(self, identifier: str, **kwargs: Any) -> Any:
        """Retrieve one record by DOI, source ID, or equivalent identifier."""

    def download(self, url: str, **kwargs: Any) -> Any:
        """
        Download an openly accessible resource.

        Connectors that support downloads may override this method.
        """
        raise NotImplementedError(
            f"{self.name} does not implement download()."
        )

    def health(self) -> Dict[str, Any]:
        """Return current connector health information."""
        return self.registry.get_health(self.name)

    def metadata(self) -> Dict[str, Any]:
        """Return non-secret connector configuration."""
        return self.registry.get_connector(self.name)
