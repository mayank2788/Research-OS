from connectors.base.base_connector import BaseConnector


class COREConnector(BaseConnector):
    """
    CORE connector skeleton.

    CORE API requires an API key, so this connector is kept disabled
    until CORE_API_KEY is configured.
    """

    def __init__(self):
        super().__init__("CORE")

    def search(self, query, max_results=10):
        print("CORE API key required. Connector structure ready.")
        return []
