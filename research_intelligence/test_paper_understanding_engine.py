from types import SimpleNamespace

from research_intelligence.paper_understanding_engine import (
    PaperUnderstandingEngine
)


paper = SimpleNamespace(

    title=
    "Capital Structure and Firm Performance using Panel Data Regression",

    abstract=
    """
    This study examines leverage,
    profitability and firm value.

    Panel data regression is applied.

    The study provides evidence and
    future research opportunities.
    """,

    ai_summary=""

)


engine = PaperUnderstandingEngine()


result = engine.understand(
    paper
)


print("=" * 70)

print(
    "AROS PAPER UNDERSTANDING ENGINE TEST"
)

print("=" * 70)


for key, value in result.items():

    print(
        key,
        ":",
        value
    )


print()

print(
    "✓ Paper Understanding Engine operational"
)

