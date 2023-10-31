import json
import logging
import logging.config
import os
from pathlib import Path

from rich.logging import RichHandler

import yaml

from ez_temp.defaults import default_log_config


class Config:
    def __init__(self):
        # Config stuff

        self.disallowed_file_attrs = [
            "disallowed_file_attrs",
            "base_dir",
            "config_file_path",
            "config_file",
            "variables",
            "db",
        ]
        self.config_parameters = [
            "dry_run", "external_function_dir", "load_env_vars",
            "template_file", "tree_directory", "var_file",
            "jinja_config", "global_variables", "rich_stdout",
            "rich_markdown_stdout", "rich_theme", "output",
            "silent", "force_overwrite", "log_config", "log_path"
        ]

        self.base_dir = Path(__file__).resolve().parent
        self.config_file_path = None
        self.config_file = None
        self.dry_run = False

        # Jinja stuff
        self.external_function_dir = None
        self.load_env_vars = False
        self.variables = []
        self.template_file = None
        self.tree_directory = None
        self.var_file = None
        self.jinja_config = {}
        self.global_variables = {}

        # Rich/Pygments stuff
        self.rich_stdout = True
        self.rich_markdown_stdout = False
        self.rich_theme = "zenburn"

        # Application-specific stuff
        self.output = None
        self.output_stub = ""
        self.silent = False
        self.force_overwrite = False

        # Logging
        self.log_config = ""
        self.log_path = ""

        self.configure_logging()

        if not self.log_config:
            self.configure_debug_logging()

        if self.silent:
            self.rich_stdout = False
            self.rich_markdown_stdout = False
            self.suppress_console_logging()

    def configure_from_path(self, config_file_path):
        """
        - Reads in a yaml config file, load top level dictionary keys that match the config class'set of attrs.
        - Will ignore any keys that are contained in the 'self.disallowed_file_attrs' list.
        - Any attrs ending in 'dir' or 'path' with be cast into a Path object, then resolved.
        """
        if config_file_path:
            self.config_file_path = Path(config_file_path).resolve()
        if os.path.exists(self.config_file_path):
            self.config_file = self.config_file_path

        loaded_config = {}
        if self.config_file:
            if ".yaml" in self.config_file.suffixes or ".yml" in self.config_file.suffixes:
                with open(self.config_file, "r") as file:
                    loaded_config = yaml.safe_load(file)
            elif ".json" in self.config_file.suffixes:
                with open(self.config_file, "r") as file:
                    loaded_config = json.load(file)
            if loaded_config:
                for attr in loaded_config.keys():
                    if hasattr(self, attr) and attr not in self.disallowed_file_attrs:
                        setattr(self, attr, loaded_config[attr])
                        if len(attr) > 3 and attr[-3:] == "dir" or len(attr) > 4 and attr[-4:] == "path":
                            setattr(self, attr, Path(loaded_config[attr]).resolve())

    def configure_logging(self):
        """
        - Configures logger with log_config property.
        - If log_config is empty, a default value is set
        """
        self.config_file = default_log_config
        if self.log_config:
            if self.log_path and not self.log_config.get("log_path"):
                self.log_config["log_path"] = self.log_path

            logging.config.dictConfig(self.log_config)

    def configure_debug_logging(self):
        default_log_format = "    [bold magenta]%(name)s[/]     %(message)s"
        logging.basicConfig(level="WARN", format=default_log_format, datefmt="[%X]", handlers=[RichHandler(markup=True)])

    def suppress_console_logging(self):
        logging.basicConfig(level=None, format='', handlers=None)

    def export_config(self):
        """
        - Exports the post-configuration config parameters to ./config_export.yml
        """
        export_dict = {}
        for attr in self.config_parameters:
            export_dict[attr] = getattr(self, attr)

        config_export = Path(os.getcwd()).joinpath("config_export.yml").resolve()

        with open(config_export, "w") as file:
            yaml.dump(export_dict, file)

config = Config()








