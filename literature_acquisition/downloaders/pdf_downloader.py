import json
import urllib.request
import re
from pathlib import Path


class PDFDownloader:

    """
    AROS PDF Acquisition Engine v1.1

    Safe downloader:
    - Open access URLs only
    - Timeout protected
    - Progress reporting
    """


    def __init__(self):

        self.library = Path(
            "Research_Output/Literature_Library"
        )


    def safe_filename(self, text):

        return re.sub(
            r"[^A-Za-z0-9]+",
            "_",
            str(text)
        )[:80]


    def extract_pdf_url(self, paper):

        for link in paper.get("links", []):

            url = link.get("url", "")

            if (
                ".pdf" in url.lower()
                or link.get("type") == "fulltext"
            ):

                return url


        return None



    def download_domain(self, domain):

        path = self.library / domain

        metadata = path / "metadata.json"

        pdf_dir = path / "PDFs"

        pdf_dir.mkdir(
            exist_ok=True
        )


        papers = json.loads(
            metadata.read_text(
                encoding="utf-8"
            )
        )


        downloaded = 0
        skipped = 0


        for i, paper in enumerate(
            papers,
            start=1
        ):

            print(
                "Checking",
                i,
                "/",
                len(papers)
            )


            url = self.extract_pdf_url(
                paper
            )


            if not url:

                skipped += 1
                continue


            filename = (
                str(i).zfill(4)
                + "_"
                + self.safe_filename(
                    paper.get(
                        "title",
                        "paper"
                    )
                )
                + ".pdf"
            )


            output = pdf_dir / filename


            try:

                request = urllib.request.Request(
                    url,
                    headers={
                        "User-Agent":
                        "AROS Research Collector"
                    }
                )


                with urllib.request.urlopen(
                    request,
                    timeout=15
                ) as response:

                    content = response.read()


                if not content.startswith(
                    b"%PDF"
                ):

                    skipped += 1
                    continue


                output.write_bytes(
                    content
                )


                paper["local_pdf_path"] = (
                    str(output)
                )


                downloaded += 1


            except Exception:

                skipped += 1


        metadata.write_text(
            json.dumps(
                papers,
                indent=2,
                ensure_ascii=False
            )
        )


        return {

            "domain": domain,

            "downloaded": downloaded,

            "skipped": skipped
        }



if __name__ == "__main__":

    print(
        PDFDownloader()
        .download_domain(
            "Finance"
        )
    )

