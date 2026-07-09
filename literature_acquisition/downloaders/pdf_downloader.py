import json
import urllib.request
import re
from pathlib import Path

from literature_acquisition.connectors.openalex_oa_resolver import (
    OpenAlexOAResolver
)


class PDFDownloader:

    """
    AROS PDF Acquisition Engine v1.2

    Features:
    - OA PDF download
    - duplicate prevention
    - download reporting
    - failure classification
    """


    def __init__(self):

        self.library = Path(
            "Research_Output/Literature_Library"
        )

        self.oa_resolver = OpenAlexOAResolver()


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

        domain_path = self.library / domain

        metadata_file = (
            domain_path /
            "metadata.json"
        )

        pdf_folder = (
            domain_path /
            "PDFs"
        )

        pdf_folder.mkdir(
            exist_ok=True
        )


        papers = json.loads(
            metadata_file.read_text(
                encoding="utf-8"
            )
        )


        report = []

        stats = {

            "downloaded": 0,
            "already_exists": 0,
            "no_pdf_url": 0,
            "invalid_pdf": 0,
            "failed": 0

        }


        for index, paper in enumerate(
            papers,
            start=1
        ):

            print(
                "Processing",
                index,
                "/",
                len(papers)
            )


            title = paper.get(
                "title",
                "paper"
            )


            pdf_url = self.extract_pdf_url(
                paper
            )


            if not pdf_url:

                pdf_url = self.oa_resolver.resolve(
                    paper
                )


            if not pdf_url:

                status = "No PDF URL"

                stats[
                    "no_pdf_url"
                ] += 1


            else:

                filename = (

                    str(index).zfill(4)
                    + "_"
                    + self.safe_filename(
                        title
                    )
                    + ".pdf"
                )


                output = (
                    pdf_folder /
                    filename
                )


                if output.exists():

                    status = "Already Exists"

                    stats[
                        "already_exists"
                    ] += 1


                else:

                    try:

                        request = urllib.request.Request(
                            pdf_url,
                            headers={
                                "User-Agent":
                                "AROS Research Collector"
                            }
                        )


                        with urllib.request.urlopen(
                            request,
                            timeout=20
                        ) as response:

                            content = response.read()


                        if not content.startswith(
                            b"%PDF"
                        ):

                            resolved_url = self.oa_resolver.resolve(paper)

                            if resolved_url and resolved_url != pdf_url:
                                try:
                                    request = urllib.request.Request(
                                        resolved_url,
                                        headers={"User-Agent": "AROS Research Collector"}
                                    )

                                    with urllib.request.urlopen(request, timeout=20) as response:
                                        content = response.read()

                                    if content.startswith(b"%PDF"):
                                        output.write_bytes(content)
                                        paper["local_pdf_path"] = str(output)
                                        paper["resolved_pdf_url"] = resolved_url
                                        status = "Downloaded via OpenAlex"
                                        stats["downloaded"] += 1
                                    else:
                                        status = "Invalid PDF"
                                        stats["invalid_pdf"] += 1
                                except Exception:
                                    status = "Invalid PDF"
                                    stats["invalid_pdf"] += 1
                            else:
                                status = "Invalid PDF"
                                stats["invalid_pdf"] += 1


                        else:

                            output.write_bytes(
                                content
                            )

                            paper[
                                "local_pdf_path"
                            ] = str(output)


                            status = "Downloaded"

                            stats[
                                "downloaded"
                            ] += 1


                    except Exception:

                        resolved_url = self.oa_resolver.resolve(paper)

                        if resolved_url and resolved_url != pdf_url:
                            try:
                                request = urllib.request.Request(
                                    resolved_url,
                                    headers={"User-Agent": "AROS Research Collector"}
                                )

                                with urllib.request.urlopen(request, timeout=20) as response:
                                    content = response.read()

                                if content.startswith(b"%PDF"):
                                    output.write_bytes(content)
                                    paper["local_pdf_path"] = str(output)
                                    paper["resolved_pdf_url"] = resolved_url
                                    status = "Downloaded via OpenAlex"
                                    stats["downloaded"] += 1
                                else:
                                    status = "Failed"
                                    stats["failed"] += 1
                            except Exception:
                                status = "Failed"
                                stats["failed"] += 1
                        else:
                            status = "Failed"
                            stats["failed"] += 1



            report.append(
                {
                    "title": title,
                    "status": status,
                    "pdf_url": pdf_url
                }
            )



        metadata_file.write_text(

            json.dumps(
                papers,
                indent=2,
                ensure_ascii=False
            ),

            encoding="utf-8"

        )


        report_file = (
            domain_path /
            "download_report.json"
        )


        report_file.write_text(

            json.dumps(
                {
                    "domain": domain,
                    "statistics": stats,
                    "papers": report
                },
                indent=2,
                ensure_ascii=False
            ),

            encoding="utf-8"

        )


        return stats



if __name__ == "__main__":


    result = PDFDownloader().download_domain(
        "Finance"
    )


    print(result)

