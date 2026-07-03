from knowledge.knowledge_object import KnowledgeObject
from research_intelligence.quality_filter import ResearchQualityFilter


topic_terms = [
    "ias 23",
    "borrowing costs",
    "capitalization",
    "financial reporting",
    "earnings management",
    "ifrs",
]

papers = [
    KnowledgeObject(
        title="IAS 23 Borrowing Costs and Earnings Management under IFRS",
        source="Crossref",
        source_type="Academic",
        document_type="Journal Article",
        research_domain="accounting reporting",
        publication_year="2024",
        abstract="This paper studies IAS 23, borrowing costs capitalization, IFRS and earnings management.",
    ),
    KnowledgeObject(
        title="Financial Literacy and Financial Inclusion",
        source="DOAJ",
        source_type="Academic",
        document_type="Journal Article",
        research_domain="finance",
        publication_year="2024",
        abstract="This paper studies financial inclusion and financial technology.",
    ),
    KnowledgeObject(
        title="IAS 23 borrowing costs capitalization - Ministry of Corporate Affairs Resource",
        source="MCA",
        source_type="Institutional",
        document_type="Policy / Report / Regulation",
        research_domain="accounting regulation",
        publication_year="",
        abstract="Institutional resource related to accounting regulation.",
    ),
]

quality = ResearchQualityFilter()

print("=" * 70)
print("AROS RESEARCH QUALITY FILTER TEST")
print("=" * 70)

for paper in papers:
    result = quality.score(paper, topic_terms=topic_terms)

    print()
    print("Title:", result["title"])
    print("Score:", result["quality_score"])
    print("Label:", result["quality_label"])
    print("Action:", result["recommended_action"])
    print("Breakdown:", {
        "topic": result["topic_score"],
        "source": result["source_score"],
        "type": result["type_score"],
        "recency": result["recency_score"],
    })

print()
print("✓ Research Quality Filter operational")
