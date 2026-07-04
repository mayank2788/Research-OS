import csv
import json
from pathlib import Path


class ScimagoConnector:
    """
    AROS SCImago Connector v1

    Converts SCImago CSV exports into
    normalized AROS journal objects.

    Source:
    raw_sources/scimago/*.csv
    """


    def __init__(self):

        self.input_folder = Path(
            "journal_intelligence/raw_sources/scimago"
        )

        self.output_file = Path(
            "journal_intelligence/processed/scimago_normalized.json"
        )


    def normalize(self):

        journals = []


        for file in self.input_folder.glob("*.csv"):

            with open(
                file,
                encoding="utf-8",
                errors="ignore"
            ) as f:

                reader = csv.DictReader(
                    f,
                    delimiter=";"
                )


                for row in reader:

                    journal = {

                        "journal_name":
                            row.get("Title",""),

                        "issn":
                            row.get("Issn",""),

                        "publisher":
                            row.get("Publisher",""),

                        "country":
                            row.get("Country",""),

                        "source_registry":
                            ["SCImago"],

                        "subject_categories":
                            [
                                row.get(
                                    "Categories",
                                    ""
                                )
                            ],

                        "ranking": {

                            "sjr_quartile":
                                row.get(
                                    "SJR Best Quartile",
                                    ""
                                ),

                            "sjr_score":
                                row.get(
                                    "SJR",
                                    ""
                                )
                        },

                        "access": {

                            "access_type":
                                "unknown"
                        }
                    }


                    journals.append(
                        journal
                    )


        self.output_file.write_text(

            json.dumps(
                journals,
                indent=2,
                ensure_ascii=False
            ),

            encoding="utf-8"
        )


        return {
            "journals_processed":
                len(journals),

            "output":
                str(self.output_file)
        }



if __name__ == "__main__":

    connector = ScimagoConnector()

    print(
        connector.normalize()
    )

