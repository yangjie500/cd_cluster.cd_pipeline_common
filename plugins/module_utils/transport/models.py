from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class TransportRequest:
    """
    Generic transport request.

    "target" is intentionally transport-agnostic.
    Could be:
    - HTTP URL
    - gRPC endpoint
    - unix socket
    - Kafka topic
    - WSL command target
    """

    method: str

    target: str

    headers: dict[str, str] = field(default_factory=dict)

    #
    # Query string parameters:
    # ?a=1&b=2
    #
    params: dict[str, str] = field(default_factory=dict)

    #
    # JSON body payload.
    #
    json: dict[str, Any] | None = None

    #
    # Raw text payload if needed.
    #
    data: str | None = None

    timeout: int = 30

    ssl_verify: bool = True


@dataclass
class TransportResponse:
    """
    Generic transport response.
    """

    ok: bool

    status_code: int | None

    body: str

    headers: dict[str, str]

    error: str | None = None
