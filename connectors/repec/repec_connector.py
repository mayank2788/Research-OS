from connectors.base.base_connector import BaseConnector


class RePEcConnector(BaseConnector):
    """
    RePEc Integration Adapter.

    Purpose:
    - Economics research
    - Finance working papers
    - Policy research

    Status:
    Connector ready.

    Future:
    - IDEAS/RePEc harvesting
    - Metadata parser
    """

    def __init__(self):
        super().__init__("RePEc")


    def search(self, query, max_results=10):

        print(
            "RePEc adapter ready. Metadata harvesting pending."
        )

        return []
