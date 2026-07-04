import json
from pathlib import Path
from openpyxl import Workbook


SOURCE = Path("journal_intelligence/journal_master_database.json")

OUTPUT = Path(
    "Research_Output/Research_Infrastructure/Journal_Intelligence"
)

OUTPUT.mkdir(parents=True, exist_ok=True)


def main():
    data = json.loads(SOURCE.read_text(encoding="utf-8"))

    export_json = OUTPUT / "journal_master_database.json"
    export_json.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    wb = Workbook()
    ws = wb.active
    ws.title = "Journal Master Database"

    headers = [
        "Journal Name",
        "Publisher",
        "Institution",
        "Country",
        "Domains",
        "Ranking Tags",
        "Access Type",
        "URL"
    ]

    ws.append(headers)

    for journal in data["journals"]:
        ws.append([
            journal.get("journal_name", ""),
            journal.get("publisher", ""),
            journal.get("institution", ""),
            journal.get("country", ""),
            ", ".join(journal.get("domains", [])),
            ", ".join(journal.get("ranking_tags", [])),
            journal.get("access_type", ""),
            journal.get("url", "")
        ])

    for col in ws.columns:
        max_length = 0
        col_letter = col[0].column_letter

        for cell in col:
            value = str(cell.value or "")
            max_length = max(max_length, len(value))

        ws.column_dimensions[col_letter].width = min(max_length + 2, 45)

    ws.freeze_panes = "A2"

    export_xlsx = OUTPUT / "journal_master_database.xlsx"
    wb.save(export_xlsx)

    print("✓ Journal database exported")
    print("JSON:", export_json)
    print("Excel:", export_xlsx)


if __name__ == "__main__":
    main()
