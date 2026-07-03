import json
import re
from pathlib import Path

import requests


class PDFLibraryManager:
    """
    AROS PDF Library Manager.

    Purpose:
    - Save research PDFs
    - Maintain research library
    - Create metadata index

    Location:

    Research_Output/
        Research_Papers/
            Researched_Library/
                Project_Name/
                    01_Sources/


    Filename Standard:

    DOMAIN_YEAR_TITLE_IF_VALUE.pdf

    Example:

    Accounting_2024_Borrowing_Cost_IF_5_8.pdf
    """

    def __init__(self, base_folder="Research_Output"):

        self.base_folder = Path(base_folder)


    def clean_text(self, value, length=80):

        value = str(value or "NA")

        value = value.replace("&", "and")

        value = re.sub(
            r"[^A-Za-z0-9]+",
            "_",
            value
        )

        value = re.sub(
            r"_+",
            "_",
            value
        )

        return value.strip("_")[:length]


    def create_filename(
        self,
        domain,
        year,
        title,
        impact_factor="NA"
    ):

        domain = self.clean_text(domain, 40)

        year = self.clean_text(year, 10)

        title = self.clean_text(title, 90)

        impact_factor = self.clean_text(
            f"IF_{impact_factor}",
            20
        )


        return (
            f"{domain}_"
            f"{year}_"
            f"{title}_"
            f"{impact_factor}.pdf"
        )


    def source_folder(
        self,
        output_type,
        project_id
    ):

        folder = (
            self.base_folder
            / output_type
            / "Researched_Library"
            / project_id
            / "01_Sources"
        )

        folder.mkdir(
            parents=True,
            exist_ok=True
        )

        return folder


    def save_pdf(
        self,
        pdf_content,
        output_type,
        project_id,
        domain,
        year,
        title,
        impact_factor="NA",
        metadata=None
    ):

        folder = self.source_folder(
            output_type,
            project_id
        )


        filename = self.create_filename(
            domain,
            year,
            title,
            impact_factor
        )


        pdf_path = folder / filename

        pdf_path.write_bytes(
            pdf_content
        )


        index_file = folder / "paper_index.json"


        if index_file.exists():

            index = json.loads(
                index_file.read_text(
                    encoding="utf-8"
                )
            )

        else:

            index = []


        index.append(
            {
                "file": filename,
                "domain": domain,
                "year": year,
                "title": title,
                "impact_factor": impact_factor,
                "metadata": metadata or {}
            }
        )


        index_file.write_text(
            json.dumps(
                index,
                indent=2,
                ensure_ascii=False
            ),
            encoding="utf-8"
        )


        return pdf_path


    def download_pdf(
        self,
        url,
        **details
    ):

        response = requests.get(
            url,
            timeout=40,
            headers={
                "User-Agent":
                "AROS Research Operating System"
            }
        )

        response.raise_for_status()


        return self.save_pdf(
            response.content,
            **details
        )
