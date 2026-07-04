import json
from pathlib import Path


class JournalDatabaseManager:
    """
    AROS Journal Database Manager.

    Responsible for:
    - Adding journals
    - Avoiding duplicates
    - Maintaining schema consistency
    - Scaling database to 500+ journals
    """


    def __init__(self):

        self.path = Path(
            "journal_intelligence/journal_master_database.json"
        )

        self.data = json.loads(
            self.path.read_text(
                encoding="utf-8"
            )
        )


    def existing_names(self):

        return {
            j["journal_name"].lower()
            for j in self.data["journals"]
        }


    def add_journals(
        self,
        journals
    ):

        existing = self.existing_names()

        added = 0
        skipped = 0


        for journal in journals:

            name = (
                journal["journal_name"]
                .lower()
            )


            if name in existing:

                skipped += 1
                continue


            template = {

                "journal_name":
                    journal.get(
                        "journal_name",
                        ""
                    ),

                "publisher":
                    journal.get(
                        "publisher",
                        ""
                    ),

                "institution":
                    journal.get(
                        "institution",
                        ""
                    ),

                "country":
                    journal.get(
                        "country",
                        ""
                    ),

                "domains":
                    journal.get(
                        "domains",
                        []
                    ),

                "ranking_tags":
                    journal.get(
                        "ranking_tags",
                        []
                    ),

                "access_type":
                    journal.get(
                        "access_type",
                        "unknown"
                    ),

                "url":
                    journal.get(
                        "url",
                        ""
                    )
            }


            self.data["journals"].append(
                template
            )

            existing.add(name)

            added += 1


        self.save()


        return {
            "added": added,
            "skipped_duplicates": skipped,
            "total": len(
                self.data["journals"]
            )
        }



    def save(self):

        self.path.write_text(

            json.dumps(
                self.data,
                indent=2,
                ensure_ascii=False
            ),

            encoding="utf-8"
        )
