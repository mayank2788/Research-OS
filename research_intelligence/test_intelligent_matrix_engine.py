from research_intelligence.intelligent_matrix_engine import (
    IntelligentMatrixEngine
)


engine = IntelligentMatrixEngine()


result = engine.build(
    output_type="Research_Papers",
    project_id="ind_as_23_borrowing_cost_research"
)


print("=" * 70)

print(
    "AROS INTELLIGENT MATRIX TEST"
)

print("=" * 70)


print(
    "Created:",
    result
)


print()

print(
    "✓ Intelligent Matrix Engine operational"
)
