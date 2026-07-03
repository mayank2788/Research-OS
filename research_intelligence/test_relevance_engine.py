from connectors.openalex.openalex_connector import OpenAlexConnector
from research_intelligence.relevance_engine import AROSResearchRelevanceEngine


print("=" * 70)
print("AROS RESEARCH RELEVANCE ENGINE V2.1 TEST")
print("=" * 70)

connector = OpenAlexConnector()

papers = connector.search(
    "corporate finance debt management taxation",
    max_results=5
)

engine = AROSResearchRelevanceEngine()

for paper in papers:
    result = engine.evaluate(paper)

    print()
    print("Title:", result["title"])
    print("Score:", result["relevance_score"])
    print("Label:", result["relevance_label"])
    print("Primary Matches:", result["primary_matches"])
    print("Secondary Matches:", result["secondary_matches"])
    print("Breakdown:", result["score_breakdown"])

print()
print("✓ AROS Research Relevance Engine v2.1 operational.")
