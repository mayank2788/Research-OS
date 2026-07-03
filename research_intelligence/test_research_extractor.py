from connectors.openalex.openalex_connector import OpenAlexConnector
from research_intelligence.research_extractor import ResearchIntelligenceExtractor


print("=" * 70)
print("AROS RESEARCH INTELLIGENCE EXTRACTION TEST")
print("=" * 70)


connector = OpenAlexConnector()

papers = connector.search(
    "corporate finance empirical regression",
    max_results=5
)


extractor = ResearchIntelligenceExtractor()


for paper in papers:

    intelligence = extractor.extract(paper)

    print()
    print("Title:", intelligence["title"])
    print("Research Type:", intelligence["possible_research_type"])
    print("Methodology:", intelligence["possible_methodology"])


print()
print("✓ Research Intelligence Extraction operational.")
