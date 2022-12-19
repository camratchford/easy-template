import logging
from pathlib import Path

import yaml

logger = logging.getLogger("__name__")

class TemplateVars(object):
    def __init__(self, config):
        self.var_dir = config.template_folder
        self.vars = {}
        if config.global_variables:
            self.vars = config.global_variables

    def ingest(self, var_file):
        var_file_path = Path(self.var_dir).joinpath(var_file)
        if var_file_path and var_file.endswith((".yaml", ".yml")):
            with open(str(var_file_path), "r") as file:
                self.vars.update(yaml.safe_load(file))

