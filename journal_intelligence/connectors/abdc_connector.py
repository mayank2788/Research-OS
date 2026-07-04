import json
from pathlib import Path

import xlrd


class ABDCConnector:
    """
    AROS ABDC Connector

    Reads ABDC .xls Journal Quality List.
    """


    def __init__(self):

        self.input_file = Path(
            "journal_intelligence/raw_sources/abdc/abdc_journal_list.xls"
        )

        self.output_file = Path(
            "journal_intelligence/processed/abdc_normalized.json"
        )


    def normalize(self):

        journals = []


        workbook = xlrd.open_workbook(
            str(self.input_file)
        )


        sheet = workbook.sheet_by_index(0)


        header_row = 2

        headers = [
            str(sheet.cell_value(header_row, c))
            .strip()
            .lower()
            for c in range(sheet.ncols)
        ]


        for r in range(header_row + 1, sheet.nrows):

            values = [
                sheet.cell_value(r, c)
                for c in range(sheet.ncols)
            ]


            record = dict(
                zip(headers, values)
            )


            title = (
                record.get("journal title")
                or record.get("title")
                or ""
            )


            issn = (
                record.get("issn")
                or ""
            )


            rating = (
                record.get("abdc rating")
                or record.get("rating")
                or ""
            )


            if not title:
                continue


            journals.append(
                {
                    "journal_name": title,

                    "issn": issn,

                    "source_registry": [
                        "ABDC"
                    ],

                    "ranking": {

                        "abdc_rating":
                            rating
                    }
                }
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
        ABDCConnector().normalize()
    )

