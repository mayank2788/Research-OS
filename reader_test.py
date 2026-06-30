from pathlib import Path
from reader.pdf_reader import read_pdf, save_text_report

SOURCE = Path.home() / "Documents/GitHub/Research-Papers"

print("=" * 70)
print("AROS READER TEST")
print("=" * 70)

pdf_files = list(SOURCE.rglob("*.pdf"))

if not pdf_files:
    print("No PDF files found.")
else:
    test_pdf = pdf_files[0]
    print("Testing PDF:")
    print(test_pdf)

    result = read_pdf(test_pdf)

    print()
    print("Reader Result")
    print("-------------")
    print("File Name :", result["file_name"])
    print("Pages     :", result["pages"])
    print("Words     :", result["word_count"])
    print("Reading   :", result["estimated_reading_time_minutes"], "minutes")
    print("Status    :", result["status"])

    report = save_text_report(result)

    print()
    print("Text preview report saved at:")
    print(report)

    print()
    print("No files were moved, renamed, or deleted.")
