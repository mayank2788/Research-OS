class ResearchIntelligenceExtractor:
    """
    Extracts research intelligence from Knowledge Objects.

    Version 1:
    Rule-based academic extraction foundation.

    Future:
    - AI extraction
    - Methodology classification
    - Variable identification
    - Research gap detection
    """

    def extract(self, knowledge_object):

        text = " ".join([
            knowledge_object.title or "",
            knowledge_object.abstract or "",
            knowledge_object.ai_summary or "",
        ]).lower()


        intelligence = {
            "title": knowledge_object.title,

            "possible_methodology": self.detect_methodology(text),

            "possible_research_type": self.detect_research_type(text),

            "variables": [],

            "dataset": "",

            "theory": "",

            "findings": "",

            "limitations": "",

            "future_scope": "",
        }

        return intelligence


    def detect_methodology(self, text):

        methods = {
            "regression": "Regression Analysis",
            "panel": "Panel Data Analysis",
            "case study": "Case Study",
            "survey": "Survey Method",
            "interview": "Interview Method",
            "review": "Literature Review",
        }

        detected = []

        for key, value in methods.items():
            if key in text:
                detected.append(value)

        return detected


    def detect_research_type(self, text):

        if "review" in text:
            return "Review Paper"

        if "empirical" in text:
            return "Empirical Study"

        if "case study" in text:
            return "Case Study"

        return "Unclassified"
