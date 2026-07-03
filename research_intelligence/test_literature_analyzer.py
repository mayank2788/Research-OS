from research_intelligence.literature_analyzer import AROSLiteratureAnalyzer


analyzer = AROSLiteratureAnalyzer()

report = analyzer.build_literature_seed_report(
    topic="corporate finance",
    limit=20
)

print("=" * 70)
print("AROS LITERATURE INTELLIGENCE TEST")
print("=" * 70)

print()
print("Topic:", report["topic"])
print("Paper Count:", report["paper_count"])

print()
print("Suggested Review Structure")
print("--------------------------")
for theme in report["suggested_review_structure"]:
    print("-", theme)

print()
print("Themes and Papers")
print("-----------------")

for theme, papers in report["themes"].items():
    print()
    print(theme)
    print("-" * len(theme))

    for paper in papers:
        print(f"- {paper['title']} | Score: {paper['confidence']}")

print()
print("✓ AROS Literature Intelligence operational.")
