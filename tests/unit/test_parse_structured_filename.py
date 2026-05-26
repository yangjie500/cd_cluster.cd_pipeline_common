from unittest.mock import MagicMock, patch

import pytest

from plugins.modules import parse_structured_filename


@patch("plugins.modules.parse_structured_filename.AnsibleModule")
def test_successful_parsing_with_extension(mock_ansible_module):
    """Test standard behavior with extensions and matching delimiters."""
    mock_instance = MagicMock()
    mock_instance.params = {
        "filename": "hello+--12345+--v1.1.1+--20052026T121212.tar.gz",
        "delimiter": "+--",
        "keys": ["name", "tag", "version", "datetime"],
    }
    mock_ansible_module.return_value = mock_instance
    parse_structured_filename.main()

    # Verify exit_json was triggered with valid structural data
    mock_instance.exit_json.assert_called_once()
    _, kwargs = mock_instance.exit_json.call_args
    expected = {"name": "hello", "tag": "12345", "version": "v1.1.1", "datetime": "20052026T121212"}
    assert kwargs["parsed_data"] == expected, "Parsed data did not match expected dictionary"


@patch("plugins.modules.parse_structured_filename.AnsibleModule")
def test_missing_keys_failure(mock_ansible_module):
    """Verifies failure when key list length differs from filename blocks."""
    mock_instance = MagicMock()
    mock_instance.params = {
        "filename": "hello+--12345+--v1.1.1",
        "delimiter": "+--",
        "keys": ["name", "tag"],
    }
    mock_ansible_module.return_value = mock_instance
    mock_instance.fail_json.side_effect = Exception("fail_json called")
    mock_ansible_module.return_value = mock_instance

    with pytest.raises(Exception, match="fail_json called"):
        parse_structured_filename.main()

    mock_instance.fail_json.assert_called_once()
    _, kwargs = mock_instance.fail_json.call_args

    assert "Parsing mismatch" in kwargs["msg"], "Mismatch error not returned"


@patch("plugins.modules.parse_structured_filename.AnsibleModule")
def test_parsing_with_absolute_directory_path(mock_ansible_module):
    """Verifies that directory paths are ignored and only the filename is parsed."""
    mock_instance = MagicMock()
    mock_instance.params = {
        "filename": "/var/tmp/builds/hello+--12345+--v1.1.1+--20052026T121212.tar.gz",
        "delimiter": "+--",
        "keys": ["name", "tag", "version", "datetime"],
    }
    mock_ansible_module.return_value = mock_instance

    # Execute module
    parse_structured_filename.main()

    # Verify exit_json was triggered with clean structural data
    mock_instance.exit_json.assert_called_once()
    _, kwargs = mock_instance.exit_json.call_args

    expected = {"name": "hello", "tag": "12345", "version": "v1.1.1", "datetime": "20052026T121212"}
    assert (
        kwargs["parsed_data"] == expected
    ), "Module failed to isolate filename from the directory path"


@patch("plugins.modules.parse_structured_filename.AnsibleModule")
def test_parsing_with_relative_directory_path(mock_ansible_module):
    """Verifies that relative directory paths are ignored and only the filename is parsed."""
    mock_instance = MagicMock()
    mock_instance.params = {
        "filename": "../../downloads/artifacts/hello+--12345+--v1.1.1+--20052026T121212.tar.gz",
        "delimiter": "+--",
        "keys": ["name", "tag", "version", "datetime"],
    }
    mock_ansible_module.return_value = mock_instance

    # Execute module
    parse_structured_filename.main()

    # Verify exit_json was triggered with clean structural data
    mock_instance.exit_json.assert_called_once()
    _, kwargs = mock_instance.exit_json.call_args

    expected = {"name": "hello", "tag": "12345", "version": "v1.1.1", "datetime": "20052026T121212"}
    assert (
        kwargs["parsed_data"] == expected
    ), "Module failed to isolate filename from the relative directory path"


@patch("plugins.modules.parse_structured_filename.AnsibleModule")
def test_empty_filename_failure(mock_ansible_module):
    """Verifies that a completely blank or empty filename triggers a hard failure."""
    mock_instance = MagicMock()
    mock_instance.params = {
        "filename": "   ",  # Blank spaces
        "delimiter": "+--",
        "keys": ["name", "tag"],
    }
    mock_instance.fail_json.side_effect = Exception("fail_json called")
    mock_ansible_module.return_value = mock_instance

    with pytest.raises(Exception, match="fail_json called"):
        parse_structured_filename.main()

    # Ensure it fails safely instead of continuing execution
    mock_instance.fail_json.assert_called_once()
    _, kwargs = mock_instance.fail_json.call_args
    assert "cannot be empty" in kwargs["msg"], "Module did not explicitly reject empty filename"


@patch("plugins.modules.parse_structured_filename.AnsibleModule")
def test_empty_delimiter_failure(mock_ansible_module):
    """Verifies that an empty delimiter string triggers a hard failure."""
    mock_instance = MagicMock()
    mock_instance.params = {
        "filename": "hello+--12345",
        "delimiter": "",  # Empty string
        "keys": ["name", "tag"],
    }
    mock_instance.fail_json.side_effect = Exception("fail_json called")
    mock_ansible_module.return_value = mock_instance

    with pytest.raises(Exception, match="fail_json called"):
        parse_structured_filename.main()

    mock_instance.fail_json.assert_called_once()
    _, kwargs = mock_instance.fail_json.call_args
    assert "cannot be empty" in kwargs["msg"], "Module did not explicitly reject empty delimiter"


@patch("plugins.modules.parse_structured_filename.AnsibleModule")
def test_empty_keys_list_failure(mock_ansible_module):
    """Verifies that a key list containing no valid text items triggers a hard failure."""
    mock_instance = MagicMock()
    mock_instance.params = {
        "filename": "hello+--12345",
        "delimiter": "+--",
        "keys": [""],  # List with no valid keys
    }
    mock_instance.fail_json.side_effect = Exception("fail_json called")
    mock_ansible_module.return_value = mock_instance

    with pytest.raises(Exception, match="fail_json called"):
        parse_structured_filename.main()

    mock_instance.fail_json.assert_called_once()
    _, kwargs = mock_instance.fail_json.call_args
    assert (
        "must contain at least one valid" in kwargs["msg"]
    ), "Module did not explicitly reject an empty key list"
