from connectors.openalex.openalex_connector import OpenAlexConnector
from repository.knowledge_repository import (
    initialize_database,
    save_knowledge_object,
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

    inserted_count = 0
    updated_count = 0
    existing_count = 0

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
            paper.ai_summary = (
                "AROS Research Evaluation\\n"
                f"Score: {evaluation['relevance_score']}\\n"
                f"Label: {evaluation['relevance_label']}\\n"
                f"Primary Matches: {evaluation['primary_matches']}\\n"
                f"Secondary Matches: {evaluation['secondary_matches']}\\n"
                f"Score Breakdown: {evaluation['score_breakdown']}"
            )
            paper.status = "evaluated"
            repository_result = save_knowledge_object(
                paper,
                return_status=True,
            )
            record_id = repository_result["record_id"]
            repository_status = repository_result["status"]

            if repository_status == "inserted":
                inserted_count += 1
            elif repository_status == "updated":
                updated_count += 1
            else:
                existing_count += 1

            print(
                f"{repository_status.upper():8} | "
                f"Record ID: {record_id}"
            )
        else:
            print("Saved to repository: NO")

    print()
    print("Pipeline Summary")
    print("----------------")
    print(f"Inserted papers: {inserted_count}")
    print(f"Updated papers: {updated_count}")
    print(f"Existing papers: {existing_count}")
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
