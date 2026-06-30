from knowledge.knowledge_object import KnowledgeObject
from repository.knowledge_repository import (
    initialize_database,
    add_knowledge_object,
    list_knowledge_objects,
    count_knowledge_objects
)

print("=" * 70)
print("AROS KNOWLEDGE REPOSITORY TEST")
print("=" * 70)

initialize_database()

item = KnowledgeObject(
    title="AI in Finance and Capital Markets",
    source="OpenAlex",
    source_type="Academic Connector",
    document_type="Journal Article",
    research_domain="Artificial Intelligence in Finance",
    authors=["Sample Researcher"],
    publication_year="2025",
    doi="10.0000/aros-test",
    abstract="Sample test record for AROS Knowledge Repository.",
    keywords=["AI in Finance", "Capital Markets", "FinTech"],
    open_access=False,
    confidence=0.80
)

record_id = add_knowledge_object(item)

print()
print("Record inserted successfully.")
print("Record ID:", record_id)

print()
print("Total records in repository:", count_knowledge_objects())

print()
print("Latest records")
print("--------------")

for row in list_knowledge_objects()[:10]:
    print(row)

print()
print("Status")
print("------")
print("✓ SQLite database created.")
print("✓ Knowledge Object stored.")
print("✓ Repository is working.")
