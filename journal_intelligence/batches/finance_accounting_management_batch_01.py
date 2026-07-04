
from journal_intelligence.journal_database_manager import (
    JournalDatabaseManager
)


journals = [

# ==================================================
# FINANCE JOURNALS
# ==================================================

{
"journal_name":"Review of Finance",
"publisher":"Oxford University Press",
"institution":"European Finance Association",
"country":"UK",
"domains":["Finance","Corporate Finance","Financial Markets"],
"ranking_tags":["ABDC","ABS/AJG","Scopus","Q1"],
"access_type":"limited",
"url":""
},

{
"journal_name":"Financial Management",
"publisher":"Wiley",
"institution":"Financial Management Association",
"country":"USA",
"domains":["Finance","Corporate Finance"],
"ranking_tags":["ABDC","Scopus"],
"access_type":"limited",
"url":""
},

{
"journal_name":"Journal of Empirical Finance",
"publisher":"Elsevier",
"institution":"",
"country":"Netherlands",
"domains":["Finance","Empirical Finance"],
"ranking_tags":["Scopus","Q1"],
"access_type":"limited",
"url":""
},

{
"journal_name":"International Review of Financial Analysis",
"publisher":"Elsevier",
"institution":"",
"country":"Netherlands",
"domains":["Finance","Financial Analysis"],
"ranking_tags":["Scopus","Q1"],
"access_type":"limited",
"url":""
},

{
"journal_name":"Finance Research Letters",
"publisher":"Elsevier",
"institution":"",
"country":"Netherlands",
"domains":["Finance"],
"ranking_tags":["Scopus","Q1"],
"access_type":"hybrid",
"url":""
},


# ==================================================
# ACCOUNTING JOURNALS
# ==================================================

{
"journal_name":"Accounting Organizations and Society",
"publisher":"Elsevier",
"institution":"",
"country":"UK",
"domains":["Accounting and Reporting"],
"ranking_tags":["FT50","ABDC A*","Scopus","Q1"],
"access_type":"limited",
"url":""
},

{
"journal_name":"Contemporary Accounting Research",
"publisher":"Wiley",
"institution":"",
"country":"Canada",
"domains":["Accounting and Reporting"],
"ranking_tags":["FT50","ABDC A*","Scopus"],
"access_type":"limited",
"url":""
},

{
"journal_name":"Accounting Horizons",
"publisher":"American Accounting Association",
"institution":"",
"country":"USA",
"domains":["Accounting","Audit"],
"ranking_tags":["Scopus"],
"access_type":"limited",
"url":""
},

{
"journal_name":"European Accounting Review",
"publisher":"Taylor and Francis",
"institution":"",
"country":"UK",
"domains":["Accounting"],
"ranking_tags":["Scopus","Q1"],
"access_type":"limited",
"url":""
},


# ==================================================
# MANAGEMENT JOURNALS
# ==================================================

{
"journal_name":"Academy of Management Review",
"publisher":"Academy of Management",
"institution":"",
"country":"USA",
"domains":["Management","Strategy"],
"ranking_tags":["FT50","ABDC A*","ABS 4*"],
"access_type":"limited",
"url":""
},

{
"journal_name":"Journal of Management",
"publisher":"Sage",
"institution":"",
"country":"USA",
"domains":["Management"],
"ranking_tags":["Scopus","Q1"],
"access_type":"limited",
"url":""
},

{
"journal_name":"Organization Science",
"publisher":"INFORMS",
"institution":"",
"country":"USA",
"domains":["Management","Organisation"],
"ranking_tags":["FT50","Scopus"],
"access_type":"limited",
"url":""
},

{
"journal_name":"Long Range Planning",
"publisher":"Elsevier",
"institution":"",
"country":"UK",
"domains":["Strategy","Management"],
"ranking_tags":["Scopus"],
"access_type":"limited",
"url":""
},


# ==================================================
# OPEN ACCESS ADDITIONS
# ==================================================

{
"journal_name":"Journal of Open Innovation Technology Market and Complexity",
"publisher":"Elsevier",
"institution":"",
"country":"Netherlands",
"domains":["Innovation","Management"],
"ranking_tags":["Scopus","Open Access"],
"access_type":"open",
"url":""
},

{
"journal_name":"Economies",
"publisher":"MDPI",
"institution":"",
"country":"Switzerland",
"domains":["Economics","Finance"],
"ranking_tags":["Scopus","Open Access"],
"access_type":"open",
"url":""
}

]


manager = JournalDatabaseManager()

result = manager.add_journals(
    journals
)


print("="*70)
print("AROS JOURNAL EXPANSION BATCH 01")
print("="*70)

print(result)

print()
print("✓ Batch import completed")

