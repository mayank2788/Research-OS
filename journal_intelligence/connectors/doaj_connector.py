import csv
import json
from pathlib import Path


class DOAJConnector:
    """
    AROS DOAJ Connector

    Converts DOAJ journal CSV export
    into normalized journal objects.
    """


    def __init__(self):

        self.input_file = Path(
            "journal_intelligence/raw_sources/doaj/doaj_journals.csv"
        )

        self.output_file = Path(
            "journal_intelligence/processed/doaj_normalized.json"
        )


    def normalize(self):

        journals = []


        with open(
            self.input_file,
            encoding="utf-8",
            errors="ignore"
        ) as f:

            reader = csv.DictReader(f)


            for row in reader:

                journal = {

                    "journal_name":
                        row.get(
                            "Journal title",
                            ""
                        ),

                    "issn":
                        row.get(
                            "Journal ISSN (print version)",
                            ""
                        ),

                    "eissn":
                        row.get(
                            "Journal EISSN (online version)",
                            ""
                        ),

                    "publisher":
                        row.get(
                            "Publisher",
                            ""
                        ),

                    "country":
                        row.get(
                            "Country of publisher",
                            ""
                        ),

                    "source_registry":
                        ["DOAJ"],

                    "access": {

                        "access_type":
                            "open",

                        "doaj_listed":
                            True,

                        "license":
                            row.get(
                                "Journal license",
                                ""
                            )
                    },


                    "urls": {

                        "journal_url":
                            row.get(
                                "Journal URL",
                                ""
                            )
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

    print(
        DOAJConnector().normalize()
    )

