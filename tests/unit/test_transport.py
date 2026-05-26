from unittest.mock import Mock, patch

import requests

from plugins.module_utils.transport.models import TransportRequest
from plugins.module_utils.transport.transport import RequestsHttpTransport


@patch("plugins.module_utils.transport.transport.requests.request")
def test_requests_http_transport_success(
    mock_request: Mock,
) -> None:
    fake_response = Mock()
    fake_response.ok = True
    fake_response.status_code = 200
    fake_response.text = "success"
    fake_response.headers = {"Content-Type": "application/json"}

    mock_request.return_value = fake_response

    transport = RequestsHttpTransport()

    request = TransportRequest(
        method="POST",
        target="https://example.com/api",
        headers={"Content-Type": "application/json"},
        params={"a": "1"},
        json={"hello": "world"},
        timeout=10,
    )

    response = transport.send(request)

    assert response.ok is True
    assert response.status_code == 200
    assert response.body == "success"
    assert response.headers == {"Content-Type": "application/json"}
    assert response.error is None

    mock_request.assert_called_once_with(
        method="POST",
        url="https://example.com/api",
        headers={"Content-Type": "application/json"},
        params={"a": "1"},
        json={"hello": "world"},
        data=None,
        timeout=10,
        verify=True,
    )


@patch("plugins.module_utils.transport.transport.requests.request")
def test_requests_http_transport_client_error_does_not_retry(
    mock_request: Mock,
) -> None:
    fake_response = Mock()
    fake_response.ok = False
    fake_response.status_code = 400
    fake_response.text = "bad request"
    fake_response.headers = {}

    mock_request.return_value = fake_response

    transport = RequestsHttpTransport()

    request = TransportRequest(
        method="POST",
        target="https://example.com/api",
        headers={},
        json={"bad": "payload"},
    )

    response = transport.send(request)

    assert response.ok is False
    assert response.status_code == 400
    assert response.body == "bad request"
    assert response.error is None

    assert mock_request.call_count == 1


@patch("plugins.module_utils.transport.transport.requests.request")
def test_requests_http_transport_retries_on_server_error(
    mock_request: Mock,
) -> None:
    fake_503 = Mock()
    fake_503.ok = False
    fake_503.status_code = 503
    fake_503.text = "service unavailable"
    fake_503.headers = {}

    fake_200 = Mock()
    fake_200.ok = True
    fake_200.status_code = 200
    fake_200.text = "ok"
    fake_200.headers = {}

    mock_request.side_effect = [
        fake_503,
        fake_503,
        fake_200,
    ]

    transport = RequestsHttpTransport()

    request = TransportRequest(
        method="POST",
        target="https://example.com/api",
        headers={},
        json={"hello": "world"},
    )

    response = transport.send(request)

    assert response.ok is True
    assert response.status_code == 200
    assert response.body == "ok"
    assert response.error is None

    assert mock_request.call_count == 3


@patch("plugins.module_utils.transport.transport.requests.request")
def test_requests_http_transport_returns_error_after_retry_exhausted(
    mock_request: Mock,
) -> None:
    fake_response = Mock()
    fake_response.ok = False
    fake_response.status_code = 503
    fake_response.text = "service unavailable"
    fake_response.headers = {}

    mock_request.return_value = fake_response

    transport = RequestsHttpTransport()

    request = TransportRequest(
        method="POST",
        target="https://example.com/api",
        headers={},
        json={"hello": "world"},
    )

    response = transport.send(request)

    assert response.ok is False
    assert response.status_code is None
    assert response.body == ""
    assert "Server error: 503" in response.error

    assert mock_request.call_count == 3


@patch("plugins.module_utils.transport.transport.requests.request")
def test_requests_http_transport_retries_on_request_exception(
    mock_request: Mock,
) -> None:
    fake_response = Mock()
    fake_response.ok = True
    fake_response.status_code = 200
    fake_response.text = "ok"
    fake_response.headers = {}

    mock_request.side_effect = [
        requests.Timeout("timeout"),
        fake_response,
    ]

    transport = RequestsHttpTransport()

    request = TransportRequest(
        method="GET",
        target="https://example.com/api",
        headers={},
    )

    response = transport.send(request)

    assert response.ok is True
    assert response.status_code == 200
    assert response.body == "ok"
    assert response.error is None

    assert mock_request.call_count == 2
