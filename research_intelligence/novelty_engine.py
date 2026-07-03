class ResearchNoveltyEngine:
    """
    AROS Research Novelty Engine v1.

    Evaluates research opportunity signals for novelty potential
    across interdisciplinary AROS domains.
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
        if "theory" in text or "agency" in text or "stakeholder" in text:
            return 7
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
        return 5

    def score_variables(self, text):
        signals = ["esg", "governance", "debt", "performance", "tax", "ai"]
        count = sum(1 for signal in signals if signal in text)
        return min(9, 4 + count)

    def score_interdisciplinary(self, text):
        areas = ["finance", "accounting", "governance", "corporate governance", "policy", "economics", "management", "methodology", "interdisciplinary", "ai"]
        count = sum(1 for area in areas if area in text)
        return min(10, 3 + count)

    def label(self, score):
        if score >= 8:
            return "High"
        if score >= 6:
            return "Medium"
        return "Low"
