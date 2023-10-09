import pytest
from pathlib import Path
from unittest.mock import patch
from ez_temp.outputs.output import OutputHandler
from ez_temp.config import config

@pytest.fixture
def mock_config():
    config.output_file = "test_output.txt"
    config.force_overwrite = False
    config.rich_stdout = True
    config.rich_markdown_stdout = False
    config.silent = False
    return config


def test_write_file_existing_without_force(mock_config):
    with patch("ez_temp.outputs.output.logger") as mock_logger:
        handler = OutputHandler(mock_config)
        Path(mock_config.output_file).touch()
        handler.write_file("Test content")
        mock_logger.warning.assert_called()


def test_write_file_existing_with_force(mock_config):
    mock_config.force_overwrite = True
    handler = OutputHandler(mock_config)
    Path(mock_config.output_file).touch()
    handler.write_file("Test content")
    assert Path(mock_config.output_file).read_text() == "Test content"


def test_write_file_new(mock_config):
    handler = OutputHandler(mock_config)
    handler.write_file("Test content")
    assert Path(mock_config.output_file).read_text() == "Test content"


def test_write_stdout(mock_config):

    with patch("ez_temp.outputs.output.Console") as mock_console:
        mock_console.assert_called_with()
        handler = OutputHandler(mock_config)
        handler.write_stdout("Test content")
        mock_console.return_value.print.assert_called_with("Test content")




def test_write_stdout_silent(mock_config):
    mock_config.silent = True
    with patch("ez_temp.outputs.output.Console") as mock_console:
        handler = OutputHandler(mock_config)
        handler.write_stdout("Test content")
        mock_console.return_value.print.assert_not_called()