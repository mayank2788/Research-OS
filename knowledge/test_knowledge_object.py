from knowledge.knowledge_object import KnowledgeObject

print("=" * 70)
print("AROS KNOWLEDGE OBJECT TEST")
print("=" * 70)

item = KnowledgeObject(
    title="Green Finance and Debt Management in Emerging Markets",
    source="OpenAlex",
    source_type="Academic Connector",
    document_type="Journal Article",
    research_domain="Green Financing",
    authors=["Sample Author One", "Sample Author Two"],
    publication_year="2024",
    doi="10.0000/sample-doi",
    abstract="This is a sample abstract for testing AROS Knowledge Object.",
    keywords=["Green Finance", "Debt Management", "Emerging Markets"],
    pdf_link="",
    open_access=False,
    confidence=0.75
)

print()
print("Knowledge Object Created")
print("------------------------")
print("Title  :", item.title)
print("Source :", item.source)
print("Domain :", item.research_domain)
print("Status :", item.status)

saved_file = item.save()

print()
print("Saved at:")
print(saved_file)

print()
print("JSON Preview")
print("------------")
print(item.to_json())

print()
print("Status")
print("------")
print("✓ Knowledge Object model working.")
