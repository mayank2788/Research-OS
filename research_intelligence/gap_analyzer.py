from collections import Counter


class ResearchGapAnalyzer:
    """
    AROS Research Gap Analyzer v1.

    Purpose:
    Detect research opportunity signals from
    structured research matrices.

    Supports:
    - Finance
    - Accounting
    - Governance
    - Economics / Policy
    - Management
    - Research Methodology
    - AI Research

    Version:
    Rule-based foundation before AI reasoning layer.
    """


    def analyze(self, research_matrix):

        domains = []
        theories = []
        methods = []
        variables = []


        for row in research_matrix:

            domains.extend(
                row.get("domains", [])
            )

            theories.extend(
                row.get("theories", [])
            )

            methods.extend(
                row.get("methodology", [])
            )

            variables.extend(
                row.get(
                    "variables_constructs",
                    []
                )
            )


        return {

            "dominant_domains":
                Counter(domains).most_common(),


            "dominant_theories":
                Counter(theories).most_common(),


            "dominant_methods":
                Counter(methods).most_common(),


            "dominant_variables":
                Counter(variables).most_common(),


            "opportunity_signals":
                self.generate_signals(
                    domains,
                    theories,
                    methods,
                    variables,
                )
        }



    def generate_signals(
        self,
        domains,
        theories,
        methods,
        variables
    ):

        signals = []


        if (
            "AI Enabled Research" not in domains
            and len(domains) > 0
        ):

            signals.append(
                "Explore AI-enabled approaches within existing research domain"
            )


        if (
            "Machine Learning Method"
            not in methods
            and len(methods) > 0
        ):

            signals.append(
                "Potential opportunity for machine learning based methodology"
            )


        if len(set(theories)) <= 2 and len(theories) > 0:

            signals.append(
                "Explore alternative theoretical perspectives"
            )


        return signals
