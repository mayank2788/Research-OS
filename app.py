from pathlib import Path
from datetime import datetime
import csv
from pypdf import PdfReader

SOURCE = Path.home() / "Documents/GitHub/Research-Papers"
REPORTS = Path("reports")
LOGS = Path("logs")

REPORTS.mkdir(exist_ok=True)
LOGS.mkdir(exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
csv_report = REPORTS / f"aros-inventory-{timestamp}.csv"
md_report = REPORTS / f"aros-summary-{timestamp}.md"
log_file = LOGS / f"aros-log-{timestamp}.txt"

SUPPORTED = [".pdf", ".docx", ".xlsx", ".pptx", ".md", ".txt", ".py"]

def log(message):
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} | {message}\n")

def get_pdf_info(file_path):
    try:
        reader = PdfReader(str(file_path))
        metadata = reader.metadata or {}
        return {
            "pages": len(reader.pages),
            "title": metadata.get("/Title", ""),
            "author": metadata.get("/Author", "")
        }
    except Exception as e:
        log(f"PDF read failed: {file_path} | {e}")
        return {"pages": "", "title": "", "author": ""}

def scan_library():
    records = []

    for file in SOURCE.rglob("*"):
        if file.is_file():
            ext = file.suffix.lower()
            if ext in SUPPORTED:
                record = {
                    "file_name": file.name,
                    "extension": ext,
                    "folder": str(file.parent),
                    "size_kb": round(file.stat().st_size / 1024, 2),
                    "modified": datetime.fromtimestamp(file.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                    "pdf_pages": "",
                    "pdf_title": "",
                    "pdf_author": ""
                }

                if ext == ".pdf":
                    pdf_info = get_pdf_info(file)
                    record["pdf_pages"] = pdf_info["pages"]
                    record["pdf_title"] = pdf_info["title"]
                    record["pdf_author"] = pdf_info["author"]

                records.append(record)

    return records

def write_csv(records):
    with open(csv_report, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)

def write_markdown(records):
    total = len(records)
    pdfs = sum(1 for r in records if r["extension"] == ".pdf")

    with open(md_report, "w", encoding="utf-8") as f:
        f.write("# AROS Research Library Summary\n\n")
        f.write(f"Generated: {datetime.now()}\n\n")
        f.write(f"Source folder: `{SOURCE}`\n\n")
        f.write("## Summary\n\n")
        f.write(f"- Total supported files: {total}\n")
        f.write(f"- PDF files: {pdfs}\n")
        f.write(f"- CSV report: `{csv_report}`\n")
        f.write(f"- Log file: `{log_file}`\n\n")
        f.write("## File Types\n\n")

        counts = {}
        for r in records:
            counts[r["extension"]] = counts.get(r["extension"], 0) + 1

        for ext, count in sorted(counts.items()):
            f.write(f"- {ext}: {count}\n")

def main():
    print("=" * 70)
    print("AROS - AI RESEARCH OPERATING SYSTEM")
    print("=" * 70)

    log("AROS scan started")
    records = scan_library()

    if not records:
        print("No supported files found.")
        log("No supported files found")
        return

    write_csv(records)
    write_markdown(records)

    log("AROS scan completed")

    print()
    print("Scan completed successfully.")
    print("Files scanned:", len(records))
    print()
    print("CSV report:", csv_report)
    print("Markdown summary:", md_report)
    print("Log file:", log_file)
    print()
    print("No files were moved, renamed, or deleted.")

if __name__ == "__main__":
    main()
