
import yaml
import json
import logging
import logging.config
import os

from pathlib import Path


class Config:
    def __init__(self):
        self.configured = False
        self.base_dir = Path(__file__).resolve().parent
        self.cwd = Path(os.getcwd())
        self.config_file_path = ""
        self.config_file = ""

        self.template_folder = []
        self.output_folder = []
        self.force_overwrite = True
        self.jinja_conf = {}
        self.global_variables = {}

        self.log_config = None

    def configure_from_file(self, config_file_path):
        self.config_file_path = config_file_path

        if Path(self.config_file_path):
            self.config_file = self.config_file_path

        loaded_config = {}
        if self.config_file:
            if self.config_file.endswith((".yaml", ".yml")):
                with open(self.config_file, "r") as file:
                    loaded_config = yaml.safe_load(file)
            elif self.config_file.endswith(".json"):
                with open(self.config_file, "r") as file:
                    loaded_config = json.load(file)
            for attr in loaded_config.keys():
                if hasattr(self, attr):
                    setattr(self, attr, loaded_config[attr])

        self.configured = True
        self.configure_logging()

    def configure_logging(self):
        if self.configured and self.log_config:
            logging.config.dictConfig(self.log_config)


config = Config()
