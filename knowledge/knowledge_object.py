from dataclasses import dataclass, asdict
from datetime import datetime
import json
from pathlib import Path
from typing import List, Optional


@dataclass
class KnowledgeObject:
    title: str
    source: str
    source_type: str
    document_type: str
    research_domain: str

    authors: Optional[List[str]] = None
    publication_year: Optional[str] = ""
    doi: Optional[str] = ""
    abstract: Optional[str] = ""
    keywords: Optional[List[str]] = None
    pdf_link: Optional[str] = ""
    open_access: Optional[bool] = False
    local_file: Optional[str] = ""
    ai_summary: Optional[str] = ""
    status: Optional[str] = "discovered"
    confidence: Optional[float] = 0.0
    date_added: Optional[str] = ""

    def __post_init__(self):
        if self.authors is None:
            self.authors = []
        if self.keywords is None:
            self.keywords = []
        if not self.date_added:
            self.date_added = datetime.now().isoformat(timespec="seconds")

    def to_dict(self):
        return asdict(self)

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)

    def save(self, folder="knowledge/objects"):
        Path(folder).mkdir(parents=True, exist_ok=True)

        safe_title = self.title.lower()
        safe_title = "".join(c if c.isalnum() else "-" for c in safe_title)
        safe_title = "-".join(safe_title.split("-"))[:80]

        file_path = Path(folder) / f"{safe_title}.json"

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(self.to_json())

        return file_path
