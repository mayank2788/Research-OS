from research_intelligence.research_matrix_engine import (
    ResearchMatrixEngine
)


engine = ResearchMatrixEngine()


result = engine.build_matrix(

    output_type="Research_Papers",

    project_id=
    "ind_as_23_borrowing_cost_research"

)


print("=" * 70)

print(
    "AROS RESEARCH MATRIX ENGINE TEST"
)

print("=" * 70)


print(
    "Matrix:",
    result
)


print()

print(
    "✓ Research Matrix Engine operational"
)

