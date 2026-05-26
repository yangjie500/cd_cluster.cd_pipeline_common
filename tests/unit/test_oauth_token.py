import json

from unittest.mock import Mock, patch

import pytest

from plugins.modules import oauth_token


@pytest.fixture
def base_params() -> dict:
    return {
        "token_url": "https://idp.example.com/token",
        "flow": "client_credentials",
        "client_id": "client-a",
        "client_secret": "secret",
        "username": None,
        "password": None,
        "scope": None,
        "audience": None,
        "assertion": None,
        "subject_token": None,
        "subject_token_type": "urn:ietf:params:oauth:token-type:access_token",
        "requested_token_type": "urn:ietf:params:oauth:token-type:access_token",
        "refresh_token": None,
    }


@pytest.fixture
def ansible_module(base_params: dict) -> Mock:
    module = Mock()
    module.params = base_params.copy()
    module.fail_json.side_effect = Exception("fail_json called")
    module.exit_json.side_effect = Exception("exit_json called")
    return module


@pytest.fixture
def transport() -> Mock:
    return Mock()


@patch("plugins.modules.oauth_token.RequestsHttpTransport")
@patch("plugins.modules.oauth_token.AnsibleModule")
def test_oauth_token_main_success(
    mock_ansible_module: Mock,
    mock_transport_cls: Mock,
    ansible_module: Mock,
    transport: Mock,
) -> None:
    mock_ansible_module.return_value = ansible_module

    transport.send.return_value = Mock(
        ok=True,
        status_code=200,
        body=json.dumps(
            {
                "access_token": "abc-token",
                "token_type": "Bearer",
                "expires_in": 300,
            },
        ),
        error=None,
    )
    mock_transport_cls.return_value = transport

    with pytest.raises(Exception, match="exit_json called"):
        oauth_token.main()

    ansible_module.exit_json.assert_called_once_with(
        changed=False,
        access_token="abc-token",
        token_type="Bearer",
        expires_in=300,
        refresh_token=None,
        raw={
            "access_token": "abc-token",
            "token_type": "Bearer",
            "expires_in": 300,
        },
    )


@patch("plugins.modules.oauth_token.RequestsHttpTransport")
@patch("plugins.modules.oauth_token.AnsibleModule")
def test_oauth_token_main_transport_failure(
    mock_ansible_module: Mock,
    mock_transport_cls: Mock,
    ansible_module: Mock,
    transport: Mock,
) -> None:
    mock_ansible_module.return_value = ansible_module

    transport.send.return_value = Mock(
        ok=False,
        status_code=401,
        body="unauthorized",
        error="bad credentials",
    )
    mock_transport_cls.return_value = transport

    with pytest.raises(Exception, match="fail_json called"):
        oauth_token.main()

    ansible_module.fail_json.assert_called_once_with(
        msg="Failed to obtain OAuth token",
        status_code=401,
        body="unauthorized",
        error="bad credentials",
    )


def test_build_form_data_removes_none_values() -> None:
    result = oauth_token.build_form_data(
        {
            "grant_type": "client_credentials",
            "client_id": "my-client",
            "client_secret": None,
        },
    )

    assert result == "grant_type=client_credentials&client_id=my-client"


def test_build_form_data_url_encodes_values() -> None:
    result = oauth_token.build_form_data(
        {
            "scope": "openid profile email",
        },
    )

    assert result == "scope=openid+profile+email"


def test_validate_required_client_credentials_success(
    ansible_module: Mock,
) -> None:
    oauth_token.validate_required(ansible_module)

    ansible_module.fail_json.assert_not_called()


def test_validate_required_client_credentials_missing_secret(
    ansible_module: Mock,
) -> None:
    ansible_module.params.update({"client_secret": None})
    with pytest.raises(Exception, match="fail_json called"):
        oauth_token.validate_required(ansible_module)

    ansible_module.fail_json.assert_called_once_with(
        msg="Missing required parameters for client_credentials: client_secret",
    )


def test_build_token_request_password(
    ansible_module: Mock,
) -> None:
    ansible_module.params.update(
        {
            "flow": "password",
            "username": "alice",
            "password": "password123",
        },
    )

    request = oauth_token.build_token_request(
        ansible_module,
    )

    assert "grant_type=password" in request.data
    assert "username=alice" in request.data
    assert "password=password123" in request.data


def test_build_token_request_jwt_bearer(
    ansible_module: Mock,
) -> None:
    ansible_module.params.update(
        {
            "flow": "jwt_bearer",
            "client_secret": None,
            "assertion": "jwt-assertion",
        },
    )

    request = oauth_token.build_token_request(
        ansible_module,
    )

    assert "grant_type=" "urn%3Aietf%3Aparams%3Aoauth%3Agrant-type%3Ajwt-bearer" in request.data

    assert "assertion=jwt-assertion" in request.data


def test_build_token_request_token_exchange(
    ansible_module: Mock,
) -> None:
    ansible_module.params.update(
        {
            "flow": "token_exchange",
            "audience": "loki",
            "subject_token": "existing-token",
            "subject_token_type": ("urn:ietf:params:oauth:token-type:access_token"),
            "requested_token_type": ("urn:ietf:params:oauth:token-type:access_token"),
        },
    )

    request = oauth_token.build_token_request(
        ansible_module,
    )

    assert "grant_type=" "urn%3Aietf%3Aparams%3Aoauth%3Agrant-type%3Atoken-exchange" in request.data

    assert "subject_token=existing-token" in request.data
    assert "audience=loki" in request.data


def test_build_token_request_refresh_token(
    ansible_module: Mock,
) -> None:
    ansible_module.params.update(
        {
            "flow": "refresh_token",
            "client_secret": None,
            "refresh_token": "refresh-abc",
        },
    )

    request = oauth_token.build_token_request(
        ansible_module,
    )

    assert "grant_type=refresh_token" in request.data
    assert "refresh_token=refresh-abc" in request.data


@patch("plugins.modules.oauth_token.RequestsHttpTransport")
@patch("plugins.modules.oauth_token.AnsibleModule")
def test_oauth_token_main_invalid_json_response(
    mock_ansible_module: Mock,
    mock_transport_cls: Mock,
    ansible_module: Mock,
    transport: Mock,
) -> None:
    mock_ansible_module.return_value = ansible_module

    transport.send.return_value = Mock(
        ok=True,
        status_code=200,
        body="not json",
        error=None,
    )
    mock_transport_cls.return_value = transport

    with pytest.raises(Exception, match="fail_json called"):
        oauth_token.main()

    assert ansible_module.fail_json.call_args.kwargs["msg"].startswith(
        "Token endpoint did not return valid JSON",
    )


@patch("plugins.modules.oauth_token.RequestsHttpTransport")
@patch("plugins.modules.oauth_token.AnsibleModule")
def test_oauth_token_main_missing_access_token(
    mock_ansible_module: Mock,
    mock_transport_cls: Mock,
    ansible_module: Mock,
    transport: Mock,
) -> None:
    mock_ansible_module.return_value = ansible_module

    body = json.dumps(
        {
            "token_type": "Bearer",
            "expires_in": 300,
        },
    )

    transport.send.return_value = Mock(
        ok=True,
        status_code=200,
        body=body,
        error=None,
    )
    mock_transport_cls.return_value = transport

    with pytest.raises(Exception, match="fail_json called"):
        oauth_token.main()

    ansible_module.fail_json.assert_called_once_with(
        msg="Token endpoint response does not contain access_token",
        body=body,
    )
