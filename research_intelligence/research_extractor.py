import json
from pathlib import Path


class ResearchIntelligenceExtractor:
    """
    Research Intelligence Extractor v2.

    Extracts early research intelligence from Knowledge Objects:
    - domain classification
    - theory signals
    - methodology signals
    - research type
    - variable signals

    This is rule-based foundation. AI extraction comes later.
    """

    def __init__(self, domain_registry_path="research_domains/domain_registry.json"):
        self.domain_registry_path = Path(domain_registry_path)
        self.domain_registry = self.load_domain_registry()

    def load_domain_registry(self):
        with open(self.domain_registry_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def build_text(self, knowledge_object):
        return " ".join([
            knowledge_object.title or "",
            knowledge_object.abstract or "",
            knowledge_object.ai_summary or "",
            " ".join(knowledge_object.keywords or []),
            knowledge_object.research_domain or "",
        ]).lower()

    def extract(self, knowledge_object):
        text = self.build_text(knowledge_object)

        return {
            "title": knowledge_object.title,
            "domains": self.detect_domains(text),
            "possible_theories": self.detect_theories(text),
            "possible_methodology": self.detect_methodology(text),
            "possible_research_type": self.detect_research_type(text),
            "variable_signals": self.detect_variable_signals(text),
            "dataset": "",
            "findings": "",
            "limitations": "",
            "future_scope": "",
        }

    def detect_domains(self, text):
        matched = []

        for domain in self.domain_registry.get("domains", []):
            domain_score = 0
            matched_areas = []

            if domain["name"].lower() in text:
                domain_score += 1
                matched_areas.append(domain["name"])

            for area in domain.get("areas", []):
                if area.lower() in text:
                    domain_score += 1
                    matched_areas.append(area)

            if domain_score > 0:
                matched.append({
                    "domain": domain["name"],
                    "score": domain_score,
                    "matched_areas": matched_areas,
                })

        return sorted(
            matched,
            key=lambda item: item["score"],
            reverse=True,
        )

    def detect_theories(self, text):
        detected = []

        for domain in self.domain_registry.get("domains", []):
            for theory in domain.get("theories", []):
                if theory.lower() in text:
                    detected.append(theory)

        return sorted(set(detected))

    def detect_methodology(self, text):
        methods = {
            "regression": "Regression Analysis",
            "panel": "Panel Data Analysis",
            "case study": "Case Study",
            "survey": "Survey Method",
            "interview": "Interview Method",
            "systematic literature review": "Systematic Literature Review",
            "bibliometric": "Bibliometric Analysis",
            "meta analysis": "Meta Analysis",
            "structural equation": "Structural Equation Modeling",
            "pls-sem": "PLS-SEM",
            "machine learning": "Machine Learning Method",
        }

        detected = []

        for key, value in methods.items():
            if key in text:
                detected.append(value)

        return sorted(set(detected))

    def detect_research_type(self, text):
        if "systematic literature review" in text or "bibliometric" in text:
            return "Review / Bibliometric Study"

        if "empirical" in text or "regression" in text or "panel" in text:
            return "Empirical Study"

        if "case study" in text:
            return "Case Study"

        if "conceptual" in text:
            return "Conceptual Paper"

        return "Unclassified"

    def detect_variable_signals(self, text):
        signals = []

        terms = [
            "profitability",
            "leverage",
            "debt",
            "capital structure",
            "firm value",
            "performance",
            "governance",
            "taxation",
            "earnings management",
            "esg",
            "working capital",
        ]

        for term in terms:
            if term in text:
                signals.append(term)

        return sorted(set(signals))
