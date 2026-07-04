from pathlib import Path
import json

from research_intelligence.domain_router import DomainRouter
from project_workspace.project_manager import ResearchOutputProjectManager
from project_workspace.literature_collector import LiteratureCollector


class ResearchProjectEngine:
    """
    AROS Research Project Engine v1.

    Master controller connecting:

    Topic
      ->
    Domain Intelligence
      ->
    Source Selection
      ->
    Literature Collection
      ->
    Research Workspace
    """

    def __init__(self):

        self.router = DomainRouter()

        self.project_manager = ResearchOutputProjectManager()

        self.collector = LiteratureCollector()


    def create_project(
        self,
        topic,
        project_id,
        output_type="Research_Papers"
    ):

        routing = self.router.route(
            topic
        )


        workspace = (
            self.project_manager
            .create_project(
                title=project_id,
                output_type=output_type,
                research_question=topic
            )
        )


        report = self.collector.collect(
            query=topic,

            output_type=output_type,

            project_id=project_id,

            domain=", ".join(
                routing["domains"]
            )
        )


        project_summary = {

            "project_id": project_id,

            "topic": topic,

            "detected_domains":
                routing["domains"],

            "selected_sources":
                routing["sources"],

            "ranking_priority":
                routing["ranking_priority"],

            "workspace":
                workspace,

            "collection_report":
                report
        }


        summary_path = (
            Path("Research_Output")
            / output_type
            / "Working"
            / project_id
            / "project_summary.json"
        )


        summary_path.write_text(
            json.dumps(
                project_summary,
                indent=2,
                ensure_ascii=False
            ),
            encoding="utf-8"
        )


        return project_summary
