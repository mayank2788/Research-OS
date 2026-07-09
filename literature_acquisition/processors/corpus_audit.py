import json
from pathlib import Path


class CorpusAudit:

    """
    AROS Corpus Audit Engine.

    Validates research corpus quality
    before AI Knowledge Object ingestion.
    """


    def __init__(self):

        self.library = Path(
            "Research_Output/Literature_Library"
        )


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


    def audit_domain(
        self,
        domain
    ):

        folder = (
            self.library /
            domain
        )


        metadata = (
            folder /
            "metadata.json"
        )


        pdf_folder = (
            folder /
            "PDFs"
        )


        papers = []


        if metadata.exists():

            papers = json.loads(

                metadata.read_text(
                    encoding="utf-8"
                )
            )


        pdf_count = 0


        if pdf_folder.exists():

            pdf_count = len(

                list(
                    pdf_folder.glob(
                        "*.pdf"
                    )
                )
            )


        doi_count = sum(

            1

            for p in papers

            if p.get(
                "doi"
            )

        )


        metadata_count = len(
            papers
        )


        coverage = 0


        if metadata_count:

            coverage = round(

                (
                    pdf_count
                    /
                    metadata_count
                )
                *
                100,

                2

            )


        ready = (

            "YES"

            if coverage >= 50

            else "PARTIAL"

        )


        return {

            "domain":
                domain,

            "metadata_records":
                metadata_count,

            "doi_records":
                doi_count,

            "pdf_files":
                pdf_count,

            "pdf_coverage_percent":
                coverage,

            "ai_ingestion_ready":
                ready

        }



    def run(self):

        report = []


        for domain in self.domains:

            report.append(

                self.audit_domain(
                    domain
                )

            )


        output = (

            self.library /
            "corpus_audit_report.json"

        )


        output.write_text(

            json.dumps(

                report,
                indent=2

            ),

            encoding="utf-8"

        )


        return report



if __name__ == "__main__":

    audit = CorpusAudit()

    result = audit.run()


    print(

        json.dumps(
            result,
            indent=2
        )

    )

