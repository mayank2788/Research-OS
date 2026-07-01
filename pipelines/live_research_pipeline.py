from pathlib import Path

from reader.pdf_reader import read_pdf, save_text_report
from knowledge.knowledge_object import KnowledgeObject
from repository.knowledge_repository import (
    initialize_database,
    add_knowledge_object,
    count_knowledge_objects,
)


def build_knowledge_object_from_pdf(pdf_path, research_domain):
    pdf_info = read_pdf(pdf_path)

    if pdf_info["status"] != "success":
        raise RuntimeError(f"PDF reading failed: {pdf_info['status']}")

    report_path = save_text_report(pdf_info)

    return KnowledgeObject(
        title=Path(pdf_path).stem.replace("_", " "),
        source="Local Research-Papers Library",
        source_type="Local PDF",
        document_type="Research Paper",
        research_domain=research_domain,
        authors=[],
        publication_year="",
        doi="",
        abstract=pdf_info["text_preview"],
        keywords=[research_domain],
        pdf_link="",
        open_access=False,
        local_file=str(pdf_path),
        ai_summary=(
            f"PDF processed successfully. Pages: {pdf_info['pages']}. "
            f"Word count: {pdf_info['word_count']}. "
            f"Estimated reading time: {pdf_info['estimated_reading_time_minutes']} minutes. "
            f"Text report saved at: {report_path}"
        ),
        status="ingested",
        confidence=0.70,
    )


def run_pipeline(pdf_path, research_domain):
    initialize_database()

    knowledge_object = build_knowledge_object_from_pdf(
        pdf_path=pdf_path,
        research_domain=research_domain,
    )

    json_path = knowledge_object.save()
    inserted_id = add_knowledge_object(knowledge_object)
    total_count = count_knowledge_objects()

    print("AROS LIVE RESEARCH PIPELINE COMPLETE")
    print("=" * 60)
    print(f"PDF: {pdf_path}")
    print(f"Research Domain: {research_domain}")
    print(f"Knowledge Object JSON: {json_path}")
    print(f"Repository Insert ID: {inserted_id}")
    print(f"Total Repository Objects: {total_count}")


if __name__ == "__main__":
    run_pipeline(
        pdf_path="/Users/anamika/Documents/GitHub/Research-Papers/Submitted Papers/AN_APPROACH_TO_PERFORMANCE_OF_MFI_USING.pdf",
        research_domain="Microfinance Performance",
    )
