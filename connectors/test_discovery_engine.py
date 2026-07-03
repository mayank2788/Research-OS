from connectors.discovery_engine import AROSDiscoveryEngine


print("=" * 70)
print("AROS MULTI-SOURCE DISCOVERY ENGINE TEST")
print("=" * 70)

engine = AROSDiscoveryEngine()

results = engine.search_all(
    query="corporate debt management",
    max_results_per_source=5,
)

print()
print("Unique Results:", len(results))

for item in results:
    print()
    print("Title:", item.title)
    print("Source:", item.source)
    print("Year:", item.publication_year)
    print("DOI:", item.doi)

print()
print("✓ AROS Multi-Source Discovery Engine operational.")
