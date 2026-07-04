import json
from pathlib import Path

from openpyxl import Workbook


class ResearchMatrixEngine:
    """
    AROS Research Matrix Engine v1.

    Domain neutral evidence builder.

    Converts preserved knowledge objects into
    structured research matrices.

    Supports:
    - Literature Review
    - Gap Analysis
    - Theory Mapping
    - Methodology Mapping
    """

    def build_matrix(
        self,
        output_type,
        project_id
    ):

        base = (
            Path("Research_Output")
            / output_type
            / "Researched_Library"
            / project_id
        )


        metadata_folder = (
            base
            / "02_Metadata_Library"
        )


        output_folder = (
            base
            / "04_Evidence_Tables"
        )


        output_folder.mkdir(
            parents=True,
            exist_ok=True
        )


        matrix_file = (
            output_folder
            / "Literature_Matrix.xlsx"
        )


        wb = Workbook()

        ws = wb.active

        ws.title = "Literature Matrix"


        headers = [

            "Title",

            "Authors",

            "Year",

            "Source",

            "DOI",

            "Research Domain",

            "Theory",

            "Variables",

            "Methodology",

            "Dataset",

            "Findings",

            "Limitations",

            "Research Gap",

            "Future Scope"

        ]


        ws.append(headers)


        for file in metadata_folder.glob("*.json"):

            data = json.loads(
                file.read_text(
                    encoding="utf-8"
                )
            )


            ws.append(

                [

                    data.get("title"),

                    ", ".join(
                        data.get(
                            "authors",
                            []
                        )
                    ),

                    data.get("year"),

                    data.get("source"),

                    data.get("doi"),

                    data.get(
                        "research_domain"
                    ),


                    "",

                    "",

                    "",

                    "",

                    "",

                    "",

                    "",

                    ""

                ]

            )


        wb.save(matrix_file)


        return str(matrix_file)
