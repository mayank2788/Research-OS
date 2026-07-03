from research_intelligence.idea_generator import (
    ResearchIdeaGenerator
)


gap = {

    "dominant_domains": [
        ("Corporate Governance", 10)
    ],

    "dominant_methods": [
        ("Regression Analysis", 8)
    ],

    "dominant_variables": [
        ("firm performance", 7)
    ]
}


generator = ResearchIdeaGenerator()

ideas = generator.generate(gap)


print("="*70)
print("AROS RESEARCH IDEA GENERATOR TEST")
print("="*70)


for idea in ideas:

    print()

    print(
        "Idea:",
        idea["idea"]
    )

    print(
        "Novelty:",
        idea["overall_score"]
    )

    print(
        "Q1 Potential:",
        idea["q1_potential"]
    )


print()
print("✓ Research Idea Generator operational")

