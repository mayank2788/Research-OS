from research_intelligence.novelty_engine import ResearchNoveltyEngine


engine = ResearchNoveltyEngine()

ideas = [
    "AI based ESG governance and debt performance in Indian public sector energy companies",
    "Traditional corporate finance regression study on leverage and profitability",
]

print("=" * 70)
print("AROS RESEARCH NOVELTY ENGINE TEST")
print("=" * 70)

for idea in ideas:
    result = engine.score_idea(idea)

    print()
    print("Idea:", result["idea"])
    print("Scores:", result["scores"])
    print("Overall:", result["overall_score"])
    print("Q1 Potential:", result["q1_potential"])

print()
print("✓ Research Novelty Engine operational")
