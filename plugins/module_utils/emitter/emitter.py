from __future__ import annotations

import json
import time

from abc import ABC, abstractmethod
from typing import Literal

from ansible_collections.cd_cluster.pipeline_common.plugins.module_utils.emitter.models import (
    Signal,
)
from ansible_collections.cd_cluster.pipeline_common.plugins.module_utils.transport.models import (
    TransportRequest,
    TransportResponse,
)
from ansible_collections.cd_cluster.pipeline_common.plugins.module_utils.transport.transport import (  # noqa: E501
    Transport,
)


class Emitter(ABC):
    @abstractmethod
    def emit(self, signal: Signal) -> TransportResponse:
        pass


class ChainEmitter(Emitter):
    """Decorator Pattern to accomodate multiple emitter if defined"""

    def __init__(self, emitters: list[Emitter]) -> None:
        self.emitters = emitters

    def emit(self, signal: Signal) -> TransportResponse:
        errors: list[str] = []

        for emitter in self.emitters:
            response = emitter.emit(signal)

            if response.ok:
                return response

            errors.append(response.error or response.body)

        return TransportResponse(
            ok=False,
            status_code=None,
            body="",
            headers={},
            error="; ".join(errors),
        )


class LokiEmitter(Emitter):
    """Send logs to Loki service"""

    def __init__(
        self,
        endpoint: str,
        transport: Transport,
        tenant_id: str | None = None,
        tenant_mode: Literal["header", "path", "none"] = "header",
        bearer_token: str | None = None,
        verify_ssl: bool = False,
    ) -> None:
        self.endpoint = endpoint
        self.transport = transport
        self.tenant_id = tenant_id
        self.tenant_mode = tenant_mode
        self.bearer_token = bearer_token
        self.verify_ssl = verify_ssl

    def _build_target(self) -> str:
        if self.tenant_mode == "path":
            if not self.tenant_id:
                raise ValueError("tenant_id is required when tenant_mode='path'")

            return self.endpoint.format(
                tenant=self.tenant_id,
                tenant_id=self.tenant_id,
            )

        return self.endpoint

    def _build_headers(self) -> dict[str, str]:
        headers = {
            "Content-Type": "application/json",
        }

        if self.tenant_mode == "header":
            if not self.tenant_id:
                raise ValueError("tenant_id is required when tenant_mode='header'")

            headers["X-Scope-OrgID"] = self.tenant_id

        if self.bearer_token:
            headers["Authorization"] = f"Bearer {self.bearer_token}"

        return headers

    def _build_stream_labels(
        self,
        signal: Signal,
    ) -> dict[str, str]:
        """Build Loki indexed stream labels. Nested Dict is not supported"""

        labels = {
            "event_type": signal.event_type,
        }

        indexed_data = signal.payload.get(
            "indexed_data",
            {},
        )

        if not isinstance(indexed_data, dict):
            raise ValueError(
                "payload.indexed_data must be a dictionary",
            )

        for key, value in indexed_data.items():
            if isinstance(value, str):
                labels[key] = value
            elif isinstance(value, (int, float, bool)):
                labels[key] = str(value)

        return labels

    def _build_log_body(self, signal: Signal) -> str:
        """Build Loki log line body as JSON string."""

        data = signal.payload.get("data", {})

        if not isinstance(data, dict):
            raise ValueError("payload.data must be a dictionary")

        body = {
            "signal_id": signal.signal_id,
            "correlation_id": signal.correlation_id,
            "event_type": signal.event_type,
            "message": signal.message,
            "data": data,
        }

        return json.dumps(body, separators=(",", ":"))

    def emit(self, signal: Signal) -> TransportResponse:
        loki_payload = {
            "streams": [
                {
                    "stream": self._build_stream_labels(signal),
                    "values": [
                        [
                            str(time.time_ns()),
                            self._build_log_body(signal),
                        ],
                    ],
                },
            ],
        }

        request = TransportRequest(
            method="POST",
            target=self._build_target(),
            headers=self._build_headers(),
            json=loki_payload,
            ssl_verify=self.verify_ssl,
        )

        return self.transport.send(request)


class CloudPortalEmitter(Emitter):
    """Send custom event by CloudPortal payload."""

    def __init__(
        self,
        endpoint: str,
        transport: Transport,
        bearer_token: str | None = None,
        verify_ssl: bool = False,
    ) -> None:
        self.endpoint = endpoint
        self.transport = transport
        self.bearer_token = bearer_token
        self.verify_ssl = verify_ssl

    def _build_headers(self) -> dict[str, str]:
        """Build HTTP request headers."""

        headers = {
            "Content-Type": "application/json",
        }

        if self.bearer_token:
            headers["Authorization"] = f"Bearer {self.bearer_token}"

        return headers

    def _build_body(
        self,
        signal: Signal,
    ) -> dict[str, object]:
        """Build custom event body."""

        job_id = signal.payload.get("job_id")
        job_status = signal.payload.get("job_status")

        if not job_id:
            raise ValueError(
                "payload.job_id is required",
            )

        if not job_status:
            raise ValueError(
                "payload.job_status is required",
            )

        if not signal.event_type:
            raise ValueError(
                "signal.event_type is required",
            )

        if not signal.message:
            raise ValueError(
                "signal.message is required",
            )

        return {
            "eventType": signal.event_type,
            "message": signal.message,
            "jobId": job_id,
            "correlationId": signal.payload.get(
                "correlation_id",
            ),
            "idempotencyKey": signal.payload.get(
                "idempotency_key",
            ),
            "jobStatus": job_status,
            "secret": signal.payload.get(
                "secret",
            ),
        }

    def emit(
        self,
        signal: Signal,
    ) -> TransportResponse:
        """Send custom event payload."""

        request = TransportRequest(
            method="POST",
            target=self.endpoint,
            headers=self._build_headers(),
            json=self._build_body(signal),
            ssl_verify=self.verify_ssl,
        )

        return self.transport.send(request)
