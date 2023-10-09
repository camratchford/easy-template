import pytest
import datetime

from pathlib import Path
from unittest.mock import patch

from ez_temp.templates.jinja_funcs import datetime_format, get_functions_from_dir
from ez_temp.config import config


@pytest.fixture
def mock_config():
    config.external_function_dir = "test_functions"
    return config


def test_datetime_format():
    dt = datetime.datetime(2023, 10, 9, 12, 34, 56)
    formatted = datetime_format(dt)
    assert formatted == "12:34 09-10-23"


def test_datetime_format_custom():
    dt = datetime.datetime(2023, 10, 9, 12, 34, 56)
    formatted = datetime_format(dt, "%Y-%m-%d %H:%M:%S")
    assert formatted == "2023-10-09 12:34:56"


def test_get_functions_from_dir_empty(mock_config):
    with patch("ez_temp.templates.jinja_funcs.Path.iterdir", return_value=[]):
        funcs = get_functions_from_dir()
    assert funcs == {}


def test_get_functions_from_dir_with_py_files(mock_config):
    def fake_iterdir():
        yield Path("fake_function.py")

    with patch("ez_temp.templates.jinja_funcs.Path.iterdir", side_effect=fake_iterdir):
        with patch("ez_temp.templates.jinja_funcs.importlib.util.spec_from_file_location") as mock_spec:
            mock_spec.return_value.loader.exec_module = lambda x: setattr(x, "fake_function", lambda: "fake")
            funcs = get_functions_from_dir()
    assert "fake_function" in funcs
    assert funcs["fake_function"]() == "fake"
