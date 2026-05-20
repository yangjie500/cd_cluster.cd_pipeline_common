from unittest.mock import MagicMock, patch

import pytest

from plugins.modules import check_archive_contents


@pytest.fixture
def mock_module_args():
    """Provides a fresh dictionary of module input arguments for each test execution."""
    return {
        "archive_path": "/mock/path/bundle.tar.gz",
        "required_files": ["config.json", "setup.sh"],
    }


@patch("tarfile.open")
def test_archive_contains_required_files_exact_match(mock_tar_open):
    """Verify matched calculation succeeds when all target files exist precisely."""
    # Setup mock tar context manager to return specific internal file path names
    mock_tar = MagicMock()
    mock_tar.getnames.return_value = ["config.json", "setup.sh", "README.md"]
    mock_tar_open.return_value.__enter__.return_value = mock_tar

    matched, found = check_archive_contents.archive_contains_required_files(
        "/mock/path/bundle.tar.gz",
        ["config.json", "setup.sh"],
    )

    assert matched is True
    assert found == ["config.json", "setup.sh"]


@patch("tarfile.open")
def test_archive_contains_required_files_nested_match(mock_tar_open):
    """Verify module can locate files when hidden inside deep archive directories."""
    mock_tar = MagicMock()
    mock_tar.getnames.return_value = ["app/src/config.json", "deploy/scripts/setup.sh"]
    mock_tar_open.return_value.__enter__.return_value = mock_tar

    matched, found = check_archive_contents.archive_contains_required_files(
        "/mock/path/bundle.tar.gz",
        ["config.json", "setup.sh"],
    )

    assert matched is True
    assert sorted(found) == ["config.json", "setup.sh"]


@patch("tarfile.open")
def test_archive_contains_required_files_partial_match(mock_tar_open):
    """Verify matched returns false if only a subset of the required list is found."""
    mock_tar = MagicMock()
    mock_tar.getnames.return_value = ["config.json", "other_file.txt"]
    mock_tar_open.return_value.__enter__.return_value = mock_tar

    matched, found = check_archive_contents.archive_contains_required_files(
        "/mock/path/bundle.tar.gz",
        ["config.json", "setup.sh"],
    )

    assert matched is False
    assert found == ["config.json"]


@patch("plugins.modules.check_archive_contents.AnsibleModule")
@patch("os.path.exists")
@patch("plugins.modules.check_archive_contents.archive_contains_required_files")
def test_run_module_execution_flow(
    mock_verify_func,
    mock_exists,
    mock_ansible_module,
    mock_module_args,
):
    """Test full standard validation loop lifecycle through the main runner block."""
    mock_exists.return_value = True
    mock_verify_func.return_value = (True, ["config.json", "setup.sh"])

    # Instantiate mock Ansible runner
    mock_instance = MagicMock()
    mock_instance.params = mock_module_args
    mock_ansible_module.return_value = mock_instance

    check_archive_contents.main()

    # Capture return arguments sent to standard exit_json loop
    mock_instance.exit_json.assert_called_once()
    kwargs = mock_instance.exit_json.call_args[1]

    assert kwargs["changed"] is False
    assert kwargs["matched"] is True
    assert kwargs["found_files"] == ["config.json", "setup.sh"]
