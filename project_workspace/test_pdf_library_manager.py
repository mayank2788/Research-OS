from project_workspace.pdf_library_manager import (
    PDFLibraryManager
)


manager = PDFLibraryManager()


saved = manager.save_pdf(

    pdf_content=(
        b"%PDF-1.4\n"
        b"AROS PDF Library Test"
    ),

    output_type="Research_Papers",

    project_id=
    "ind_as_23_borrowing_cost_research",

    domain="Accounting",

    year="2024",

    title=(
        "Borrowing Cost Capitalisation "
        "and Financial Reporting Quality"
    ),

    impact_factor="NA",

    metadata={
        "test":
        "PDF manager validation"
    }
)


print("=" * 70)

print(
    "AROS PDF LIBRARY MANAGER TEST"
)

print("=" * 70)

print(
    "Saved:",
    saved
)

print()

print(
    "✓ PDF Library Manager operational"
)
