
import logging
import sys

from ez_temp.config import Config
from ez_temp.templates import Templates
from ez_temp.variables import TemplateVars
from ez_temp.outputs import OutputHandler

logger = logging.getLogger(__name__)


def main(config: Config):
    # Create the Jinja environment
    if not config.dry_run:
        templater = Templates(config.jinja_config)

        # Load the TemplateVars object with the app config
        template_vars = TemplateVars(config)

        # Load template_vars object in order of least to most precedence
        if config.load_env_vars:
            template_vars.load_env()
        if config.var_file:
            template_vars.load_file(config.var_file)
        if config.variables:
            template_vars.load(config.variables)

        # Load the template_vars variable dictionary into the templates environment
        templater.env.globals.update(template_vars.vars)

        # Initialize the file handler
        output_handler = OutputHandler(config)
        if templater.template_path:
            template_dict = templater.compile_template()
            output_handler.write_file(template_dict)
        elif templater.tree_dir:
            template_dict = templater.compile_tree()
            output_handler.write_tree(template_dict)




