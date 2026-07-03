class ResearchNoveltyEngine:
    """
    AROS Research Novelty Engine v2.

    Scores interdisciplinary research ideas across:
    - Finance
    - Accounting & Reporting
    - Corporate Governance
    - Economics & Public Policy
    - Management
    - Research Methodology
    - AI Enabled Research
    """

    def score_idea(self, idea):
        text = idea.lower()

        scores = {
            "theory_novelty": self.score_theory(text),
            "methodology_novelty": self.score_methodology(text),
            "context_novelty": self.score_context(text),
            "variable_novelty": self.score_variables(text),
            "interdisciplinary_novelty": self.score_interdisciplinary(text),
        }

        overall = round(sum(scores.values()) / len(scores), 2)

        return {
            "idea": idea,
            "scores": scores,
            "overall_score": overall,
            "q1_potential": self.label(overall),
        }

    def score_theory(self, text):
        if "agency" in text or "stakeholder" in text or "governance" in text:
            return 7
        if "theory" in text:
            return 6
        return 4

    def score_methodology(self, text):
        if "machine learning" in text or "ai" in text or "advanced analytical" in text:
            return 8
        if "panel" in text or "sem" in text or "pls" in text:
            return 6
        return 4

    def score_context(self, text):
        if "india" in text or "public sector" in text or "energy" in text:
            return 8
        if "emerging market" in text or "developing economy" in text:
            return 7
        return 5

    def score_variables(self, text):
        signals = [
            "esg",
            "governance",
            "corporate governance",
            "debt",
            "performance",
            "financial performance",
            "tax",
            "accounting",
            "policy",
            "management",
            "ai",
        ]

        count = sum(1 for signal in signals if signal in text)
        return min(9, 4 + count)

    def score_interdisciplinary(self, text):
        areas = [
            "finance",
            "financial",
            "accounting",
            "governance",
            "corporate governance",
            "policy",
            "economics",
            "management",
            "methodology",
            "interdisciplinary",
            "ai",
            "artificial intelligence",
        ]

        count = sum(1 for area in areas if area in text)
        return min(10, 4 + count)

    def label(self, score):
        if score >= 7:
            return "High"
        if score >= 5.5:
            return "Medium"
        return "Low"
