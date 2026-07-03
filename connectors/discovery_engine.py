from connectors.registry.connector_loader import AROSConnectorLoader


class AROSDiscoveryEngine:
    """
    Registry driven multi-source discovery engine.

    Version 3:
    - No hard coded connectors
    - Loads enabled integrations
    - Supports future expansion
    """

    def __init__(self):
        loader = AROSConnectorLoader()
        self.connectors = loader.load_enabled_connectors()

    def deduplicate(self, results):
        unique = {}

        for item in results:
            if item.doi:
                key = "doi:" + item.doi.lower().strip()
            else:
                key = "title:" + item.title.lower().strip()

            if key not in unique:
                unique[key] = item

        return list(unique.values())

    def search_all(self, query, max_results_per_source=5):
        combined = []

        for connector in self.connectors:
            print(f"Searching {connector.name}...")

            try:
                results = connector.search(
                    query=query,
                    max_results=max_results_per_source,
                )
                combined.extend(results)

            except Exception as error:
                print(f"{connector.name} failed: {error}")

        return self.deduplicate(combined)
