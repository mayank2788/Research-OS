from connectors.openalex.openalex_connector import OpenAlexConnector
from repository.knowledge_repository import (
    initialize_database,
    add_knowledge_object,
    count_knowledge_objects,
    list_knowledge_objects,
)
from research_intelligence.relevance_engine import AROSResearchRelevanceEngine


def run_intelligent_research_pipeline(
    query,
    max_results=10,
    minimum_score=30,
):
    initialize_database()

    connector = OpenAlexConnector()
    engine = AROSResearchRelevanceEngine()

    papers = connector.search(query, max_results=max_results)

    evaluated = []

    for paper in papers:
        result = engine.evaluate(paper)

        evaluated.append({
            "paper": paper,
            "evaluation": result,
        })

    evaluated.sort(
        key=lambda item: item["evaluation"]["relevance_score"],
        reverse=True,
    )

    saved_count = 0

    print("=" * 70)
    print("AROS INTELLIGENT RESEARCH PIPELINE")
    print("=" * 70)
    print(f"Query: {query}")
    print(f"Results fetched: {len(papers)}")
    print(f"Minimum score for repository save: {minimum_score}")

    print()
    print("Evaluated Papers")
    print("----------------")

    for item in evaluated:
        paper = item["paper"]
        evaluation = item["evaluation"]

        print()
        print("Title:", evaluation["title"])
        print("Score:", evaluation["relevance_score"])
        print("Label:", evaluation["relevance_label"])
        print("Primary Matches:", evaluation["primary_matches"])
        print("Secondary Matches:", evaluation["secondary_matches"])

        if evaluation["relevance_score"] >= minimum_score:
            record_id = add_knowledge_object(paper)
            saved_count += 1
            print(f"Saved to repository: YES | Record ID: {record_id}")
        else:
            print("Saved to repository: NO")

    print()
    print("Pipeline Summary")
    print("----------------")
    print(f"Saved papers: {saved_count}")
    print(f"Total repository objects: {count_knowledge_objects()}")

    print()
    print("Latest repository records")
    print("-------------------------")
    for row in list_knowledge_objects()[:10]:
        print(row)

    print()
    print("✓ AROS Intelligent Research Pipeline operational.")


if __name__ == "__main__":
    run_intelligent_research_pipeline(
        query="corporate finance debt management taxation",
        max_results=10,
        minimum_score=30,
    )
