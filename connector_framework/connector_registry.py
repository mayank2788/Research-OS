import json
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List


class ConnectorRegistry:
    """
    Loads connector configuration and stores last-known health state.

    Phase A uses JSON files rather than a database.
    """

    def __init__(
        self,
        registry_path: str = "config/connector_registry.json",
        runtime_path: str = "config/connector_runtime_status.json",
    ) -> None:
        self.registry_path = Path(registry_path)
        self.runtime_path = Path(runtime_path)

        if not self.registry_path.exists():
            raise FileNotFoundError(
                f"Connector registry not found: {self.registry_path}"
            )

        self.data = json.loads(
            self.registry_path.read_text(encoding="utf-8")
        )

        if "connectors" not in self.data:
            raise ValueError(
                "Connector registry must contain a 'connectors' object."
            )

        self.runtime = self._load_runtime()

    def _load_runtime(self) -> Dict[str, Any]:
        if not self.runtime_path.exists():
            return {"connectors": {}}

        try:
            return json.loads(
                self.runtime_path.read_text(encoding="utf-8")
            )
        except (json.JSONDecodeError, OSError):
            return {"connectors": {}}

    def _save_runtime(self) -> None:
        self.runtime_path.parent.mkdir(parents=True, exist_ok=True)

        self.runtime_path.write_text(
            json.dumps(self.runtime, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def list_connectors(
        self,
        enabled_only: bool = False,
    ) -> List[str]:
        names = []

        for name, config in self.data["connectors"].items():
            if enabled_only and not config.get("enabled", False):
                continue

            names.append(name)

        return sorted(names)

    def get_connector(self, name: str) -> Dict[str, Any]:
        try:
            return deepcopy(self.data["connectors"][name])
        except KeyError as error:
            raise KeyError(
                f"Unknown connector: {name}"
            ) from error

    def get_policy(
        self,
        name: str,
        operation: str,
    ) -> Dict[str, Any]:
        connector = self.get_connector(name)
        policies = connector.get("policies", {})

        if operation not in policies:
            raise KeyError(
                f"No policy for connector '{name}' "
                f"and operation '{operation}'."
            )

        return deepcopy(policies[operation])

    def update_health(
        self,
        name: str,
        status: str,
        **details: Any,
    ) -> Dict[str, Any]:
        if name not in self.data["connectors"]:
            raise KeyError(f"Unknown connector: {name}")

        allowed = {
            "unknown",
            "healthy",
            "degraded",
            "down",
            "unauthenticated",
        }

        if status not in allowed:
            raise ValueError(
                f"Invalid health status: {status}"
            )

        record = {
            "status": status,
            "last_checked": datetime.now(
                timezone.utc
            ).isoformat(timespec="seconds"),
            **details,
        }

        self.runtime.setdefault(
            "connectors",
            {}
        )[name] = record

        self._save_runtime()

        return deepcopy(record)

    def get_health(self, name: str) -> Dict[str, Any]:
        connector = self.get_connector(name)

        return deepcopy(
            self.runtime.get(
                "connectors",
                {}
            ).get(
                name,
                connector.get(
                    "health",
                    {
                        "status": "unknown",
                        "last_checked": None,
                    },
                ),
            )
        )
