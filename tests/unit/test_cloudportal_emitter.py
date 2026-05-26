from unittest.mock import Mock

import pytest

from plugins.module_utils.emitter.emitter import CloudPortalEmitter, Signal
from plugins.module_utils.transport.models import TransportResponse


def test_custom_event_emitter_sends_expected_body() -> None:
    transport = Mock()
    transport.send.return_value = TransportResponse(
        ok=True,
        status_code=200,
        body="ok",
        headers={},
        error=None,
    )

    emitter = CloudPortalEmitter(
        endpoint="https://node.example.com/events",
        transport=transport,
    )

    signal = Signal(
        signal_id="unused-signal-id",
        correlation_id=None,
        event_type="jobFinished",
        message="Job completed successfully",
        payload={
            "job_id": "123",
            "correlation_id": "corr-123",
            "idempotency_key": "job-123-finished",
            "job_status": "success",
            "secret": "secret-value",
        },
    )

    response = emitter.emit(signal)

    assert response.ok is True

    request = transport.send.call_args.args[0]

    assert request.method == "POST"
    assert request.target == "https://node.example.com/events"
    assert request.headers == {
        "Content-Type": "application/json",
    }
    assert request.json == {
        "eventType": "jobFinished",
        "message": "Job completed successfully",
        "jobId": "123",
        "correlationId": "corr-123",
        "idempotencyKey": "job-123-finished",
        "jobStatus": "success",
        "secret": "secret-value",
    }


def test_custom_event_emitter_adds_bearer_token() -> None:
    transport = Mock()
    transport.send.return_value = TransportResponse(
        ok=True,
        status_code=200,
        body="ok",
        headers={},
        error=None,
    )

    emitter = CloudPortalEmitter(
        endpoint="https://node.example.com/events",
        transport=transport,
        bearer_token="token-123",
    )

    emitter.emit(
        Signal(
            signal_id="unused",
            correlation_id=None,
            event_type="jobStarted",
            message="Job started",
            payload={
                "job_id": "123",
                "job_status": "running",
            },
        ),
    )

    request = transport.send.call_args.args[0]

    assert request.headers == {
        "Content-Type": "application/json",
        "Authorization": "Bearer token-123",
    }


def test_custom_event_emitter_optional_fields_can_be_none() -> None:
    transport = Mock()
    transport.send.return_value = TransportResponse(
        ok=True,
        status_code=200,
        body="ok",
        headers={},
        error=None,
    )

    emitter = CloudPortalEmitter(
        endpoint="https://node.example.com/events",
        transport=transport,
    )

    emitter.emit(
        Signal(
            signal_id="unused",
            correlation_id=None,
            event_type="jobStarted",
            message="Job started",
            payload={
                "job_id": "123",
                "job_status": "running",
            },
        ),
    )

    request = transport.send.call_args.args[0]

    assert request.json == {
        "eventType": "jobStarted",
        "message": "Job started",
        "jobId": "123",
        "correlationId": None,
        "idempotencyKey": None,
        "jobStatus": "running",
        "secret": None,
    }


def test_custom_event_emitter_requires_job_id() -> None:
    transport = Mock()
    emitter = CloudPortalEmitter(
        endpoint="https://node.example.com/events",
        transport=transport,
    )

    with pytest.raises(ValueError, match="payload.job_id is required"):
        emitter.emit(
            Signal(
                signal_id="unused",
                correlation_id=None,
                event_type="jobStarted",
                message="Job started",
                payload={
                    "job_status": "running",
                },
            ),
        )

    transport.send.assert_not_called()


def test_custom_event_emitter_requires_job_status() -> None:
    transport = Mock()
    emitter = CloudPortalEmitter(
        endpoint="https://node.example.com/events",
        transport=transport,
    )

    with pytest.raises(ValueError, match="payload.job_status is required"):
        emitter.emit(
            Signal(
                signal_id="unused",
                correlation_id=None,
                event_type="jobStarted",
                message="Job started",
                payload={
                    "job_id": "123",
                },
            ),
        )

    transport.send.assert_not_called()
