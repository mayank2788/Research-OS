from connectors.openalex.openalex_connector import OpenAlexConnector
from repository.knowledge_repository import (
    initialize_database,
    save_knowledge_object,
    count_knowledge_objects,
    list_knowledge_objects,
)

print("=" * 70)
print("AROS OPENALEX CONNECTOR TEST")
print("=" * 70)

initialize_database()

connector = OpenAlexConnector()

print()
print("Connector Info")
print("--------------")
print(connector.connector_info())

query = "debt management power sector India"
results = connector.search(query, max_results=5)

print()
print(f"Search Query: {query}")
print(f"Results returned: {len(results)}")

if not results:
    raise RuntimeError("OpenAlex returned no results.")

print()
print("Saving results to Knowledge Repository...")
for item in results:
    result = save_knowledge_object(
        item,
        return_status=True,
    )
    print(
        f"{result['status'].upper():8} | "
        f"Record ID: {result['record_id']} | "
        f"{item.title}"
    )

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
print("✓ OpenAlex connector working.")
print("✓ OpenAlex returned Knowledge Objects.")
print("✓ Knowledge Objects processed through lifecycle repository.")
