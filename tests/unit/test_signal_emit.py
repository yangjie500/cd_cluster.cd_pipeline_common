from __future__ import annotations

import json

from pathlib import Path
from unittest.mock import Mock, patch

import pytest

import plugins.modules.signal_emit as signal_emit


@patch("plugins.modules.signal_emit.AnsibleModule")
@patch("plugins.modules.signal_emit.create_chain_emitter")
def test_signal_emit_success(
    mock_create_chain_emitter: Mock,
    mock_ansible_module: Mock,
    tmp_path: Path,
) -> None:
    registration_id = "abc123"
    state_file = tmp_path / f"{registration_id}.json"

    state_file.write_text(
        json.dumps(
            {
                "version": 1,
                "emitters": [
                    {
                        "service": "loki",
                        "transport": "requests",
                        "endpoint": "https://example.com/loki",
                        "options": {
                            "tenant_id": "application",
                            "tenant_mode": "path",
                        },
                    },
                ],
            },
        ),
    )

    module = Mock()
    module.params = {
        "registration_id": registration_id,
        "event_type": "job_started",
        "message": "Job started",
        "payload": {
            "job_id": "123",
        },
    }
    module.check_mode = False
    mock_ansible_module.return_value = module

    emitter = Mock()
    emitter.emit.return_value = Mock(
        ok=True,
        status_code=204,
        body="",
        error=None,
    )
    mock_create_chain_emitter.return_value = emitter

    # with patch.object(register_emitter, "STATE_DIR", tmp_path):
    #     signal_emit.main()
    with patch.object(signal_emit, "get_state_file", return_value=state_file):
        signal_emit.main()

    mock_create_chain_emitter.assert_called_once_with(
        configs=[
            {
                "service": "loki",
                "transport": "requests",
                "endpoint": "https://example.com/loki",
                "options": {
                    "tenant_id": "application",
                    "tenant_mode": "path",
                },
            },
        ],
    )

    emitter.emit.assert_called_once()

    signal = emitter.emit.call_args.args[0]
    assert signal.event_type == "job_started"
    assert signal.message == "Job started"
    assert signal.payload == {"job_id": "123"}

    module.exit_json.assert_called_once_with(
        changed=False,
        msg="Signal emitted",
        registration_id=registration_id,
        status_code=204,
        body="",
    )

    module.fail_json.assert_not_called()


@patch("plugins.modules.signal_emit.AnsibleModule")
def test_signal_emit_missing_registration_file(
    mock_ansible_module: Mock,
    tmp_path: Path,
) -> None:
    missing_file = tmp_path / "missing123.json"

    module = Mock()
    module.params = {
        "registration_id": "missing123",
        "event_type": "job_started",
        "message": "Job started",
        "payload": {},
    }
    module.check_mode = False

    module.fail_json.side_effect = Exception("fail_json called")

    mock_ansible_module.return_value = module

    with (
        patch.object(
            signal_emit,
            "get_state_file",
            return_value=missing_file,
        ),
        pytest.raises(Exception, match="fail_json called"),
    ):
        signal_emit.main()

    module.fail_json.assert_called_once_with(
        msg="Emitter registration does not exist. Run register_emitter first.",
        registration_id="missing123",
    )

    module.exit_json.assert_not_called()


@patch("plugins.modules.signal_emit.AnsibleModule")
def test_signal_emit_state_file_has_no_emitters(
    mock_ansible_module: Mock,
    tmp_path: Path,
) -> None:
    registration_id = "abc123"
    state_file = tmp_path / f"{registration_id}.json"

    state_file.write_text(
        json.dumps(
            {
                "version": 1,
                "emitters": [],
            },
        ),
    )

    module = Mock()
    module.params = {
        "registration_id": registration_id,
        "event_type": "job_started",
        "message": "Job started",
        "payload": {},
    }
    module.check_mode = False
    mock_ansible_module.return_value = module
    module.fail_json.side_effect = Exception("fail_json called")

    with (
        patch.object(
            signal_emit,
            "get_state_file",
            return_value=state_file,
        ),
        pytest.raises(Exception, match="fail_json called"),
    ):
        signal_emit.main()

    module.fail_json.assert_called_once_with(
        msg="Emitter registration does not contain any emitters",
        registration_id=registration_id,
    )

    module.exit_json.assert_not_called()


@patch("plugins.modules.signal_emit.AnsibleModule")
@patch("plugins.modules.signal_emit.create_chain_emitter")
def test_signal_emit_emitter_failure(
    mock_create_chain_emitter: Mock,
    mock_ansible_module: Mock,
    tmp_path: Path,
) -> None:
    registration_id = "abc123"
    state_file = tmp_path / f"{registration_id}.json"

    state_file.write_text(
        json.dumps(
            {
                "version": 1,
                "emitters": [
                    {
                        "service": "loki",
                        "transport": "requests",
                        "endpoint": "https://example.com/loki",
                        "options": {},
                    },
                ],
            },
        ),
    )

    module = Mock()
    module.params = {
        "registration_id": registration_id,
        "event_type": "job_failed",
        "message": "Job failed",
        "payload": {},
    }
    module.check_mode = False
    mock_ansible_module.return_value = module
    module.fail_json.side_effect = Exception("fail_json called")

    emitter = Mock()
    emitter.emit.return_value = Mock(
        ok=False,
        status_code=503,
        body="service unavailable",
        error="Server error: 503",
    )
    mock_create_chain_emitter.return_value = emitter

    with (
        patch.object(
            signal_emit,
            "get_state_file",
            return_value=state_file,
        ),
        pytest.raises(Exception, match="fail_json called"),
    ):
        signal_emit.main()

    module.fail_json.assert_called_once_with(
        msg="Failed to emit signal",
        registration_id=registration_id,
        status_code=503,
        body="service unavailable",
        error="Server error: 503",
    )

    module.exit_json.assert_not_called()
