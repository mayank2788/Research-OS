import json
from pathlib import Path


class AROSResearchRelevanceEngine:
    """
    Evaluates Knowledge Objects against the research profile.

    Version 1:
    - Profile keyword matching
    - Title matching
    - Abstract matching
    - Keyword matching

    Future:
    - Methodology scoring
    - Journal quality
    - Citation impact
    - Research gap detection
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

        domains = self.profile.get("research_domains", {})

        for domain, topics in domains.items():
            terms.append(domain.replace("_", " "))

            for topic in topics:
                terms.append(topic)

        return [x.lower() for x in terms]

    def evaluate(self, knowledge_object):

        searchable_text = " ".join([
            knowledge_object.title or "",
            knowledge_object.abstract or "",
            " ".join(knowledge_object.keywords or [])
        ]).lower()

        matched_terms = []

        for term in self.domain_terms:
            if term in searchable_text:
                matched_terms.append(term)

        score = min(
            100,
            round(
                (len(matched_terms) / max(len(self.domain_terms), 1)) * 100,
                2
            )
        )

        knowledge_object.confidence = score

        return {
            "title": knowledge_object.title,
            "relevance_score": score,
            "matched_terms": matched_terms,
            "status": "evaluated"
        }
