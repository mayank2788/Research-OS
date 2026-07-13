import os
from typing import Any, Dict

from dotenv import load_dotenv


class ConnectorCredentialManager:
    """
    Loads connector credentials from environment variables.

    It never writes secrets to configuration files or logs.
    """

    def __init__(
        self,
        registry: Any,
        env_file: str = ".env",
    ) -> None:
        load_dotenv(env_file)
        self.registry = registry

    @staticmethod
    def _environment_value(
        variable_name: str,
    ) -> str:
        if not variable_name:
            return ""

        return os.getenv(
            variable_name,
            "",
        ).strip()

    def get_auth(
        self,
        connector_name: str,
    ) -> Dict[str, Any]:
        config = self.registry.get_connector(
            connector_name
        )

        auth_type = config.get(
            "auth_type",
            "none",
        )

        result: Dict[str, Any] = {
            "auth_type": auth_type,
            "headers": {},
            "params": {},
            "token_expires_at": None,
            "configured": True,
        }

        if auth_type == "none":
            return result

        if auth_type == "query_param":
            value = self._environment_value(
                config.get(
                    "credential_env",
                    "",
                )
            )

            if not value:
                result["configured"] = False
                return result

            parameter = config.get(
                "credential_parameter",
                "api_key",
            )

            result["params"][parameter] = value
            return result

        if auth_type == "header":
            value = self._environment_value(
                config.get(
                    "credential_env",
                    "",
                )
            )

            if not value:
                result["configured"] = False
                return result

            header = config.get(
                "credential_header",
                "Authorization",
            )

            result["headers"][header] = value
            return result

        if auth_type == "bearer":
            value = self._environment_value(
                config.get(
                    "credential_env",
                    "",
                )
            )

            if not value:
                result["configured"] = False
                return result

            result["headers"]["Authorization"] = (
                f"Bearer {value}"
            )

            return result

        if auth_type == "contact_identity":
            email = self._environment_value(
                config.get(
                    "contact_email_env",
                    "",
                )
            )

            if not email:
                result["configured"] = False
                return result

            result["headers"]["User-Agent"] = (
                f"AROS/1.0 (mailto:{email})"
            )

            result["params"]["mailto"] = email

            return result

        if auth_type == "oauth_client_credentials":
            client_id = self._environment_value(
                config.get(
                    "client_id_env",
                    "",
                )
            )

            client_secret = self._environment_value(
                config.get(
                    "client_secret_env",
                    "",
                )
            )

            token_url = self._environment_value(
                config.get(
                    "token_url_env",
                    "",
                )
            )

            result["oauth"] = {
                "client_id": client_id,
                "client_secret": client_secret,
                "token_url": token_url,
            }

            result["configured"] = bool(
                client_id
                and client_secret
                and token_url
            )

            return result

        raise ValueError(
            f"Unsupported authentication type: {auth_type}"
        )
