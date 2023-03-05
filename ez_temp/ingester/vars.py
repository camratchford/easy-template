
import logging

from pathlib import Path

import yaml

from ez_temp.ingester.environment_variables import collect_variables

logger = logging.getLogger(__name__)


class TemplateVars(object):
    def __init__(self, config):
        self.var_dir = config.vars_folder
        self.vars = {}

        if config.global_variables:
            self.vars = config.global_variables
            self.vars.update(collect_variables())

    def ingest(self, var_file):
        # Populates environ, os, sys keys
        # Finds valid paths
        if Path(self.var_dir).joinpath(var_file).exists():
            var_files = [
                p for p in [
                    Path(self.var_dir).joinpath(var_file),
                    Path.cwd().joinpath(var_file),
                    Path(var_file)
                ] if p.exists()
            ]
            try:
                var_file_path = var_files.pop()
                if var_file_path and var_file.endswith((".yaml", ".yml")):
                    with open(str(var_file_path), "r") as file:
                        self.vars.update(yaml.safe_load(file))
            except Exception as e:
                logger.error(e)

