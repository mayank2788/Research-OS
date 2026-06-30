from connectors.base.base_connector import BaseConnector
from knowledge.knowledge_object import KnowledgeObject

class MockAcademicConnector(BaseConnector):
    def __init__(self):
        super().__init__("Mock Academic Connector")

    def search(self, query, max_results=10):
        results = []

        for i in range(1, max_results + 1):
            item = KnowledgeObject(
                title=f"{query} - Sample Research Paper {i}",
                source=self.name,
                source_type="Mock Connector",
                document_type="Journal Article",
                research_domain=query,
                authors=[f"Sample Author {i}"],
                publication_year="2026",
                doi=f"10.0000/mock-{i}",
                abstract=f"This is a mock abstract for {query}, paper {i}.",
                keywords=[query, "Research", "Finance"],
                open_access=False,
                confidence=0.50
            )
            results.append(item)

        return results
