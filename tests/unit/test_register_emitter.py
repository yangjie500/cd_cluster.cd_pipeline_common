from __future__ import annotations

import json

from pathlib import Path
from unittest.mock import Mock, patch

from plugins.modules import register_emitter


@patch("plugins.modules.register_emitter.AnsibleModule")
@patch("plugins.modules.register_emitter.generate_registration_id")
def test_register_emitter_success(
    mock_generate_registration_id: Mock,
    mock_ansible_module: Mock,
    tmp_path: Path,
) -> None:
    mock_generate_registration_id.return_value = "abc123"

    module = Mock()
    module.params = {
        "emitters": [
            {
                "service": "loki",
                "transport": "requests",
                "endpoint": "https://gateway.example.com/api/logs/v1/{tenant}/loki/api/v1/push",
                "options": {
                    "tenant_id": "application",
                    "tenant_mode": "path",
                },
            },
        ],
    }
    module.check_mode = False
    mock_ansible_module.return_value = module

    with patch.object(register_emitter, "STATE_DIR", tmp_path):
        register_emitter.main()

    expected_file = tmp_path / "abc123.json"

    assert expected_file.exists()
    assert expected_file.stat().st_mode & 0o777 == 0o600

    data = json.loads(expected_file.read_text())

    assert data == {
        "version": 1,
        "emitters": module.params["emitters"],
    }

    module.exit_json.assert_called_once_with(
        changed=True,
        msg="Emitter configuration registered",
        registration_id="abc123",
    )

    module.fail_json.assert_not_called()


def test_generate_registration_id_returns_hex_string() -> None:
    registration_id = register_emitter.generate_registration_id()

    assert isinstance(registration_id, str)
    assert len(registration_id) == 32
