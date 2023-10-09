import pytest
import os
from unittest.mock import patch
from ez_temp.templates.templates import Templates
from ez_temp.config import Config


@pytest.fixture
def mock_config():
    config = Config()
    config.external_function_dir = "test_functions"
    return config


@pytest.fixture
def test_template_file():
    template_path = "test_template.j2"
    with open(template_path, "w", encoding="utf-8") as f:
        f.write("Hello, {{ name }}!")
    yield template_path
    os.remove(template_path)


def test_template_initialization(test_template_file, mock_config):
    template = Templates(test_template_file, {})
    assert template.template_path == test_template_file
    assert template.template_name == "test_template.j2"


def test_template_render(test_template_file, mock_config):
    template = Templates(test_template_file, {})
    output = template.render()
    assert output == "Hello, "


def test_template_render_with_non_utf8_encoding(test_template_file, mock_config):
    with open(test_template_file, "w", encoding="latin1") as f:
        f.write("Hello, {{ name }}!")
    template = Templates(test_template_file, {})
    output = template.render()
    assert output == "Hello, "


def test_template_render_file_not_found(test_template_file, mock_config):
    with patch("ez_temp.templates.templates.logger") as mock_logger:
        with pytest.raises(FileNotFoundError):
            template = Templates("nonexistent.j2", {})
            template.render()
        mock_logger.error.assert_called_with("nonexistent.j2 not found")