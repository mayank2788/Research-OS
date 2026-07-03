from connectors.semantic_scholar.semantic_scholar_connector import SemanticScholarConnector


print("=" * 70)
print("AROS SEMANTIC SCHOLAR CONNECTOR TEST")
print("=" * 70)

connector = SemanticScholarConnector()

papers = connector.search(
    "corporate finance debt management",
    max_results=5,
)

print()
print("Results:", len(papers))

for paper in papers:
    print()
    print("Title:", paper.title)
    print("Authors:", paper.authors[:3])
    print("Year:", paper.publication_year)
    print("DOI:", paper.doi)
    print("PDF/URL:", paper.pdf_link)
    print("Summary:", paper.ai_summary)

print()

if papers:
    print("✓ Semantic Scholar Connector operational.")
else:
    print("⚠ Semantic Scholar Connector created, but no live results returned.")

