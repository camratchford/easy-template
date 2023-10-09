import json
import os
import tempfile
import logging
from pathlib import Path

import pytest
import yaml

from ez_temp.config import config


def test_config_initialization():
    assert config.configured == False
    assert config.base_dir == Path(__file__).resolve().parent
    assert config.cwd == Path(os.getcwd())

def test_configure_from_yaml_file():
    with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False) as temp_file:
        yaml.dump({"rich_stdout": False, "output_file": "test_output"}, temp_file)
        temp_file.close()

        config.configure_from_file(temp_file.name)

        assert config.rich_stdout == False
        assert config.output_file == "test_output"

        os.remove(temp_file.name)

def test_configure_from_json_file():
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as temp_file:
        json.dump({"rich_stdout": False, "output_file": "test_output"}, temp_file)
        temp_file.close()

        config.configure_from_file(temp_file.name)

        assert config.rich_stdout == False
        assert config.output_file == "test_output"

        os.remove(temp_file.name)

def test_configure_logging():
    config.log_config = {
        "version": 1,
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "DEBUG",
            }
        },
        "root": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
    }
    config.configure_logging()

    root_logger = logging.getLogger()
    assert root_logger.level == logging.DEBUG

def test_suppress_console_logging():

    config.suppress_console_logging()

    root_logger = logging.getLogger()
    assert root_logger.level == logging.NOTSET

