from pathlib import Path
from datetime import datetime
from pypdf import PdfReader

REPORT_FOLDER = Path("extracted_text")
REPORT_FOLDER.mkdir(exist_ok=True)

def clean_text(text):
    if not text:
        return ""
    return " ".join(text.split())

def read_pdf(pdf_path):
    pdf_path = Path(pdf_path)

    try:
        reader = PdfReader(str(pdf_path))
        pages = len(reader.pages)

        extracted_text = []

        for page in reader.pages:
            text = page.extract_text()
            extracted_text.append(clean_text(text))

        full_text = "\n\n".join(extracted_text)
        word_count = len(full_text.split())
        reading_time = round(word_count / 200, 1)

        return {
            "file_name": pdf_path.name,
            "file_path": str(pdf_path),
            "pages": pages,
            "word_count": word_count,
            "estimated_reading_time_minutes": reading_time,
            "text_preview": full_text[:1000],
            "status": "success"
        }

    except Exception as error:
        return {
            "file_name": pdf_path.name,
            "file_path": str(pdf_path),
            "pages": "",
            "word_count": "",
            "estimated_reading_time_minutes": "",
            "text_preview": "",
            "status": f"failed: {error}"
        }

def save_text_report(pdf_info):
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    safe_name = pdf_info["file_name"].replace(" ", "_").replace("/", "_")
    output_file = REPORT_FOLDER / f"{safe_name}-{timestamp}.txt"

    with open(output_file, "w", encoding="utf-8") as file:
        file.write("AROS PDF READER REPORT\n")
        file.write("=" * 60 + "\n\n")
        file.write(f"File Name: {pdf_info['file_name']}\n")
        file.write(f"File Path: {pdf_info['file_path']}\n")
        file.write(f"Pages: {pdf_info['pages']}\n")
        file.write(f"Word Count: {pdf_info['word_count']}\n")
        file.write(f"Estimated Reading Time: {pdf_info['estimated_reading_time_minutes']} minutes\n")
        file.write(f"Status: {pdf_info['status']}\n\n")
        file.write("TEXT PREVIEW\n")
        file.write("-" * 60 + "\n")
        file.write(pdf_info["text_preview"])

    return output_file
