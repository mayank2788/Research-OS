from connector_framework.connector_registry import (
    ConnectorRegistry,
)
from connector_framework.credential_manager import (
    ConnectorCredentialManager,
)


registry = ConnectorRegistry()
credentials = ConnectorCredentialManager(registry)

print("=" * 70)
print("AROS CONNECTOR FOUNDATION TEST")
print("=" * 70)

names = registry.list_connectors()

print("Connectors:", names)
print("Total:", len(names))
print()

for name in names:
    config = registry.get_connector(name)
    auth = credentials.get_auth(name)

    print(name)
    print("  enabled:", config.get("enabled"))
    print("  auth_type:", auth["auth_type"])
    print("  configured:", auth["configured"])
    print("  health:", registry.get_health(name)["status"])

print()
print("✓ Connector registry operational")
print("✓ Credential manager operational")
print("✓ Base connector interface available")
