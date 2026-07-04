from research_intelligence.source_mapper import SourceMapper


mapper = SourceMapper()

domain = "Taxation"

print("="*70)
print("AROS SOURCE MAPPER TEST")
print("="*70)

print("Domain:", domain)

print()

print(
    "Sources:",
    mapper.get_sources(domain)
)

print()

print(
    "Ranking:",
    mapper.get_ranking_priority(domain)
)

print()

print(
    "✓ Source Mapper operational"
)
