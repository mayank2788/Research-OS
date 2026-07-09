import json
import hashlib
from pathlib import Path


class KnowledgeObjectBridge:

    """
    AROS Knowledge Object Bridge v1.

    Converts harvested literature metadata
    into AROS Knowledge Objects.
    """


    def __init__(self):

        self.library = Path(
            "Research_Output/Literature_Library"
        )

        self.output = Path(
            "knowledge/objects/literature"
        )

        self.output.mkdir(
            parents=True,
            exist_ok=True
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



    def make_id(self, text):

        return hashlib.md5(
            text.encode()
        ).hexdigest()



    def convert_paper(
        self,
        paper,
        domain
    ):

        title = paper.get(
            "title",
            ""
        )


        return {

            "object_type":
                "research_paper",

            "knowledge_id":
                self.make_id(
                    title
                ),


            "metadata": {

                "title":
                    title,

                "domain":
                    domain,

                "authors":
                    paper.get(
                        "authors",
                        []
                    ),

                "journal":
                    paper.get(
                        "journal",
                        ""
                    ),

                "year":
                    paper.get(
                        "year",
                        ""
                    ),

                "doi":
                    paper.get(
                        "doi",
                        ""
                    )

            },


            "research_intelligence": {

                "abstract":
                    paper.get(
                        "abstract",
                        ""
                    ),

                "methodology":
                    None,

                "variables":
                    [],

                "models":
                    [],

                "findings":
                    [],

                "limitations":
                    [],

                "future_scope":
                    []

            },


            "source": {

                "origin":
                    paper.get(
                        "source",
                        ""
                    ),

                "pdf_available":
                    bool(
                        paper.get(
                            "local_pdf_path"
                        )
                    ),

                "pdf_path":
                    paper.get(
                        "local_pdf_path",
                        ""
                    )

            }

        }



    def process_domain(
        self,
        domain
    ):

        metadata = (

            self.library /
            domain /
            "metadata.json"

        )


        if not metadata.exists():

            return 0


        papers = json.loads(

            metadata.read_text(
                encoding="utf-8"
            )

        )


        count = 0


        for paper in papers:

            obj = self.convert_paper(
                paper,
                domain
            )


            file = (

                self.output /

                (
                    obj["knowledge_id"]
                    +
                    ".json"
                )

            )


            file.write_text(

                json.dumps(
                    obj,
                    indent=2,
                    ensure_ascii=False
                ),

                encoding="utf-8"

            )


            count += 1


        return count



    def run(self):

        total = 0

        report = {}


        for domain in self.domains:

            count = self.process_domain(
                domain
            )

            report[domain] = count

            total += count


        report["TOTAL"] = total


        return report




if __name__ == "__main__":

    bridge = KnowledgeObjectBridge()

    print(

        json.dumps(
            bridge.run(),
            indent=2
        )

    )

