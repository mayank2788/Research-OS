from project_workspace.knowledge_preservation_engine import (
    KnowledgePreservationEngine
)

from knowledge.knowledge_object import KnowledgeObject


engine = KnowledgePreservationEngine()


paper = KnowledgeObject(

    title=
    "Corporate Finance Research Test Paper",

    source="AROS Test",

    source_type="Journal",

    document_type="Article",

    research_domain="Finance",

    publication_year="2026",

    authors=[
        "Researcher A",
        "Researcher B"
    ],

    abstract=
    "This paper examines corporate finance decisions."

)


result = engine.preserve(

    paper,

    output_type="Research_Papers",

    project_id="generic_research_test",

    domain="Finance"

)


print("="*70)

print(
    "AROS KNOWLEDGE PRESERVATION ENGINE TEST"
)

print("="*70)


print(result)


print()

print(
    "✓ Knowledge Preservation Engine operational"
)

