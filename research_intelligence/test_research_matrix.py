from knowledge.knowledge_object import KnowledgeObject
from research_intelligence.research_matrix import ResearchMatrixGenerator


papers = [
    KnowledgeObject(
        title="Corporate Governance and Firm Performance using Panel Data",
        source="Test",
        source_type="Journal",
        document_type="Research Paper",
        research_domain="corporate governance finance",
        publication_year="2025",
        abstract="""
        This empirical study examines governance,
        firm performance and agency theory using
        panel data regression.
        """
    ),

    KnowledgeObject(
        title="AI Enabled Bibliometric Analysis in Management Research",
        source="Test",
        source_type="Journal",
        document_type="Review",
        research_domain="AI research methodology",
        publication_year="2026",
        abstract="""
        A systematic literature review using
        bibliometric analysis and machine learning.
        """
    )
]


generator = ResearchMatrixGenerator()
matrix = generator.generate_matrix(papers)


print("=" * 70)
print("AROS RESEARCH MATRIX TEST")
print("=" * 70)

for row in matrix:
    print()
    for key, value in row.items():
        print(key, ":", value)

print()
print("✓ Research Matrix Generator operational")
