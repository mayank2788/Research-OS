import json
import re
from pathlib import Path


class JournalMergeEngine:
    """
    AROS Journal Merge Engine v1.

    Merges:
    - SCImago
    - DOAJ
    - UGC CARE
    - ABDC

    Matching priority:
    1. ISSN / EISSN
    2. Normalized title fallback
    """

    def __init__(self):
        self.processed = Path("journal_intelligence/processed")
        self.output = self.processed / "merged_journal_database.json"

    def clean_key(self, value):
        value = str(value or "").lower()
        value = re.sub(r"[^a-z0-9]+", "", value)
        return value.strip()

    def issn_key(self, journal):
        issn = journal.get("issn") or journal.get("eissn") or ""
        issn = str(issn).replace("-", "").strip().lower()
        return f"issn:{issn}" if issn else ""

    def title_key(self, journal):
        return f"title:{self.clean_key(journal.get('journal_name'))}"

    def make_key(self, journal):
        return self.issn_key(journal) or self.title_key(journal)

    def load_json(self, filename):
        path = self.processed / filename
        if not path.exists():
            return []
        return json.loads(path.read_text(encoding="utf-8"))

    def merge_field(self, existing, new, field):
        if not existing.get(field) and new.get(field):
            existing[field] = new.get(field)

    def merge_list(self, existing, new, field):
        values = set(existing.get(field, []))
        values.update(new.get(field, []))
        existing[field] = sorted(values)

    def merge_dict(self, existing, new, field):
        existing.setdefault(field, {})
        for k, v in new.get(field, {}).items():
            if v not in ["", None, [], {}]:
                existing[field][k] = v

    def merge_journal(self, existing, new):
        for field in [
            "journal_name",
            "issn",
            "eissn",
            "publisher",
            "country"
        ]:
            self.merge_field(existing, new, field)

        for field in [
            "source_registry",
            "subject_categories",
            "aros_domains"
        ]:
            self.merge_list(existing, new, field)

        for field in [
            "ranking",
            "access",
            "urls",
            "verification"
        ]:
            self.merge_dict(existing, new, field)

        return existing

    def normalize_base(self, journal):
        return {
            "journal_name": journal.get("journal_name", ""),
            "issn": journal.get("issn", ""),
            "eissn": journal.get("eissn", ""),
            "publisher": journal.get("publisher", ""),
            "country": journal.get("country", ""),
            "source_registry": journal.get("source_registry", []),
            "subject_categories": journal.get("subject_categories", []),
            "aros_domains": journal.get("aros_domains", []),
            "ranking": journal.get("ranking", {}),
            "access": journal.get("access", {}),
            "urls": journal.get("urls", {}),
            "verification": journal.get("verification", {})
        }

    def merge(self):
        sources = [
            "scimago_normalized.json",
            "doaj_normalized.json",
            "ugc_care_normalized.json",
            "abdc_normalized.json"
        ]

        merged = {}

        raw_count = 0

        for source in sources:
            journals = self.load_json(source)
            raw_count += len(journals)

            for journal in journals:
                key = self.make_key(journal)

                if not key:
                    continue

                base = self.normalize_base(journal)

                if key not in merged:
                    merged[key] = base
                else:
                    merged[key] = self.merge_journal(
                        merged[key],
                        base
                    )

        output_data = {
            "schema_version": "3.0",
            "raw_records": raw_count,
            "unique_journals": len(merged),
            "journals": list(merged.values())
        }

        self.output.write_text(
            json.dumps(output_data, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )

        return {
            "raw_records": raw_count,
            "unique_journals": len(merged),
            "output": str(self.output)
        }


if __name__ == "__main__":
    print(JournalMergeEngine().merge())
