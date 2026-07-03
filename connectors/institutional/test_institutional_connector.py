from connectors.institutional.institutional_connector import InstitutionalConnector


print("=" * 70)
print("AROS INSTITUTIONAL CONNECTOR TEST")
print("=" * 70)


sources = [
    "RBI",
    "SEBI",
    "ICAI",
    "IMF",
    "WorldBank",
    "ADB"
]


for source in sources:

    connector = InstitutionalConnector(source)

    results = connector.search(
        "corporate finance regulation"
    )

    for item in results:

        print()
        print("Institution:", item.source)
        print("Title:", item.title)
        print("URL:", item.pdf_link)


print()
print("✓ Institutional Connector Framework operational.")
