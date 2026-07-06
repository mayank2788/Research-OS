import json
import urllib.parse
import urllib.request
from pathlib import Path


class DOAJArticleConnector:
    """
    AROS DOAJ Article Connector.

    Searches DOAJ open access articles
    and stores research paper metadata.
    """


    def __init__(self):

        self.output_dir = Path(
            "Research_Output/Literature_Library"
        )

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True
        )


    def search(self, query, limit=100):

        encoded = urllib.parse.quote(query)

        url = (
            "https://doaj.org/api/search/articles/"
            + encoded
            + f"?pageSize={limit}"
        )


        with urllib.request.urlopen(url) as response:

            data = json.loads(
                response.read().decode()
            )


        papers = []


        for item in data.get("results", []):

            bibjson = item.get(
                "bibjson",
                {}
            )


            paper = {

                "title":
                    bibjson.get(
                        "title",
                        ""
                    ),

                "journal":
                    bibjson.get(
                        "journal",
                        {}
                    ).get(
                        "title",
                        ""
                    ),

                "year":
                    bibjson.get(
                        "year",
                        ""
                    ),

                "doi":
                    "",

                "authors":
                    [
                        a.get("name")
                        for a in bibjson.get(
                            "author",
                            []
                        )
                    ],

                "links":
                    bibjson.get(
                        "link",
                        []
                    ),

                "source":
                    "DOAJ"
            }


            for identifier in bibjson.get(
                "identifier",
                []
            ):

                if (
                    identifier.get("type")
                    == "doi"
                ):

                    paper["doi"] = (
                        identifier.get("id")
                    )


            papers.append(
                paper
            )


        return papers


    def save_domain(
        self,
        domain,
        papers
    ):

        folder = (
            self.output_dir
            /
            domain.replace(
                " ",
                "_"
            )
        )

        folder.mkdir(
            exist_ok=True
        )


        output = (
            folder
            /
            "metadata.json"
        )


        output.write_text(

            json.dumps(
                papers,
                indent=2,
                ensure_ascii=False
            ),

            encoding="utf-8"
        )


        return str(output)



if __name__ == "__main__":

    connector = DOAJArticleConnector()

    papers = connector.search(
        "corporate finance",
        20
    )

    location = connector.save_domain(
        "Finance",
        papers
    )


    print(
        {
            "papers_found": len(papers),
            "output": location
        }
    )

