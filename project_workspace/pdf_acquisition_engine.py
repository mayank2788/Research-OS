import json
from pathlib import Path

from project_workspace.pdf_resolver import PDFResolver
from project_workspace.pdf_library_manager import PDFLibraryManager


class PDFAcquisitionEngine:
    """
    AROS PDF Acquisition Engine v2.

    Purpose:
    Preserve research knowledge even when
    full PDFs are unavailable.

    Pipeline:
    1. Resolve legal PDF
    2. Save PDF when available
    3. Preserve metadata otherwise
    """

    def __init__(self):

        self.resolver = PDFResolver()

        self.pdf_manager = PDFLibraryManager()


    def acquire(
        self,
        paper,
        output_type,
        project_id,
        domain,
        impact_factor="NA"
    ):

        resolved_url = self.resolver.resolve(
            paper
        )


        if resolved_url:

            try:

                saved_pdf = (
                    self.pdf_manager.download_pdf(
                        url=resolved_url,
                        output_type=output_type,
                        project_id=project_id,
                        domain=domain,
                        year=(
                            paper.publication_year
                            or "Year_NA"
                        ),
                        title=paper.title,
                        impact_factor=impact_factor,
                        metadata={
                            "source": paper.source,
                            "doi": paper.doi,
                            "authors": paper.authors,
                        }
                    )
                )


                return {
                    "status": "PDF Saved",
                    "path": str(saved_pdf)
                }


            except Exception:
                pass


        return self.save_metadata(
            paper,
            output_type,
            project_id
        )


    def save_metadata(
        self,
        paper,
        output_type,
        project_id
    ):

        folder = (
            Path("Research_Output")
            / output_type
            / "Researched_Library"
            / project_id
            / "02_Metadata_Library"
        )


        folder.mkdir(
            parents=True,
            exist_ok=True
        )


        file = (
            folder
            / (
                paper.title[:80]
                .replace("/", "_")
                + ".json"
            )
        )


        data = {
            "title": paper.title,
            "source": paper.source,
            "year": paper.publication_year,
            "doi": paper.doi,
            "authors": paper.authors,
            "abstract": paper.abstract,
            "pdf_status": "Not Available"
        }


        file.write_text(
            json.dumps(
                data,
                indent=2,
                ensure_ascii=False
            ),
            encoding="utf-8"
        )


        return {
            "status": "Metadata Saved",
            "path": str(file)
        }
