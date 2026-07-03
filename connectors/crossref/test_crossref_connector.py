from connectors.crossref.crossref_connector import CrossrefConnector


print("=" * 70)
print("AROS CROSSREF CONNECTOR TEST")
print("=" * 70)


connector = CrossrefConnector()

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


print()
print("✓ Crossref Connector operational.")
