from connectors.base.base_connector import BaseConnector


class ZoteroConnector(BaseConnector):
    """
    Zotero Integration Adapter.

    Purpose:
    - Personal research library
    - PDF management
    - Citation workflow

    Requires:
    Zotero API key
    Library ID
    """

    def __init__(self):
        super().__init__("Zotero")


    def search(self, query, max_results=10):

        print(
            "Zotero adapter ready. Credentials required."
        )

        return []
