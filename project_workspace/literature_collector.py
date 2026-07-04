import json
from pathlib import Path

from connectors.discovery_engine import AROSDiscoveryEngine
from project_workspace.pdf_acquisition_engine import PDFAcquisitionEngine
from research_intelligence.relevance_engine import AROSResearchRelevanceEngine
from research_intelligence.quality_filter import ResearchQualityFilter
from research_intelligence.research_intent_filter import ResearchIntentFilter
from project_workspace.pdf_resolver import PDFResolver


class LiteratureCollector:
    def __init__(self):
        self.discovery = AROSDiscoveryEngine()
        self.acquisition_engine = PDFAcquisitionEngine()
        self.relevance_engine = AROSResearchRelevanceEngine()
        self.quality_filter = ResearchQualityFilter()
        self.intent_filter = ResearchIntentFilter()
        self.pdf_resolver = PDFResolver()

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

        
        intent = {
            "must_have": [
                "ias 23",
                "borrowing costs",
                "ifrs"
            ],

            "preferred": [
                "earnings management",
                "financial reporting quality",
                "capitalization",
                "capitalisation"
            ],

            "exclude": [
                "financial literacy",
                "financial inclusion",
                "fintech"
            ]
        }

        topic_terms = (
            intent["must_have"]
            + intent["preferred"]
        )


        for paper in papers:

            intent_result = self.intent_filter.score(
                paper,
                intent
            )


            if intent_result["decision"] == "Reject":
                continue


            quality = self.quality_filter.score(
                paper,
                topic_terms=topic_terms
            )

            if quality["recommended_action"] == "Exclude from core literature":
                continue


            evaluation = self.relevance_engine.evaluate(
                paper
            )


            evaluated.append(
                {
                    "paper": paper,
                    "evaluation": evaluation,
                    "quality": quality,
                }
            )


        evaluated.sort(
            key=lambda x: x["quality"]["quality_score"],
            reverse=True
        )

        saved = []
        attempted = 0

        for item in evaluated:
            if len(saved) >= max_pdfs:
                break

            paper = item["paper"]

            if item["quality"]["recommended_action"] == "Save as institutional evidence":
                continue

            resolved_url = self.pdf_resolver.resolve(paper)

            if not resolved_url:
                continue

            attempted += 1

            try:

                acquisition = self.acquisition_engine.acquire(
                    paper=paper,
                    output_type=output_type,
                    project_id=project_id,
                    domain=domain,
                    impact_factor=impact_factor
                )


                saved.append(
                    acquisition
                )


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
            "items_preserved": len(saved),
            "pdfs_saved": len(
                [
                    x for x in saved
                    if x.get("status") == "PDF Saved"
                ]
            ),
            "metadata_saved": len(
                [
                    x for x in saved
                    if x.get("status") == "Metadata Saved"
                ]
            ),
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
