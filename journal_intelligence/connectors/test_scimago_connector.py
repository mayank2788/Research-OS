from journal_intelligence.connectors.scimago_connector import (
    ScimagoConnector
)


result = ScimagoConnector().normalize()


print("="*70)

print(
    "AROS SCIMAGO CONNECTOR TEST"
)

print("="*70)


print(result)


print()

print(
    "✓ SCImago Connector operational"
)

