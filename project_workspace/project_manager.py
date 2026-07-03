import json
from datetime import datetime
from pathlib import Path


class ResearchOutputProjectManager:
    def __init__(self, registry_path="project_workspace/output_registry.json"):
        self.registry_path = Path(registry_path)
        self.registry = json.loads(self.registry_path.read_text(encoding="utf-8"))

    def safe_name(self, name):
        safe = name.lower()
        safe = "".join(c if c.isalnum() else "_" for c in safe)
        safe = "_".join(safe.split("_"))
        return safe[:80]

    def initialize_library(self):
        base = Path(self.registry["base_folder"])

        for output_type in self.registry["output_types"]:
            for stage in self.registry["stages"]:
                (base / output_type / stage).mkdir(parents=True, exist_ok=True)

        return base

    def create_project(self, title, output_type="Research_Papers", research_question=""):
        if output_type not in self.registry["output_types"]:
            raise ValueError(f"Invalid output type: {output_type}")

        self.initialize_library()

        project_id = self.safe_name(title)
        base = Path(self.registry["base_folder"]) / output_type

        stage_paths = {}

        for stage in self.registry["stages"]:
            project_path = base / stage / project_id
            project_path.mkdir(parents=True, exist_ok=True)

            for subfolder in self.registry["project_subfolders"]:
                (project_path / subfolder).mkdir(parents=True, exist_ok=True)

            stage_paths[stage] = str(project_path)

        metadata = {
            "title": title,
            "project_id": project_id,
            "output_type": output_type,
            "research_question": research_question,
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "stage_paths": stage_paths
        }

        working_path = Path(stage_paths["Working"])

        (working_path / "project_metadata.json").write_text(
            json.dumps(metadata, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )

        (working_path / "README.md").write_text(
            f"# {title}\n\n"
            f"Output Type: {output_type}\n\n"
            f"Research Question:\n\n{research_question}\n",
            encoding="utf-8"
        )

        return metadata
