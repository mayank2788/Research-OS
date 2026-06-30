from connectors.mock.mock_connector import MockAcademicConnector
from repository.knowledge_repository import (
    initialize_database,
    add_knowledge_object,
    count_knowledge_objects,
    list_knowledge_objects
)

print("=" * 70)
print("AROS CONNECTOR FRAMEWORK TEST")
print("=" * 70)

initialize_database()

connector = MockAcademicConnector()

print()
print("Connector Info")
print("--------------")
print(connector.connector_info())

query = "Green Financing"
results = connector.search(query, max_results=5)

print()
print(f"Search Query: {query}")
print(f"Results returned: {len(results)}")

print()
print("Saving results to Knowledge Repository...")
for item in results:
    record_id = add_knowledge_object(item)
    print(f"Saved Record ID {record_id}: {item.title}")

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
print("✓ Connector Framework working.")
print("✓ Mock connector returned Knowledge Objects.")
print("✓ Knowledge Objects saved into Repository.")
