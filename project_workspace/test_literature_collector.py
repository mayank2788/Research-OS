from project_workspace.literature_collector import LiteratureCollector


collector = LiteratureCollector()

report = collector.collect(
    query=(
        "IAS 23 borrowing costs capitalization "
        "financial reporting earnings management"
    ),
    output_type="Research_Papers",
    project_id="ind_as_23_borrowing_cost_research",
    domain="Accounting",
    max_results_per_source=3,
    max_pdfs=10,
    impact_factor="NA"
)

print("=" * 70)
print("AROS LITERATURE COLLECTION PIPELINE TEST")
print("=" * 70)

for key, value in report.items():
    print(key, ":", value)

print()
print("✓ Literature Collection Pipeline completed")
