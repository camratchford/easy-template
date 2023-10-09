import json
import logging
import logging.config
import os
import sys
from pathlib import Path

from rich.logging import RichHandler

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
        # Config stuff
        self.configured = False

        self.base_dir = Path(__file__).resolve().parent
        self.cwd = Path(os.getcwd())
        self.config_file_path = ""
        self.config_file = ""
        self.dry_run = False

        # Jinja stuff
        self.external_function_dir = ""
        self.load_env_vars = False
        self.variables = []
        self.var_file = ""
        self.jinja_config = {}
        self.global_variables = {}

        # Rich/Pygments stuff
        self.rich_stdout = True
        self.rich_markdown_stdout = False
        self.rich_theme = "zenburn"

        # Application-specific stuff
        self.output_file = ""
        self.output_stub = Path(self.output_file).name if self.output_file else ""
        self.silent = False
        self.force_overwrite = False

        # Logging
        self.log_config = None
        self.configure_debug_logging()
        if self.silent:
            self.rich_stdout = False
            self.rich_markdown_stdout = False
            self.suppress_console_logging()

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
        default_log_format = "%(asctime)s\t|%(levelname)s\t|%(name)s\t%(message)s"
        logging.basicConfig(level="WARN", format="", datefmt="[%X]", handlers=[RichHandler()])

    def suppress_console_logging(self):
        logging.basicConfig(level=None, format='', handlers=None)


config = Config()








