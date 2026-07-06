import json
import time
from pathlib import Path

from literature_acquisition.connectors.doaj_article_connector import (
    DOAJArticleConnector
)


class AROSLiteratureCollector:
    """
    AROS Literature Collector v1.

    Collects open-access paper metadata
    domain-wise from DOAJ.
    """


    def __init__(self):

        self.connector = DOAJArticleConnector()

        self.output = Path(
            "Research_Output/Literature_Library"
        )

        self.domains = {

            "Finance": [
                "corporate finance",
                "capital structure",
                "debt management",
                "financial markets"
            ],

            "Accounting": [
                "financial reporting",
                "earnings management",
                "accounting standards",
                "audit quality"
            ],

            "Corporate_Governance": [
                "corporate governance",
                "board governance",
                "ownership structure"
            ],

            "Economics": [
                "applied economics",
                "development economics",
                "energy economics"
            ],

            "Management": [
                "strategic management",
                "innovation management",
                "organizational performance"
            ],

            "Public_Policy": [
                "public policy",
                "regulation",
                "public administration"
            ],

            "Sustainability_ESG": [
                "ESG",
                "sustainability",
                "climate finance",
                "CSR"
            ],

            "Energy_Infrastructure": [
                "energy infrastructure",
                "renewable energy",
                "power sector",
                "infrastructure finance"
            ],

            "Taxation": [
                "taxation",
                "corporate tax",
                "tax policy"
            ],

            "Research_Methodology": [
                "research methodology",
                "bibliometric analysis",
                "systematic literature review",
                "econometrics"
            ],

            "AI_Data_Science": [
                "artificial intelligence",
                "machine learning",
                "data science",
                "analytics"
            ],

            "Interdisciplinary": [
                "interdisciplinary research",
                "multidisciplinary research",
                "business technology"
            ]
        }


    def deduplicate(self, papers):

        unique = {}

        for paper in papers:

            key = (
                paper.get("doi")
                or paper.get("title")
                or ""
            ).lower().strip()

            if key:

                unique[key] = paper


        return list(
            unique.values()
        )


    def collect_domain(
        self,
        domain,
        target=100
    ):

        queries = self.domains[domain]

        papers = []


        for query in queries:

            if len(papers) >= target:
                break


            try:

                results = self.connector.search(
                    query=query,
                    limit=100
                )

                for paper in results:

                    paper["domain"] = domain
                    paper["query"] = query

                papers.extend(
                    results
                )


                time.sleep(1)


            except Exception as error:

                print(
                    "Query failed:",
                    domain,
                    query,
                    error
                )


        papers = self.deduplicate(
            papers
        )[:target]


        folder = (
            self.output
            /
            domain
        )

        folder.mkdir(
            parents=True,
            exist_ok=True
        )


        output_file = (
            folder
            /
            "metadata.json"
        )


        output_file.write_text(

            json.dumps(
                papers,
                indent=2,
                ensure_ascii=False
            ),

            encoding="utf-8"
        )


        return {

            "domain":
                domain,

            "papers_saved":
                len(papers),

            "output":
                str(output_file)

        }



    def collect_all(
        self,
        target_per_domain=100
    ):

        report = []


        for domain in self.domains:

            print(
                "Collecting:",
                domain
            )


            result = self.collect_domain(
                domain,
                target=target_per_domain
            )


            report.append(
                result
            )


        report_file = (
            self.output
            /
            "literature_collection_report.json"
        )


        report_file.write_text(

            json.dumps(
                report,
                indent=2,
                ensure_ascii=False
            ),

            encoding="utf-8"
        )


        return report



if __name__ == "__main__":

    collector = AROSLiteratureCollector()

    result = collector.collect_all(
        target_per_domain=100
    )

    print(
        json.dumps(
            result,
            indent=2
        )
    )

