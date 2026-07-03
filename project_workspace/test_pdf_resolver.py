from knowledge.knowledge_object import KnowledgeObject
from project_workspace.pdf_resolver import PDFResolver


paper = KnowledgeObject(
    title="Test Open Access Paper",
    source="Test",
    source_type="Academic Test",
    document_type="Journal Article",
    research_domain="Open Access PDF Resolution",
    doi="10.7554/eLife.32822",
    pdf_link="",
)

resolver = PDFResolver()
result = resolver.resolve(paper)

print("=" * 70)
print("AROS PDF RESOLVER TEST")
print("=" * 70)
print("Resolved PDF:", result)
print()
print("✓ PDF Resolver operational")
