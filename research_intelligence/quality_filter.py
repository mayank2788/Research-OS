class ResearchQualityFilter:
    """
    AROS Research Quality Filter v1.

    Purpose:
    Filter discovered literature before PDF download.

    Scores:
    - topic relevance
    - source quality
    - document type quality
    - recency
    - Q1 probability proxy

    This is rule-based foundation. Journal ranking engine comes later.
    """

    def __init__(self):
        self.high_quality_sources = [
            "OpenAlex",
            "Crossref",
            "DOAJ",
            "Semantic Scholar",
            "CORE",
            "SSRN",
            "RePEc",
        ]

        self.institutional_sources = [
            "RBI",
            "SEBI",
            "MCA",
            "MoF",
            "NITI",
            "MOSPI",
            "ICAI",
            "ICMAI",
            "ICSI",
            "NFRA",
            "WorldBank",
            "IMF",
            "ADB",
            "OECD",
            "BIS",
        ]

    def score(self, paper, topic_terms=None):
        topic_terms = topic_terms or []

        text = " ".join([
            paper.title or "",
            paper.abstract or "",
            paper.research_domain or "",
            " ".join(paper.keywords or []),
        ]).lower()

        topic_score = self.topic_relevance_score(text, topic_terms)
        source_score = self.source_quality_score(paper.source)
        type_score = self.document_type_score(paper.document_type)
        recency_score = self.recency_score(paper.publication_year)

        total = round(
            topic_score * 0.45
            + source_score * 0.25
            + type_score * 0.15
            + recency_score * 0.15,
            2
        )

        return {
            "title": paper.title,
            "source": paper.source,
            "topic_score": topic_score,
            "source_score": source_score,
            "type_score": type_score,
            "recency_score": recency_score,
            "quality_score": total,
            "quality_label": self.label(total),
            "recommended_action": self.action(total, paper.source),
        }

    def topic_relevance_score(self, text, topic_terms):
        if not topic_terms:
            return 5

        matched = 0

        for term in topic_terms:
            if term.lower() in text:
                matched += 1

        return min(10, round((matched / len(topic_terms)) * 10, 2))

    def source_quality_score(self, source):
        if source in self.high_quality_sources:
            return 8

        if source in self.institutional_sources:
            return 6

        return 4

    def document_type_score(self, document_type):
        text = (document_type or "").lower()

        if "journal" in text or "article" in text:
            return 8

        if "working" in text or "preprint" in text:
            return 6

        if "report" in text or "policy" in text:
            return 5

        return 4

    def recency_score(self, year):
        try:
            y = int(year)
        except Exception:
            return 4

        if y >= 2020:
            return 8
        if y >= 2015:
            return 6
        if y >= 2010:
            return 5
        return 3

    def label(self, score):
        if score >= 7:
            return "High"
        if score >= 5:
            return "Medium"
        return "Low"

    def action(self, score, source):
        if source in self.institutional_sources:
            return "Save as institutional evidence"

        if score >= 7:
            return "Download PDF / include in core literature"

        if score >= 5:
            return "Keep metadata / review manually"

        return "Exclude from core literature"
