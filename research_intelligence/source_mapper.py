import json
from pathlib import Path


class SourceMapper:
    """
    AROS Source Mapper.

    Maps research domains to suitable
    academic and institutional sources.
    """

    def __init__(
        self,
        path="research_domains/source_mapping.json"
    ):
        self.path = Path(path)
        self.mapping = self.load()


    def load(self):

        with open(
            self.path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)


    def get_sources(self, domain):

        domain_data = (
            self.mapping["domains"]
            .get(domain)
        )

        if not domain_data:
            return []


        return domain_data["sources"]


    def get_ranking_priority(self, domain):

        domain_data = (
            self.mapping["domains"]
            .get(domain)
        )

        if not domain_data:
            return []


        return domain_data[
            "ranking_priority"
        ]
