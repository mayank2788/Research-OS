import json
from pathlib import Path

from literature_acquisition.downloaders.pdf_downloader import PDFDownloader


class BulkPDFDownloader:
    def __init__(self):
        self.downloader = PDFDownloader()

        self.domains = [
            "Finance",
            "Accounting",
            "Corporate_Governance",
            "Economics",
            "Management",
            "Public_Policy",
            "Sustainability_ESG",
            "Energy_Infrastructure",
            "Taxation",
            "Research_Methodology",
            "AI_Data_Science",
            "Interdisciplinary"
        ]

        self.output = Path(
            "Research_Output/Literature_Library/master_pdf_acquisition_report.json"
        )

    def run(self):
        report = []

        for domain in self.domains:
            print("=" * 70)
            print("Downloading domain:", domain)
            print("=" * 70)

            result = self.downloader.download_domain(domain)
            result["domain"] = domain
            report.append(result)

        self.output.write_text(
            json.dumps(report, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )

        return report


if __name__ == "__main__":
    result = BulkPDFDownloader().run()
    print(json.dumps(result, indent=2))
