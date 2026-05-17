from unittest.mock import MagicMock, mock_open, patch

import pytest

from plugins.modules import replace_placeholders


@pytest.fixture
def mock_module_args():
    """Default module arguments to clear/reset for each test."""
    return {
        "path": "/mock/path/file.txt",
        "placeholders": {"db_host": "127.0.0.1", "app_port": "8080"},
        "whole_word": False,
        "jinja_tokens": False,
        "case_sensitive": True,
        "backup": True,
    }


def test_build_pattern_default():
    """Verify default pattern correctly matches angle-brackets <key>."""
    pattern = replace_placeholders.build_pattern(
        "mykey",
        whole_word=False,
        jinja_tokens=False,
        flags=0,
    )
    assert pattern.match("<mykey>")
    assert not pattern.match("mykey")


def test_build_pattern_jinja():
    """Verify jinja option matches {{ key }} patterns including whitespace."""
    pattern = replace_placeholders.build_pattern(
        "mykey",
        whole_word=False,
        jinja_tokens=True,
        flags=0,
    )
    assert pattern.match("{{mykey}}")
    assert pattern.match("{{ mykey }}")
    assert pattern.match("{{   mykey   }}")


def test_build_pattern_whole_word():
    """Verify whole_word handles regular expression word boundaries."""
    pattern = replace_placeholders.build_pattern(
        "mykey",
        whole_word=True,
        jinja_tokens=False,
        flags=0,
    )
    text = "this is mykey text"
    matches = pattern.findall(text)
    assert len(matches) == 1

    bad_text = "this is mykey_extended text"
    bad_matches = pattern.findall(bad_text)
    assert len(bad_matches) == 0


@patch("plugins.modules.replace_placeholders.AnsibleModule")
@patch("plugins.modules.replace_placeholders.os.path.exists")
@patch(
    "plugins.modules.replace_placeholders.io.open",
    new_callable=mock_open,
    read_data="Host is <db_host> and port is <app_port>.",
)
def test_run_module_successful_replacement(
    mock_file,
    mock_exists,
    mock_ansible_module,
    mock_module_args,
):
    """Test successful substitution under normal execution parameters."""
    mock_exists.return_value = True

    # Instantiate mocked AnsibleModule and mock out its behaviors
    mock_instance = MagicMock()
    mock_instance.params = mock_module_args
    mock_instance.check_mode = False
    mock_instance.tmpdir = "/tmp"
    mock_instance.backup_local.return_value = "/mock/path/file.txt.1234.bak"
    mock_ansible_module.return_value = mock_instance

    # Run the module execution block
    replace_placeholders.run_module()

    # Capture outputs passed down to exit_json
    mock_instance.exit_json.assert_called_once()
    kwargs = mock_instance.exit_json.call_args[1]

    assert kwargs["changed"] is True
    assert kwargs["replaced_total"] == 2
    assert kwargs["replaced_per_key"] == {"db_host": 1, "app_port": 1}
    assert kwargs["backup_file"] == "/mock/path/file.txt.1234.bak"

    # Assert atomic write operation kicked off
    mock_instance.atomic_move.assert_called_once()


@patch("plugins.modules.replace_placeholders.AnsibleModule")
@patch("plugins.modules.replace_placeholders.os.path.exists")
@patch(
    "plugins.modules.replace_placeholders.io.open",
    new_callable=mock_open,
    read_data="No placeholders present here.",
)
def test_run_module_no_changes_needed(
    mock_file,
    mock_exists,
    mock_ansible_module,
    mock_module_args,
):
    """Verify behavior when no tokens are found matching keys inside targeted document."""
    mock_exists.return_value = True

    mock_instance = MagicMock()
    mock_instance.params = mock_module_args
    mock_instance.check_mode = False
    mock_ansible_module.return_value = mock_instance

    replace_placeholders.run_module()

    mock_instance.exit_json.assert_called_once()
    kwargs = mock_instance.exit_json.call_args[1]

    assert kwargs["changed"] is False
    assert kwargs["replaced_total"] == 0
    mock_instance.atomic_move.assert_not_called()


@patch("plugins.modules.replace_placeholders.AnsibleModule")
@patch("plugins.modules.replace_placeholders.os.path.exists")
def test_run_module_file_not_found(mock_exists, mock_ansible_module, mock_module_args):
    """Ensure custom module fails reliably if the path parameter points to a missing file."""
    mock_exists.return_value = False

    mock_instance = MagicMock()
    mock_instance.params = mock_module_args
    mock_ansible_module.return_value = mock_instance
    mock_instance.fail_json.side_effect = Exception("fail_json called")

    with pytest.raises(Exception, match="fail_json called"):
        replace_placeholders.run_module()

    mock_instance.fail_json.assert_called_once()
    kwargs = mock_instance.fail_json.call_args[1]
    assert "File not found" in kwargs["msg"]


@patch("plugins.modules.replace_placeholders.AnsibleModule")
@patch("plugins.modules.replace_placeholders.os.path.exists")
@patch(
    "plugins.modules.replace_placeholders.io.open",
    new_callable=mock_open,
    read_data="Host is {{ db_host }}.",
)
def test_run_module_check_mode(mock_file, mock_exists, mock_ansible_module, mock_module_args):
    """Verify check mode reports changes correctly without touching real system storage."""
    mock_exists.return_value = True

    # Shift parameters to utilize Jinja tokens
    mock_module_args["jinja_tokens"] = True

    mock_instance = MagicMock()
    mock_instance.params = mock_module_args
    mock_instance.check_mode = True  # Enable dry-run check mode
    mock_ansible_module.return_value = mock_instance

    replace_placeholders.run_module()

    mock_instance.exit_json.assert_called_once()
    kwargs = mock_instance.exit_json.call_args[1]

    assert kwargs["changed"] is True
    assert kwargs["replaced_total"] == 1

    # Structural execution guards during check mode
    mock_instance.backup_local.assert_not_called()
    mock_instance.atomic_move.assert_not_called()
