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
        self.base_dir = Path(__file__).resolve().parent
        self.cwd = Path(os.getcwd())
        self.config_file_path = ""
        self.config_file = ""

        self.template_folder = ""
        self.output_folder = ""
        self.vars_folder = ""
        self.logs_folder = ""

        self.force_overwrite = True
        self.jinja_config = {}
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


def configure_default_app_directory():
    from ez_temp.bootstraping.default_configs import windows_default_config, posix_default_config
    from ez_temp.bootstraping.example_files import example_vars, example_template
    app_dir_dict = {
        "Windows": {
            "parent": os.getenv('USERPROFILE'),
            "child": "EasyTemplate",
            "config": windows_default_config
        },
        "Posix": {
            "parent": os.getenv('HOME'),
            "child": ".EasyTemplate",
            "config": posix_default_config
        }
    }
    parent = app_dir_dict.get(os_config).get("parent")
    child = app_dir_dict.get(os_config).get("child")

    # Create app folder
    Path(parent).joinpath(child).mkdir(exist_ok=True)
    app_folder = Path(parent).joinpath(child)

    # Create templates, output, and vars folders
    app_folder.joinpath("templates").mkdir(exist_ok=True)
    app_folder.joinpath("output").mkdir(exist_ok=True)
    app_folder.joinpath("vars").mkdir(exist_ok=True)
    app_folder.joinpath("logs").mkdir(exist_ok=True)

    dest_template_config = app_folder.joinpath("default_config.yml")
    dest_example_template = app_folder.joinpath("templates").joinpath("valid_README.md.j2")
    dest_example_vars = app_folder.joinpath("vars").joinpath("valid_vars.yml")

    dest_path_dict = {
        "config_dest": {
            "destination_path": dest_template_config,
            "contents": app_dir_dict.get(os_config).get("config")
        },
        "template_dest": {
            "destination_path": dest_example_template,
            "contents": example_template
        },
        "vars_dest": {
            "destination_path": dest_example_vars,
            "contents": example_vars
        }
    }

    for file in ["config_dest", "template_dest", "vars_dest"]:
        if not dest_path_dict[file]["destination_path"].exists():
            with open(dest_path_dict[file]["destination_path"], "w") as writer:
                writer.write(dest_path_dict[file]["contents"])



    return dest_template_config







config = Config()
