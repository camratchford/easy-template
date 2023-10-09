
import logging
import os.path

from pathlib import Path

import yaml

from ez_temp.variables.environment_variables import collect_variables

logger = logging.getLogger(__name__)


class TemplateVars(object):
    def __init__(self, config):
        self.vars = {}
        if config.global_variables:
            self.vars.update(config.global_variables)

    def load_file(self, var_file=None):
        if os.path.exists(var_file):
            try:
                with open(var_file, "r") as file:
                    self.vars.update(yaml.safe_load(file))
            except Exception as e:
                logger.error(e)

    def load(self, variables: list = None):
        if variables:
            for v in variables:
                try:
                    split_var = v.split("=")
                    if r"\," in split_var[1]:
                        split_var[1] = split_var[1].split(r"\,")
                    self.vars[split_var[0]] = split_var[1]
                except ValueError as e:
                    logger.error(f"Variable {v} could not be parsed\n\t{e}")


    def load_env(self):
        self.vars.update(collect_variables())
