from connectors.accounting import AccountingStandardsConnector


connector = AccountingStandardsConnector()

results = connector.search(
    "IAS 23 borrowing costs IFRS"
)

print("=" * 70)
print("AROS ACCOUNTING CONNECTOR TEST")
print("=" * 70)

print("Results:", len(results))

for r in results:
    print()
    print("Title:", r.title)
    print("Source:", r.source)
    print("Type:", r.document_type)
    print("URL:", r.pdf_link)

print()
print("✓ Accounting Connector operational")
