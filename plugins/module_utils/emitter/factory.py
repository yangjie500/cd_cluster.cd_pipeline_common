from __future__ import annotations

from typing import Any

from ansible_collections.cd_cluster.pipeline_common.plugins.module_utils.emitter.emitter import (
    ChainEmitter,
    CloudPortalEmitter,
    Emitter,
    LokiEmitter,
)
from ansible_collections.cd_cluster.pipeline_common.plugins.module_utils.transport.transport import (  # noqa: E501
    RequestsHttpTransport,
    Transport,
)


def create_transport(name: str) -> Transport:
    if name == "requests":
        return RequestsHttpTransport()

    raise ValueError(f"Unsupported transport: {name}")


def create_emitter(
    service: str,
    endpoint: str,
    transport: Transport,
    options: dict[str, Any] | None = None,
) -> Emitter:
    """Create emitter for selected service."""

    options = options or {}

    if service == "loki":
        return LokiEmitter(
            endpoint=endpoint,
            transport=transport,
            tenant_id=options.get("tenant_id"),
            tenant_mode=options.get("tenant_mode", "header"),
            bearer_token=options.get("bearer_token"),
            verify_ssl=options.get("verify_ssl"),
        )

    if service == "custom_event":
        return CloudPortalEmitter(
            endpoint=endpoint,
            transport=transport,
            bearer_token=options.get("bearer_token"),
            verify_ssl=options.get("verify_ssl"),
        )

    raise ValueError(f"Unsupported emitter service: {service}")


def create_chain_emitter(
    configs: list[dict[str, Any]],
) -> Emitter:
    emitters: list[Emitter] = []

    for config in configs:
        transport = create_transport(config["transport"])

        emitter = create_emitter(
            service=config["service"],
            endpoint=config["endpoint"],
            transport=transport,
            options=config.get("options", {}),
        )

        emitters.append(emitter)

    return ChainEmitter(emitters)
