from research_intelligence.research_extractor import (
    ResearchIntelligenceExtractor
)


class ResearchMatrixGenerator:
    """
    AROS Research Matrix Generator.

    Converts Knowledge Objects into structured
    academic research matrices.

    Supports:
    - Finance
    - Accounting
    - Governance
    - Economics / Policy
    - Management
    - Research Methodology
    - AI Research

    Version:
    v1 rule-based matrix generation
    """

    def __init__(self):

        self.extractor = ResearchIntelligenceExtractor()


    def generate_row(self, knowledge_object):

        intelligence = self.extractor.extract(
            knowledge_object
        )


        return {

            "title":
                knowledge_object.title,

            "year":
                knowledge_object.publication_year,

            "source":
                knowledge_object.source,

            "doi":
                knowledge_object.doi,


            "domains":
                [
                    d["domain"]
                    for d in intelligence["domains"]
                ],


            "theories":
                intelligence[
                    "possible_theories"
                ],


            "methodology":
                intelligence[
                    "possible_methodology"
                ],


            "research_type":
                intelligence[
                    "possible_research_type"
                ],


            "variables_constructs":
                intelligence[
                    "variable_signals"
                ],


            "research_gap":
                "",


            "future_scope":
                "",
        }


    def generate_matrix(
        self,
        knowledge_objects
    ):

        matrix = []

        for obj in knowledge_objects:

            matrix.append(
                self.generate_row(obj)
            )

        return matrix
