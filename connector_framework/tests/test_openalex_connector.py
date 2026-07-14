import unittest

from connector_framework.connector_registry import ConnectorRegistry
from connector_framework.credential_manager import ConnectorCredentialManager
from connector_framework.execution_manager import ConnectorExecutionManager
from connector_framework.connectors.openalex_connector import OpenAlexConnector


class TestOpenAlexConnector(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = ConnectorRegistry()
        cls.credentials = ConnectorCredentialManager(cls.registry)
        cls.execution = ConnectorExecutionManager(
            cls.registry,
            cls.credentials,
        )

        cls.connector = OpenAlexConnector(
            cls.registry,
            cls.credentials,
            cls.execution,
        )

    def test_health_check(self) -> None:
        result = self.connector.health()

        self.assertIsInstance(result, dict)
        self.assertTrue(result.get("healthy"))
        self.assertEqual(result.get("status_code"), 200)
        self.assertEqual(result.get("connector"), "openalex")

    def test_search_returns_results(self) -> None:
        response = self.connector.search(
            search="corporate finance",
            per_page=5,
        )

        self.assertIsInstance(response, dict)

        results = response.get("results", [])

        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)
        self.assertLessEqual(len(results), 5)


if __name__ == "__main__":
    unittest.main()
