import unittest

from connector_framework.connector_registry import ConnectorRegistry
from connector_framework.credential_manager import ConnectorCredentialManager
from connector_framework.execution_manager import ConnectorExecutionManager


class TestConnectorFoundation(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = ConnectorRegistry()
        self.credentials = ConnectorCredentialManager(self.registry)
        self.execution = ConnectorExecutionManager(
            self.registry,
            self.credentials,
        )

    def test_registry_contains_expected_connectors(self) -> None:
        connectors = self.registry.list_connectors()

        expected = {
            "core",
            "crossref",
            "openaire",
            "openalex",
            "semantic_scholar",
        }

        self.assertTrue(
            expected.issubset(set(connectors)),
            f"Missing connectors: {expected - set(connectors)}",
        )

    def test_core_components_initialize(self) -> None:
        self.assertIsNotNone(self.registry)
        self.assertIsNotNone(self.credentials)
        self.assertIsNotNone(self.execution)


if __name__ == "__main__":
    unittest.main()
