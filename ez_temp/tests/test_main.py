import pytest
from unittest.mock import patch, Mock
from ez_temp.__main__ import main
from ez_temp.config import config


@pytest.fixture
def mock_config():
    config.dry_run = False
    config.jinja_config = {}
    config.load_env_vars = False
    config.var_file = None
    config.variables = None
    return config


def test_main_template_not_found(mock_config):
    with patch("ez_temp.__main__.logger") as mock_logger:
        with pytest.raises(SystemExit) as e:
            main(mock_config, "nonexistent_template.j2")
        assert e.value.code == 100
        mock_logger.error.assert_called()


def test_main_generic_exception(mock_config):
    with patch("ez_temp.__main__.Templates.render", side_effect=Exception("Generic Error")):
        with patch("ez_temp.__main__.logger") as mock_logger:
            with pytest.raises(SystemExit) as e:
                main(mock_config, "template.j2")
            assert e.value.code == 1
            mock_logger.error.assert_called()


def test_main_successful_run(mock_config):
    with patch("ez_temp.__main__.Templates.render", return_value="Rendered Content"):
        with patch("ez_temp.__main__.OutputHandler.write_file") as mock_write_file:
            main(mock_config, "template.j2")
            mock_write_file.assert_called_with("Rendered Content")
            # with patch("ez_temp.__main__.OutputHandler.write_stdout") as mock_write_stdout:

                # mock_write_stdout.assert_called_with("Rendered Content")
