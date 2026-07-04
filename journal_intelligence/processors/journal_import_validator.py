import json
from pathlib import Path
from collections import Counter


class JournalImportValidator:
    """
    AROS Journal Import Validator

    Checks imported registry quality:
    - total journals
    - ISSN coverage
    - quartile distribution
    - country spread
    """


    def __init__(self):

        self.file = Path(
            "journal_intelligence/processed/scimago_normalized.json"
        )


    def validate(self):

        if not self.file.exists():

            return {
                "status": "No processed file found"
            }


        journals = json.loads(
            self.file.read_text(
                encoding="utf-8"
            )
        )


        issns = [
            j.get("issn")
            for j in journals
            if j.get("issn")
        ]


        countries = Counter(
            j.get("country", "Unknown")
            for j in journals
        )


        quartiles = Counter(
            j.get(
                "ranking",
                {}
            ).get(
                "sjr_quartile",
                "Unknown"
            )
            for j in journals
        )


        return {

            "total_journals":
                len(journals),

            "unique_issns":
                len(set(issns)),

            "countries":
                dict(countries),

            "quartiles":
                dict(quartiles)
        }



if __name__ == "__main__":

    result = JournalImportValidator().validate()


    print("="*70)

    print(
        "AROS JOURNAL IMPORT VALIDATION"
    )

    print("="*70)


    for k,v in result.items():

        print(
            k,
            ":",
            v
        )


    print()

    print(
        "✓ Validation completed"
    )

