from research_intelligence.research_strategy_engine import (
    ResearchStrategyEngine
)


engine = ResearchStrategyEngine()


result = engine.generate(

    output_type="Research_Papers",

    project_id=
    "ind_as_23_borrowing_cost_research"

)


print("=" * 70)

print(
    "AROS RESEARCH STRATEGY ENGINE TEST"
)

print("=" * 70)


print(
    "Created:",
    result
)


print()


print(
    "✓ Research Strategy Engine operational"
)

