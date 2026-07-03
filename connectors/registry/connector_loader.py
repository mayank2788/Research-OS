import json
from pathlib import Path

from connectors.openalex.openalex_connector import OpenAlexConnector
from connectors.crossref.crossref_connector import CrossrefConnector
from connectors.institutional.institutional_connector import InstitutionalConnector
from connectors.doaj.doaj_connector import DOAJConnector
from connectors.arxiv.arxiv_connector import ArxivConnector


class AROSConnectorLoader:
    """
    Registry based connector loader.

    Reads source_registry.json and loads only enabled connectors.

    This prevents discovery engine modifications
    when adding new integrations.
    """

    def __init__(
        self,
        registry_path="connectors/registry/source_registry.json",
    ):
        self.registry_path = Path(registry_path)


    def load_registry(self):

        with open(
            self.registry_path,
            "r",
            encoding="utf-8",
        ) as file:

            return json.load(file)


    def load_enabled_connectors(self):

        registry = self.load_registry()

        connectors = []

        for item in registry["integrations"]:

            if not item["enabled"]:
                continue


            if item["id"] == "openalex":

                connectors.append(
                    OpenAlexConnector()
                )


            elif item["id"] == "crossref":

                connectors.append(
                    CrossrefConnector()
                )


            elif item["id"] == "doaj":

                connectors.append(
                    DOAJConnector()
                )


            elif item["id"] == "arxiv":

                connectors.append(
                    ArxivConnector()
                )


            elif item["id"] == "institutional_registry":

                institutional_file = Path(
                    "connectors/institutional/institution_registry.json"
                )

                data = json.loads(
                    institutional_file.read_text()
                )

                for institution in data["institutions"]:

                    connectors.append(
                        InstitutionalConnector(
                            institution["short_name"]
                        )
                    )

        return connectors
