import logging
import random
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests
from requests import Response
from tenacity import (
    RetryCallState,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from connector_framework.rate_limiter import (
    ConnectorRateLimiter,
)


LOGGER = logging.getLogger("aros.connector_execution")


class RetryableConnectorError(Exception):
    """
    Raised only for request failures that AROS may retry.
    """


class ConnectorAuthenticationError(Exception):
    """
    Raised when connector credentials are missing or rejected.
    """


class ConnectorRequestError(Exception):
    """
    Raised for permanent request failures.
    """


@dataclass
class ExecutionResult:
    connector: str
    operation: str
    method: str
    url: str
    status_code: int
    elapsed_seconds: float
    attempts: int
    rate_limit_remaining: Optional[str]
    rate_limit_reset: Optional[str]
    response: Response


class ConnectorExecutionManager:
    """
    Central HTTP execution layer for all AROS connectors.

    Responsibilities:
    - credential injection
    - session reuse
    - connector/operation rate limiting
    - timeout enforcement
    - retry and exponential backoff
    - Retry-After handling
    - request metrics
    """

    RETRYABLE_STATUS_CODES = {
        429,
        500,
        502,
        503,
        504,
    }

    AUTH_FAILURE_CODES = {
        401,
        403,
    }

    def __init__(
        self,
        registry,
        credential_manager,
        max_attempts: int = 4,
    ) -> None:
        self.registry = registry
        self.credentials = credential_manager
        self.max_attempts = max_attempts

        self.session = requests.Session()
        self.rate_limiter = ConnectorRateLimiter(
            registry
        )

        self._attempt_counter = 0

    @staticmethod
    def _retry_after_seconds(
        response: Response,
    ) -> Optional[float]:
        value = response.headers.get(
            "Retry-After"
        )

        if not value:
            return None

        try:
            return max(
                float(value),
                0.0,
            )
        except ValueError:
            return None

    @staticmethod
    def _rate_limit_header(
        response: Response,
        names,
    ) -> Optional[str]:
        for name in names:
            value = response.headers.get(name)

            if value is not None:
                return value

        return None

    def _wait_before_retry(
        self,
        retry_state: RetryCallState,
    ) -> float:
        exception = retry_state.outcome.exception()

        if isinstance(
            exception,
            RetryableConnectorError,
        ):
            retry_after = getattr(
                exception,
                "retry_after",
                None,
            )

            if retry_after is not None:
                return retry_after

        exponential = wait_exponential(
            multiplier=1,
            min=1,
            max=30,
        )(retry_state)

        jitter = random.uniform(
            0,
            0.5,
        )

        return exponential + jitter

    def _build_request_auth(
        self,
        connector_name: str,
    ) -> Dict[str, Any]:
        auth = self.credentials.get_auth(
            connector_name
        )

        config = self.registry.get_connector(
            connector_name
        )

        auth_type = config.get(
            "auth_type",
            "none",
        )

        if (
            auth_type != "none"
            and not auth.get(
                "configured",
                False,
            )
        ):
            raise ConnectorAuthenticationError(
                f"Credentials not configured for "
                f"connector '{connector_name}'."
            )

        if auth_type == "oauth_client_credentials":
            raise ConnectorAuthenticationError(
                "OpenAIRE OAuth token exchange is not "
                "implemented in Phase A2."
            )

        return auth

    def _execute_once(
        self,
        connector_name: str,
        operation: str,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]],
        headers: Optional[Dict[str, str]],
        json_body: Optional[Dict[str, Any]],
        data: Any,
        timeout: float,
    ) -> ExecutionResult:
        self._attempt_counter += 1

        connector = self.registry.get_connector(
            connector_name
        )

        base_url = connector[
            "base_url"
        ].rstrip("/")

        if endpoint.startswith("http"):
            url = endpoint
        else:
            url = (
                base_url
                + "/"
                + endpoint.lstrip("/")
            )

        auth = self._build_request_auth(
            connector_name
        )

        final_headers = {
            **auth.get(
                "headers",
                {},
            ),
            **(
                headers
                or {}
            ),
        }

        final_params = {
            **auth.get(
                "params",
                {},
            ),
            **(
                params
                or {}
            ),
        }

        self.rate_limiter.acquire(
            connector_name,
            operation,
        )

        started = time.monotonic()

        try:
            response = self.session.request(
                method=method.upper(),
                url=url,
                params=final_params,
                headers=final_headers,
                json=json_body,
                data=data,
                timeout=timeout,
            )

        except (
            requests.Timeout,
            requests.ConnectionError,
        ) as error:
            raise RetryableConnectorError(
                f"{connector_name} request failed: "
                f"{error}"
            ) from error

        elapsed = time.monotonic() - started

        if response.status_code in (
            self.RETRYABLE_STATUS_CODES
        ):
            error = RetryableConnectorError(
                f"{connector_name} returned "
                f"HTTP {response.status_code}"
            )

            error.retry_after = (
                self._retry_after_seconds(
                    response
                )
            )

            raise error

        if response.status_code in (
            self.AUTH_FAILURE_CODES
        ):
            raise ConnectorAuthenticationError(
                f"{connector_name} authentication "
                f"failed with HTTP "
                f"{response.status_code}."
            )

        if response.status_code >= 400:
            raise ConnectorRequestError(
                f"{connector_name} returned "
                f"HTTP {response.status_code}: "
                f"{response.text[:300]}"
            )

        remaining = self._rate_limit_header(
            response,
            [
                "X-RateLimit-Remaining",
                "RateLimit-Remaining",
                "x-ratelimit-remaining",
            ],
        )

        reset = self._rate_limit_header(
            response,
            [
                "X-RateLimit-Reset",
                "RateLimit-Reset",
                "x-ratelimit-reset",
            ],
        )

        return ExecutionResult(
            connector=connector_name,
            operation=operation,
            method=method.upper(),
            url=response.url,
            status_code=response.status_code,
            elapsed_seconds=round(
                elapsed,
                4,
            ),
            attempts=self._attempt_counter,
            rate_limit_remaining=remaining,
            rate_limit_reset=reset,
            response=response,
        )

    def request(
        self,
        connector_name: str,
        operation: str,
        method: str,
        endpoint: str,
        params: Optional[
            Dict[str, Any]
        ] = None,
        headers: Optional[
            Dict[str, str]
        ] = None,
        json_body: Optional[
            Dict[str, Any]
        ] = None,
        data: Any = None,
        timeout: Optional[float] = None,
    ) -> ExecutionResult:
        policy = self.registry.get_policy(
            connector_name,
            operation,
        )

        request_timeout = float(
            timeout
            or policy.get(
                "timeout_seconds",
                30,
            )
        )

        self._attempt_counter = 0

        decorated = retry(
            retry=retry_if_exception_type(
                RetryableConnectorError
            ),
            stop=stop_after_attempt(
                self.max_attempts
            ),
            wait=self._wait_before_retry,
            reraise=True,
        )(
            self._execute_once
        )

        return decorated(
            connector_name=connector_name,
            operation=operation,
            method=method,
            endpoint=endpoint,
            params=params,
            headers=headers,
            json_body=json_body,
            data=data,
            timeout=request_timeout,
        )

    def get_json(
        self,
        connector_name: str,
        operation: str,
        endpoint: str,
        params: Optional[
            Dict[str, Any]
        ] = None,
        headers: Optional[
            Dict[str, str]
        ] = None,
    ) -> Dict[str, Any]:
        result = self.request(
            connector_name=connector_name,
            operation=operation,
            method="GET",
            endpoint=endpoint,
            params=params,
            headers=headers,
        )

        try:
            return result.response.json()

        except ValueError as error:
            raise ConnectorRequestError(
                f"{connector_name} returned "
                "invalid JSON."
            ) from error
