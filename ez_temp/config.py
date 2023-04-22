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
        self.config_file_path = self.cwd.joinpath("ezt.yml") if not os.path.exists(f"{os.getcwd()}/ezt.yml") else ""
        self.config_file = ""
        self.dry_run = False

        self.template_folder = self.cwd.joinpath("templates")
        self.output_folder = self.cwd.joinpath("outputs")
        self.vars_folder = self.cwd.joinpath("vars")
        self.logs_folder = self.cwd.joinpath("logs")

        self.force_overwrite = False
        self.jinja_config = {}
        self.global_variables = {}

        self.log_config = None

        if self.debug:
            self.configure_debug_logging()

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

    def configure_debug_logging(self):
        import logging
        logging.basicConfig(level=logging.DEBUG, format='Line %(lineno)d ;; %(filename)s ;; %(message)s')


config = Config()


def configure_default_app_directory(config: Config, template_dir, output_dir, vars_dir, logs_dir, examples):
    from ez_temp.bootstraping.default_config import default_config
    from ez_temp.bootstraping.example_files import example_vars, example_template

    template_dir = Path(template_dir)
    output_dir = Path(output_dir)
    vars_dir = Path(vars_dir)
    logs_dir = Path(logs_dir)

    # Create templates, output, and vars folders
    template_dir.mkdir(exist_ok=True, mode=777)
    output_dir.mkdir(exist_ok=True, mode=777)
    vars_dir.mkdir(exist_ok=True, mode=777)
    logs_dir.mkdir(exist_ok=True, mode=777)

    # Create the config file from the template if it doesn't already exist
    config_file_path = rf"{os.getcwd()}\ezt.yml"

    absolute_user_config_path = Path(config.config_file_path).absolute()
    absolute_default_config_path = Path(config_file_path).absolute()

    if absolute_user_config_path == absolute_default_config_path and not os.path.exists(config_file_path):
        with open(config_file_path, "w") as writer:
            writer.write(default_config)
    if examples:
        with open(template_dir.joinpath("valid_README.md.j2"), "w") as writer:
            writer.write(example_template)

        with open(vars_dir.joinpath("valid_vars.yml"), "w") as writer:
            writer.write(example_vars)









