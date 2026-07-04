from research_intelligence.research_extractor import (
    ResearchIntelligenceExtractor
)
from research_intelligence.source_mapper import SourceMapper
from knowledge.knowledge_object import KnowledgeObject


class DomainRouter:
    """
    AROS Domain Router v1.

    Purpose:
    Converts a research topic into:
    - likely research domains
    - suitable sources
    - ranking priorities
    """

    def __init__(self):
        self.extractor = ResearchIntelligenceExtractor()
        self.mapper = SourceMapper()

    def route(self, topic):
        topic_object = KnowledgeObject(
            title=topic,
            source="User Topic",
            source_type="Research Topic",
            document_type="Research Query",
            research_domain=topic,
            abstract=topic,
            keywords=[topic],
        )

        intelligence = self.extractor.extract(topic_object)

        domains = [
            item["domain"]
            for item in intelligence["domains"]
        ]

        sources = []
        ranking = []

        for domain in domains:
            sources.extend(
                self.mapper.get_sources(domain)
            )

            ranking.extend(
                self.mapper.get_ranking_priority(domain)
            )

        return {
            "topic": topic,
            "domains": domains,
            "sources": sorted(set(sources)),
            "ranking_priority": sorted(set(ranking)),
            "intelligence": intelligence,
        }
