from research_intelligence.novelty_engine import (
    ResearchNoveltyEngine
)


class ResearchIdeaGenerator:
    """
    AROS Research Idea Generator v1.

    Converts research gaps into potential
    Q1-oriented research ideas.

    Supports:
    - Finance
    - Accounting & Reporting
    - Corporate Governance
    - Economics & Public Policy
    - Management
    - Research Methodology
    - AI Enabled Research
    """

    def __init__(self):

        self.novelty_engine = ResearchNoveltyEngine()


    def generate(
        self,
        gap_analysis
    ):

        ideas = []


        domains = [
            x[0]
            for x in gap_analysis.get(
                "dominant_domains",
                []
            )
        ]


        methods = [
            x[0]
            for x in gap_analysis.get(
                "dominant_methods",
                []
            )
        ]


        variables = [
            x[0]
            for x in gap_analysis.get(
                "dominant_variables",
                []
            )
        ]


        if domains:

            ideas.append(
                f"AI enabled research approach in "
                f"{domains[0]} using advanced analytical methods"
            )


        if domains and variables:

            ideas.append(
                f"Impact of {variables[0]} on outcomes in "
                f"{domains[0]} using interdisciplinary perspective"
            )


        if (
            "Machine Learning Method"
            not in methods
            and domains
        ):

            ideas.append(
                f"Machine learning based predictive framework "
                f"for {domains[0]} research"
            )



        ranked = []


        for idea in ideas:

            ranked.append(
                self.novelty_engine.score_idea(
                    idea
                )
            )


        return sorted(
            ranked,
            key=lambda x: x["overall_score"],
            reverse=True
        )
