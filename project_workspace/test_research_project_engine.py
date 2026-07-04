from project_workspace.research_project_engine import (
    ResearchProjectEngine
)


engine = ResearchProjectEngine()


result = engine.create_project(

    topic=(
        "Impact of Ind AS 23 Borrowing Cost "
        "Capitalisation on Earnings Management "
        "and Financial Reporting Quality"
    ),

    project_id=
    "ind_as_23_domain_driven_research"

)


print("=" * 70)

print(
    "AROS RESEARCH PROJECT ENGINE TEST"
)

print("=" * 70)


print(
    "Project:",
    result["project_id"]
)

print()

print(
    "Domains:",
    result["detected_domains"]
)

print()

print(
    "Sources:",
    result["selected_sources"]
)


print()

print(
    "PDF Saved:",
    result["collection_report"]["pdfs_saved"]
)


print()

print(
    "✓ Research Project Engine operational"
)

