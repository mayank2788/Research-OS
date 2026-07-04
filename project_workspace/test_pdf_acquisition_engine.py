from project_workspace.pdf_acquisition_engine import (
    PDFAcquisitionEngine
)

from knowledge.knowledge_object import KnowledgeObject


engine = PDFAcquisitionEngine()


paper = KnowledgeObject(

    title=
    "IAS 23 Borrowing Costs and Reporting Quality",

    source="Test",

    source_type="Journal",

    document_type="Article",

    research_domain="Accounting",

    doi="",

    pdf_link="",

    publication_year="2025",

    authors=["AROS Test"]

)


result = engine.acquire(

    paper,

    output_type="Research_Papers",

    project_id=
    "ind_as_23_domain_driven_research",

    domain="Accounting"

)


print("=" * 70)

print(
    "AROS PDF ACQUISITION ENGINE TEST"
)

print("=" * 70)


print(result)


print()

print(
    "✓ PDF Acquisition Engine operational"
)

