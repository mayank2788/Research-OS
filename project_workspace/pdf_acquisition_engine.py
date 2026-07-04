import json
import hashlib
import re
from pathlib import Path

from project_workspace.pdf_resolver import PDFResolver
from project_workspace.pdf_library_manager import PDFLibraryManager


class PDFAcquisitionEngine:
    """
    AROS PDF Acquisition Engine v2.

    Preserves research knowledge even when
    full PDFs are unavailable.
    """

    def __init__(self):
        self.resolver = PDFResolver()
        self.pdf_manager = PDFLibraryManager()

    def clean_text(self, value, length=70):
        value = str(value or "NA")
        value = re.sub(r"[^A-Za-z0-9]+", "_", value)
        value = re.sub(r"_+", "_", value).strip("_")
        return value[:length]

    def acquire(
        self,
        paper,
        output_type,
        project_id,
        domain,
        impact_factor="NA"
    ):
        resolved_url = self.resolver.resolve(paper)

        if resolved_url:
            try:
                saved_pdf = self.pdf_manager.download_pdf(
                    url=resolved_url,
                    output_type=output_type,
                    project_id=project_id,
                    domain=domain,
                    year=paper.publication_year or "Year_NA",
                    title=paper.title,
                    impact_factor=impact_factor,
                    metadata={
                        "source": paper.source,
                        "doi": paper.doi,
                        "authors": paper.authors,
                    }
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
            project_id,
            domain
        )

    def save_metadata(
        self,
        paper,
        output_type,
        project_id,
        domain
    ):
        folder = (
            Path("Research_Output")
            / output_type
            / "Researched_Library"
            / project_id
            / "02_Metadata_Library"
        )

        folder.mkdir(parents=True, exist_ok=True)

        unique_text = (
            (paper.doi or "")
            + (paper.title or "")
            + (paper.source or "")
            + (paper.publication_year or "")
        )

        unique_id = hashlib.md5(
            unique_text.encode("utf-8")
        ).hexdigest()[:8]

        filename = (
            f"{self.clean_text(domain, 40)}_"
            f"{self.clean_text(paper.publication_year or 'Year_NA', 12)}_"
            f"{self.clean_text(paper.source, 30)}_"
            f"{self.clean_text(paper.title, 80)}_"
            f"{unique_id}.json"
        )

        file = folder / filename

        data = {
            "title": paper.title,
            "source": paper.source,
            "year": paper.publication_year,
            "doi": paper.doi,
            "authors": paper.authors,
            "abstract": paper.abstract,
            "research_domain": paper.research_domain,
            "pdf_status": "Not Available"
        }

        file.write_text(
            json.dumps(data, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )

        return {
            "status": "Metadata Saved",
            "path": str(file)
        }
