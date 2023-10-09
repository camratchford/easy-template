import json
import logging
import logging.config
import os
import sys
from pathlib import Path

import yaml


if os.name == 'nt':
    win_ver = sys.getwindowsversion()
    if win_ver.major == 10:
        os_config = "Windows"
    else:
        raise OSError(f"Windows {win_ver.major} is not supported")
else:
    os_config = "Posix"


class Config:
    def __init__(self):
        self.configured = False
        self.debug = False
        self.base_dir = Path(__file__).resolve().parent
        self.cwd = Path(os.getcwd())
        self.config_file_path = ""
        self.config_file = ""
        self.dry_run = False

        self.external_function_dir = ""
        self.load_env_vars = False
        self.variables = []
        self.var_file = ""
        self.output_file = ""
        self.force_overwrite = False
        self.jinja_config = {}
        self.global_variables = {}

        self.log_config = None

        # todo check if template, var_file, and output_file are relative

        if self.debug:
            self.configure_debug_logging()

    def configure_from_file(self, config_file_path):
        if config_file_path:
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
                        attr_value = loaded_config[attr]
                        if isinstance(loaded_config[attr], str) and loaded_config[attr][0] == '~':
                            attr_value = loaded_config[attr].replace("~", str(Path.home()))
                        setattr(self, attr, attr_value)

            self.configured = True
            self.configure_logging()

    def configure_logging(self):
        if self.configured and self.log_config:
            log_filename = None
            try:
                log_filename = self.log_config.get("handlers").get("file").get("filename")
            except:
                pass

            if log_filename and Path(self.logs_folder).exists():
                Path(self.logs_folder).joinpath(log_filename).touch()
                if (self.log_config.get("handlers")
                    and self.log_config["handlers"].get("file")
                    and self.log_config["handlers"]["file"].get("filename")):
                
                    self.log_config["handlers"]["file"]["filename"] = Path(self.logs_folder).joinpath(log_filename)

            logging.config.dictConfig(self.log_config)

    def configure_debug_logging(self):
        import logging
        logging.basicConfig(level=logging.DEBUG, format='Line %(lineno)d ;; %(filename)s ;; %(message)s')


config = Config()








