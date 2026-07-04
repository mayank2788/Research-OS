import json
from pathlib import Path


class JournalDomainFilterEngine:
    """
    AROS Journal Domain Filter Engine.

    Maps merged journal database into the frozen
    12-domain AROS journal taxonomy.
    """

    def __init__(self):
        self.taxonomy_path = Path(
            "journal_intelligence/domain_taxonomy.json"
        )

        self.input_path = Path(
            "journal_intelligence/processed/merged_journal_database.json"
        )

        self.output_path = Path(
            "journal_intelligence/domain_filtered/aros_domain_journals.json"
        )

        self.taxonomy = json.loads(
            self.taxonomy_path.read_text(encoding="utf-8")
        )

    def build_text(self, journal):
        parts = [
            journal.get("journal_name", ""),
            journal.get("publisher", ""),
            journal.get("country", ""),
            " ".join(journal.get("subject_categories", [])),
            " ".join(journal.get("source_registry", []))
        ]

        return " ".join(parts).lower()

    def classify(self, journal):
        text = self.build_text(journal)
        matched = []

        for domain, keywords in self.taxonomy["domains"].items():
            for keyword in keywords:
                if keyword.lower() in text:
                    matched.append(domain)
                    break

        return sorted(set(matched))

    def filter(self):
        data = json.loads(
            self.input_path.read_text(encoding="utf-8")
        )

        results = []

        for journal in data["journals"]:
            domains = self.classify(journal)

            if not domains:
                continue

            journal["aros_domains"] = domains
            results.append(journal)

        output = {
            "schema_version": "3.0",
            "source_unique_journals": data["unique_journals"],
            "domain_filtered_journals": len(results),
            "journals": results
        }

        self.output_path.write_text(
            json.dumps(output, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )

        return {
            "source_unique_journals": data["unique_journals"],
            "domain_filtered_journals": len(results),
            "output": str(self.output_path)
        }


if __name__ == "__main__":
    print(JournalDomainFilterEngine().filter())
