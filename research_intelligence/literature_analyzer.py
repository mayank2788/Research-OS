from research_workspace.research_query_layer import AROSResearchWorkspace


class AROSLiteratureAnalyzer:
    """
    Literature Intelligence module.

    Version 1:
    - Builds literature review seed report
    - Groups papers into simple research themes
    - Identifies high-level review structure
    """

    def __init__(self):
        self.workspace = AROSResearchWorkspace()

    def infer_theme(self, title):
        text = title.lower()

        if "tax" in text or "taxation" in text:
            return "Taxation and Corporate Decisions"

        if "debt" in text:
            return "Debt, Capital Structure and Financing"

        if "finance" in text or "financial" in text:
            return "Corporate Finance and Financial Management"

        if "governance" in text:
            return "Corporate Governance"

        if "esg" in text or "sustainability" in text:
            return "ESG, Sustainability and Finance"

        return "General Management and Economics"

    def build_literature_seed_report(self, topic, limit=20):
        papers = self.workspace.literature_review_seed(topic, limit=limit)

        themes = {}

        for paper in papers:
            title, source, research_domain, confidence = paper

            theme = self.infer_theme(title)

            themes.setdefault(theme, []).append({
                "title": title,
                "source": source,
                "research_domain": research_domain,
                "confidence": confidence,
            })

        return {
            "topic": topic,
            "paper_count": len(papers),
            "themes": themes,
            "suggested_review_structure": list(themes.keys()),
        }
