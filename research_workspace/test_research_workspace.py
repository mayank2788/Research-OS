from research_workspace.research_query_layer import AROSResearchWorkspace


workspace = AROSResearchWorkspace()


print("=" * 70)
print("AROS RESEARCH WORKSPACE TEST")
print("=" * 70)


print()
print("Highest Relevance Papers")
print("------------------------")

for row in workspace.highest_relevance_papers(5):
    print(row)


print()
print("Taxation Collection")
print("-------------------")

for row in workspace.search_domain("taxation")[:5]:
    print(row)


print()
print("Literature Review Seed: Corporate Finance")
print("-----------------------------------------")

for row in workspace.literature_review_seed("corporate finance"):
    print(row)


print()
print("✓ AROS Research Workspace operational.")
