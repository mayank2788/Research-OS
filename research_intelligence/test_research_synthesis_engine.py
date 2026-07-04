from research_intelligence.research_synthesis_engine import (
    ResearchSynthesisEngine
)


engine = ResearchSynthesisEngine()


result = engine.synthesize(

    output_type="Research_Papers",

    project_id=
    "ind_as_23_borrowing_cost_research"

)


print("=" * 70)

print(
    "AROS RESEARCH SYNTHESIS ENGINE TEST"
)

print("=" * 70)


print(
    "Created:",
    result
)


print()


print(
    "✓ Research Synthesis Engine operational"
)

