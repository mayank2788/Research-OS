from journal_intelligence.journal_database_manager import (
    JournalDatabaseManager
)


manager = JournalDatabaseManager()


batch = [

{
"journal_name":"Test Finance Journal",
"publisher":"Test Publisher",
"institution":"",
"country":"Test",
"domains":["Finance"],
"ranking_tags":["Test"],
"access_type":"open",
"url":""
}

]


result = manager.add_journals(
    batch
)


print("="*70)

print(
    "AROS JOURNAL DATABASE MANAGER TEST"
)

print("="*70)


print(result)


print()

print(
    "✓ Journal Database Manager operational"
)

