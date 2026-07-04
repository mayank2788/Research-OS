import csv
import json
from pathlib import Path


class UGCCareConnector:
    """
    AROS UGC CARE Connector

    Reads UGC CARE journal lists:
    J1.csv
    J2.csv
    J3.csv
    J4.csv

    Creates normalized Indian journal
    recognition database.
    """


    def __init__(self):

        self.input_folder = Path(
            "journal_intelligence/raw_sources/ugc_care"
        )

        self.output_file = Path(
            "journal_intelligence/processed/ugc_care_normalized.json"
        )


    def normalize(self):

        journals = []


        for file in self.input_folder.glob("*.csv"):

            with open(
                file,
                encoding="utf-8",
                errors="ignore"
            ) as f:

                reader = csv.reader(f)


                for row in reader:

                    if not row:
                        continue


                    name = row[0].strip()


                    if (
                        not name
                        or name.lower()
                        in ["title","journal"]
                    ):
                        continue


                    journal = {

                        "journal_name": name,

                        "source_registry": [
                            "UGC CARE"
                        ],

                        "ranking": {

                            "ugc_care_status":
                                True
                        },

                        "access": {},

                        "source_file":
                            file.name

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
        UGCCareConnector().normalize()
    )

