from connectors.discovery_engine import AROSDiscoveryEngine

from research_intelligence.research_matrix import (
    ResearchMatrixGenerator
)

from research_intelligence.gap_analyzer import (
    ResearchGapAnalyzer
)

from research_intelligence.idea_generator import (
    ResearchIdeaGenerator
)


QUERY = (
    "Artificial Intelligence Corporate Governance "
    "Financial Performance"
)


print("="*70)
print("AROS FULL RESEARCH PIPELINE CASE STUDY")
print("="*70)

print()
print("Research Topic:")
print(QUERY)


print()
print("STEP 1: Discovering Knowledge Objects")

engine = AROSDiscoveryEngine()

papers = engine.search_all(
    QUERY,
    max_results_per_source=5
)

print(
    "Knowledge Objects:",
    len(papers)
)


print()
print("STEP 2: Creating Research Matrix")

matrix_engine = ResearchMatrixGenerator()

matrix = matrix_engine.generate_matrix(
    papers
)

print(
    "Matrix Rows:",
    len(matrix)
)


print()
print("STEP 3: Gap Analysis")

gap_engine = ResearchGapAnalyzer()

gaps = gap_engine.analyze(
    matrix
)

for key, value in gaps.items():

    print()
    print(key)
    print(value)


print()
print("STEP 4: Idea Generation")

idea_engine = ResearchIdeaGenerator()

ideas = idea_engine.generate(
    gaps
)


for idea in ideas[:5]:

    print()

    print(
        "Research Idea:",
        idea["idea"]
    )

    print(
        "Novelty Score:",
        idea["overall_score"]
    )

    print(
        "Potential:",
        idea["q1_potential"]
    )


print()
print("✓ FULL AROS RESEARCH PIPELINE COMPLETED")

