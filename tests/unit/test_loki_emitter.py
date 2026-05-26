import json

from unittest.mock import Mock, patch

import pytest

from plugins.module_utils.emitter.emitter import LokiEmitter, Signal
from plugins.module_utils.transport.models import TransportResponse


@patch("plugins.module_utils.emitter.emitter.time.time_ns")
def test_loki_emitter_uses_header_tenant(
    mock_time_ns: Mock,
) -> None:
    mock_time_ns.return_value = 1710000000000000000

    transport = Mock()
    transport.send.return_value = TransportResponse(
        ok=True,
        status_code=204,
        body="",
        headers={},
        error=None,
    )

    emitter = LokiEmitter(
        endpoint="https://loki.example.com/loki/api/v1/push",
        transport=transport,
        tenant_id="tenant-a",
        tenant_mode="header",
    )

    signal = Signal(
        signal_id="sig-123",
        correlation_id="corr-123",
        event_type="job_started",
        message="Job started",
        payload={
            "indexed_data": {
                "job_status": "started",
                "stage": "precheck",
            },
            "data": {
                "job_id": "123",
                "count": 10,
            },
        },
    )

    response = emitter.emit(signal)

    assert response.ok is True

    transport.send.assert_called_once()

    request = transport.send.call_args.args[0]

    assert request.method == "POST"
    assert request.target == "https://loki.example.com/loki/api/v1/push"

    assert request.headers == {
        "Content-Type": "application/json",
        "X-Scope-OrgID": "tenant-a",
    }

    log_body = json.loads(request.json["streams"][0]["values"][0][1])

    assert request.json["streams"][0]["stream"] == {
        "event_type": "job_started",
        "job_status": "started",
        "stage": "precheck",
    }

    assert request.json["streams"][0]["values"][0][0] == ("1710000000000000000")

    assert log_body == {
        "signal_id": "sig-123",
        "correlation_id": "corr-123",
        "event_type": "job_started",
        "message": "Job started",
        "data": {
            "job_id": "123",
            "count": 10,
        },
    }


@patch("plugins.module_utils.emitter.emitter.time.time_ns")
def test_loki_emitter_uses_path_tenant(
    mock_time_ns: Mock,
) -> None:
    mock_time_ns.return_value = 1710000000000000000

    transport = Mock()
    transport.send.return_value = TransportResponse(
        ok=True,
        status_code=204,
        body="",
        headers={},
        error=None,
    )

    emitter = LokiEmitter(
        endpoint=("https://gateway.example.com/api/logs/v1/" "{tenant}/loki/api/v1/push"),
        transport=transport,
        tenant_id="application",
        tenant_mode="path",
    )

    signal = Signal(
        signal_id="sig-456",
        correlation_id="corr-456",
        event_type="deploy_started",
        message="Deploy started",
        payload={
            "indexed_data": {
                "app": "payment",
            },
            "data": {
                "deployment_id": "deploy-123",
            },
        },
    )

    response = emitter.emit(signal)

    assert response.ok is True

    request = transport.send.call_args.args[0]

    assert request.target == (
        "https://gateway.example.com/api/logs/v1/application/loki/api/v1/push"
    )

    assert request.headers == {
        "Content-Type": "application/json",
    }

    assert request.json["streams"][0]["stream"] == {
        "event_type": "deploy_started",
        "app": "payment",
    }

    log_body = json.loads(request.json["streams"][0]["values"][0][1])

    assert log_body == {
        "signal_id": "sig-456",
        "correlation_id": "corr-456",
        "event_type": "deploy_started",
        "message": "Deploy started",
        "data": {
            "deployment_id": "deploy-123",
        },
    }


def test_loki_emitter_header_mode_requires_tenant_id() -> None:
    transport = Mock()

    emitter = LokiEmitter(
        endpoint="https://loki.example.com/loki/api/v1/push",
        transport=transport,
        tenant_id=None,
        tenant_mode="header",
    )

    with pytest.raises(
        ValueError,
        match="tenant_id is required when tenant_mode='header'",
    ):
        emitter.emit(
            Signal(
                signal_id="sig-123",
                correlation_id=None,
                event_type="job_started",
                message="Job started",
                payload={},
            ),
        )

    transport.send.assert_not_called()


def test_loki_emitter_path_mode_requires_tenant_id() -> None:
    transport = Mock()

    emitter = LokiEmitter(
        endpoint="https://loki.example.com/loki/api/v1/push",
        transport=transport,
        tenant_id=None,
        tenant_mode="path",
    )

    with pytest.raises(
        ValueError,
        match="tenant_id is required when tenant_mode='path'",
    ):
        emitter.emit(
            Signal(
                signal_id="sig-123",
                correlation_id=None,
                event_type="job_started",
                message="Job started",
                payload={},
            ),
        )

    transport.send.assert_not_called()
