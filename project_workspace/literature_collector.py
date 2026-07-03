import json
from pathlib import Path

from connectors.discovery_engine import AROSDiscoveryEngine
from project_workspace.pdf_library_manager import PDFLibraryManager
from research_intelligence.relevance_engine import AROSResearchRelevanceEngine


class LiteratureCollector:
    def __init__(self):
        self.discovery = AROSDiscoveryEngine()
        self.pdf_manager = PDFLibraryManager()
        self.relevance_engine = AROSResearchRelevanceEngine()

    def collect(
        self,
        query,
        output_type,
        project_id,
        domain,
        max_results_per_source=5,
        max_pdfs=10,
        impact_factor="NA"
    ):
        papers = self.discovery.search_all(
            query=query,
            max_results_per_source=max_results_per_source
        )

        evaluated = []

        for paper in papers:
            evaluation = self.relevance_engine.evaluate(paper)
            evaluated.append({
                "paper": paper,
                "evaluation": evaluation
            })

        evaluated.sort(
            key=lambda x: x["evaluation"]["relevance_score"],
            reverse=True
        )

        saved = []
        attempted = 0

        for item in evaluated:
            if len(saved) >= max_pdfs:
                break

            paper = item["paper"]

            if not paper.pdf_link:
                continue

            attempted += 1

            try:

                saved_path = self.pdf_manager.download_pdf(
                    url=paper.pdf_link,
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
                        "query": query,
                        "relevance": item["evaluation"]
                    }
                )


                if saved_path:
                    saved.append(str(saved_path))


            except Exception as error:

                print(
                    "PDF unavailable:",
                    paper.title
                )

                print(
                    "Reason:",
                    error
                )

                continue

        report = {
            "query": query,
            "total_discovered": len(papers),
            "download_attempts": attempted,
            "pdfs_saved": len(saved),
            "saved_files": saved,
        }

        report_folder = (
            Path("Research_Output")
            / output_type
            / "Researched_Library"
            / project_id
            / "02_Notes"
        )

        report_folder.mkdir(parents=True, exist_ok=True)

        report_path = report_folder / "literature_collection_report.json"

        report_path.write_text(
            json.dumps(report, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )

        return report
