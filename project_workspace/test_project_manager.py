from project_workspace.project_manager import ResearchOutputProjectManager


manager = ResearchOutputProjectManager()

metadata = manager.create_project(
    title="IND AS 23 Borrowing Cost Research",
    output_type="Research_Papers",
    research_question=(
        "How does borrowing cost capitalisation under IND AS 23 / IAS 23 "
        "relate to financial reporting quality, earnings management, "
        "corporate governance and investment efficiency?"
    )
)

print("=" * 70)
print("AROS RESEARCH OUTPUT LIBRARY TEST")
print("=" * 70)
print("Project ID:", metadata["project_id"])
print("Output Type:", metadata["output_type"])

print()
print("Stage Paths")
print("-" * 70)
for stage, path in metadata["stage_paths"].items():
    print(stage, ":", path)

print()
print("✓ Research Output Library operational")
