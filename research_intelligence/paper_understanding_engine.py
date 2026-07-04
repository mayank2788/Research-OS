class PaperUnderstandingEngine:
    """
    AROS Paper Understanding Engine v1.

    Domain neutral research comprehension layer.

    Purpose:
    Convert paper text into structured
    research methodology intelligence.
    """


    def understand(
        self,
        knowledge_object
    ):

        text = self.build_text(
            knowledge_object
        )


        return {

            "research_problem":
                self.detect_problem(text),


            "research_design":
                self.detect_design(text),


            "variables":
                self.detect_variables(text),


            "statistical_models":
                self.detect_models(text),


            "dataset":
                self.detect_dataset(text),


            "contribution":
                self.detect_contribution(text),


            "limitations":
                self.detect_limitations(text),


            "future_scope":
                self.detect_future_scope(text)

        }



    def build_text(
        self,
        obj
    ):

        return " ".join(
            [

                obj.title or "",

                obj.abstract or "",

                getattr(
                    obj,
                    "ai_summary",
                    ""
                ) or ""

            ]
        ).lower()



    def detect_problem(
        self,
        text
    ):

        signals = [

            "gap",
            "problem",
            "challenge",
            "limited evidence",
            "unclear"

        ]


        return [
            s for s in signals
            if s in text
        ]



    def detect_design(
        self,
        text
    ):

        methods = [

            "panel data",

            "regression",

            "case study",

            "survey",

            "bibliometric",

            "systematic literature review",

            "machine learning"

        ]


        return [
            m for m in methods
            if m in text
        ]



    def detect_variables(
        self,
        text
    ):

        variables = [

            "profitability",

            "leverage",

            "firm value",

            "earnings management",

            "capital structure",

            "governance",

            "tax",

            "esg",

            "performance"

        ]


        return [
            v for v in variables
            if v in text
        ]



    def detect_models(
        self,
        text
    ):

        models = [

            "ols",

            "fixed effect",

            "random effect",

            "gmm",

            "sem",

            "pls"

        ]


        return [
            m for m in models
            if m in text
        ]



    def detect_dataset(
        self,
        text
    ):

        signals = [

            "database",

            "annual report",

            "panel",

            "sample",

            "dataset"

        ]


        return [
            s for s in signals
            if s in text
        ]



    def detect_contribution(
        self,
        text
    ):

        signals = [

            "contribution",

            "evidence",

            "implication",

            "novel"

        ]


        return [
            s for s in signals
            if s in text
        ]



    def detect_limitations(
        self,
        text
    ):

        return (
            ["limitations mentioned"]
            if "limitation" in text
            else []
        )



    def detect_future_scope(
        self,
        text
    ):

        return (
            ["future research direction"]
            if "future research" in text
            else []
        )
