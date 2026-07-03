import json
from datetime import datetime
from pathlib import Path


class AROSResearchRelevanceEngine:
    """
    AROS Research Relevance Engine.

    Version 2.1:
    - Weighted research relevance scoring
    - Primary evidence: title and abstract
    - Secondary evidence: keywords and declared domain
    - Recency scoring
    - Open-access scoring
    """

    def __init__(self, profile_path="profile/research_profile.json"):
        self.profile_path = Path(profile_path)
        self.profile = self.load_profile()
        self.domain_terms = self.extract_domain_terms()

    def load_profile(self):
        with open(self.profile_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def extract_domain_terms(self):
        terms = []

        for domain, topics in self.profile.get("research_domains", {}).items():
            terms.append(domain.replace("_", " "))

            for topic in topics:
                terms.append(topic)

        return sorted(set(term.lower() for term in terms))

    def score_research_match(self, knowledge_object):

        primary_text = " ".join([
            knowledge_object.title or "",
            knowledge_object.abstract or "",
        ]).lower()

        secondary_text = " ".join([
            " ".join(knowledge_object.keywords or []),
            knowledge_object.research_domain or "",
        ]).lower()

        matched_primary = []
        matched_secondary = []

        for term in self.domain_terms:

            if term in primary_text:
                matched_primary.append(term)

            elif term in secondary_text:
                matched_secondary.append(term)

        score = min(
            60,
            len(matched_primary) * 15
            + len(matched_secondary) * 5
        )

        return score, matched_primary, matched_secondary

    def score_recency(self, knowledge_object):

        try:
            year = int(knowledge_object.publication_year)
        except Exception:
            return 0

        current = datetime.now().year

        if year >= current - 3:
            return 15
        if year >= current - 7:
            return 10
        if year >= current - 12:
            return 5

        return 0

    def score_open_access(self, knowledge_object):
        return 10 if knowledge_object.open_access else 0

    def label_score(self, score):

        if score >= 70:
            return "High"
        if score >= 40:
            return "Medium"
        if score > 0:
            return "Low"

        return "Not Relevant"

    def evaluate(self, knowledge_object):

        research_score, primary, secondary = (
            self.score_research_match(knowledge_object)
        )

        recency_score = self.score_recency(knowledge_object)
        access_score = self.score_open_access(knowledge_object)

        total = min(
            100,
            research_score + recency_score + access_score
        )

        knowledge_object.confidence = total

        return {
            "title": knowledge_object.title,
            "relevance_score": total,
            "relevance_label": self.label_score(total),
            "primary_matches": primary,
            "secondary_matches": secondary,
            "score_breakdown": {
                "research_score": research_score,
                "recency_score": recency_score,
                "open_access_score": access_score,
            },
            "status": "evaluated",
        }
