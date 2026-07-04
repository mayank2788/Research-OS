from knowledge.knowledge_object import KnowledgeObject


class AccountingStandardsConnector:
    """
    AROS Accounting Standards Connector.

    Purpose:
    Domain specific acquisition for:

    - IFRS
    - IAS
    - Ind AS
    - Accounting standards research
    - Professional accounting evidence

    v1:
    Curated authoritative sources.

    Future:
    API / crawler integration.
    """

    def __init__(self):

        self.name = "Accounting Standards"


        self.sources = [

            {
                "title":
                "IAS 23 Borrowing Costs IFRS Foundation",

                "url":
                "https://www.ifrs.org",

                "domain":
                "IFRS Accounting Standards"
            },


            {
                "title":
                "Ind AS 23 Borrowing Costs ICAI",

                "url":
                "https://www.icai.org",

                "domain":
                "Indian Accounting Standards"
            },


            {
                "title":
                "Companies Indian Accounting Standards Rules MCA",

                "url":
                "https://www.mca.gov.in",

                "domain":
                "Accounting Regulation"
            },

        ]


    def search(
        self,
        query,
        max_results=10
    ):

        results = []


        query_text = query.lower()


        for item in self.sources:


            if (
                "ias" in query_text
                or "ind as" in query_text
                or "accounting" in query_text
                or "ifrs" in query_text
            ):


                results.append(

                    KnowledgeObject(

                        title=item["title"],

                        source=self.name,

                        source_type=
                        "Professional Accounting Source",

                        document_type=
                        "Accounting Standard / Guidance",

                        research_domain=
                        item["domain"],

                        pdf_link=
                        item["url"],

                        open_access=True,

                        confidence=0.90,

                        keywords=[
                            "IAS",
                            "IFRS",
                            "Ind AS",
                            "Accounting Standards"
                        ]

                    )

                )


        return results[:max_results]
