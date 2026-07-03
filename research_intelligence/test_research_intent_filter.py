from knowledge.knowledge_object import KnowledgeObject
from research_intelligence.research_intent_filter import ResearchIntentFilter


intent = {
    "must_have": [
        "ias 23",
        "borrowing costs",
        "ifrs"
    ],
    "preferred": [
        "earnings management",
        "financial reporting quality",
        "capitalization",
        "capitalisation"
    ],
    "exclude": [
        "financial literacy",
        "financial inclusion",
        "fintech"
    ]
}


papers = [
    KnowledgeObject(
        title="IAS 23 Borrowing Costs and Earnings Management under IFRS",
        source="Test",
        source_type="Academic",
        document_type="Journal Article",
        research_domain="accounting",
        abstract="This paper studies IAS 23, borrowing costs, IFRS and earnings management."
    ),

    KnowledgeObject(
        title="Financial Literacy and Financial Inclusion",
        source="Test",
        source_type="Academic",
        document_type="Journal Article",
        research_domain="finance",
        abstract="This paper studies financial literacy, financial inclusion and fintech."
    )
]


filter_engine = ResearchIntentFilter()

print("=" * 70)
print("AROS RESEARCH INTENT FILTER TEST")
print("=" * 70)

for paper in papers:
    result = filter_engine.score(paper, intent)

    print()
    print("Title:", paper.title)
    print("Score:", result["intent_score"])
    print("Label:", result["intent_label"])
    print("Decision:", result["decision"])
    print("Matched Must:", result["matched_must_have"])
    print("Matched Preferred:", result["matched_preferred"])
    print("Excluded:", result["excluded_terms"])

print()
print("✓ Research Intent Filter operational")
