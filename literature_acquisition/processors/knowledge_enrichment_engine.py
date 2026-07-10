import json
from pathlib import Path


class KnowledgeEnrichmentEngine:

    def __init__(self):

        self.folder = Path(
            "knowledge/objects/literature"
        )

        self.methods = [
            "regression",
            "panel data",
            "case study",
            "survey",
            "machine learning",
            "bibliometric",
            "systematic review"
        ]

        self.models = [
            "OLS",
            "VAR",
            "ARIMA",
            "DEA",
            "SEM",
            "ANOVA",
            "GMM",
            "TOPSIS",
            "AHP"
        ]

        self.variables = [
            "profitability",
            "liquidity",
            "leverage",
            "risk",
            "performance",
            "debt",
            "capital structure",
            "governance",
            "sustainability"
        ]


    def enrich(self, file):

        data = json.loads(
            file.read_text(
                encoding="utf-8"
            )
        )

        text = json.dumps(
            data
        ).lower()


        intelligence = data.get(
            "research_intelligence",
            {}
        )


        intelligence["detected_methods"] = [

            x for x in self.methods

            if x in text

        ]


        intelligence["detected_models"] = [

            x for x in self.models

            if x.lower() in text

        ]


        intelligence["detected_variables"] = [

            x for x in self.variables

            if x in text

        ]


        data["research_intelligence"] = intelligence


        file.write_text(

            json.dumps(
                data,
                indent=2
            ),

            encoding="utf-8"

        )


    def run(self):

        count = 0


        for file in self.folder.glob(
            "*.json"
        ):

            self.enrich(file)

            count += 1


        return {
            "objects_enriched": count
        }



if __name__ == "__main__":

    engine = KnowledgeEnrichmentEngine()

    print(
        engine.run()
    )

