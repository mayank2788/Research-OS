from connectors.openalex.openalex_connector import OpenAlexConnector
from connectors.crossref.crossref_connector import CrossrefConnector


class AROSDiscoveryEngine:
    """
    Multi-source discovery engine.

    Version 1:
    - Searches OpenAlex and Crossref
    - Combines Knowledge Objects
    - Deduplicates by DOI first, title second
    """

    def __init__(self):
        self.connectors = [
            OpenAlexConnector(),
            CrossrefConnector(),
        ]

    def deduplicate(self, results):
        unique = {}

        for item in results:
            key = ""

            if item.doi:
                key = f"doi:{item.doi.lower().strip()}"
            else:
                key = f"title:{item.title.lower().strip()}"

            if key and key not in unique:
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
