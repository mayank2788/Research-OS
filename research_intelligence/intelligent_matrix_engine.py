import json
from pathlib import Path
from types import SimpleNamespace

from openpyxl import Workbook

from research_intelligence.research_extractor import (
    ResearchIntelligenceExtractor
)


class IntelligentMatrixEngine:
    """
    AROS Intelligent Research Matrix Engine v2.

    Converts preserved knowledge objects into
    research intelligence.
    """

    def __init__(self):
        self.extractor = ResearchIntelligenceExtractor()


    def build(
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

        metadata = base / "02_Metadata_Library"

        output = base / "05_Intelligent_Matrix"

        output.mkdir(
            parents=True,
            exist_ok=True
        )

        file = output / "Intelligent_Literature_Matrix.xlsx"


        wb = Workbook()

        ws = wb.active

        ws.title = "Research Intelligence"


        ws.append(
            [
                "Title",
                "Year",
                "Source",
                "Domain",
                "Theory",
                "Variables",
                "Methodology",
                "Research Type",
                "Dataset",
                "Findings",
                "Limitations",
                "Future Scope"
            ]
        )


        for item in metadata.glob("*.json"):

            data = json.loads(
                item.read_text(
                    encoding="utf-8"
                )
            )


            obj = SimpleNamespace(
                title=data.get("title"),
                abstract=data.get("abstract"),
                ai_summary="",
                keywords=[],
                research_domain=data.get(
                    "research_domain"
                )
            )


            intelligence = (
                self.extractor.extract(obj)
            )


            ws.append(
                [
                    data.get("title"),

                    data.get("year"),

                    data.get("source"),

                    str(
                        intelligence[
                            "domains"
                        ]
                    ),

                    ", ".join(
                        intelligence[
                            "possible_theories"
                        ]
                    ),

                    ", ".join(
                        intelligence[
                            "variable_signals"
                        ]
                    ),

                    ", ".join(
                        intelligence[
                            "possible_methodology"
                        ]
                    ),

                    intelligence[
                        "possible_research_type"
                    ],

                    intelligence[
                        "dataset"
                    ],

                    intelligence[
                        "findings"
                    ],

                    intelligence[
                        "limitations"
                    ],

                    intelligence[
                        "future_scope"
                    ]
                ]
            )


        wb.save(file)

        return str(file)
