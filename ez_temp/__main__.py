
import logging
import sys

from ez_temp.config import Config
from ez_temp.templates import Templates
from ez_temp.variables import TemplateVars
from ez_temp.outputs import OutputHandler

logger = logging.getLogger(__name__)


def main(config: Config, template):
    # Create the Jinja environment
    if not config.dry_run:
        templater = Templates(template, config.jinja_config)

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
        try:
            template_out = templater.render()

        except FileNotFoundError as e:
            logger.error(msg=f"Template [{template}] not found", exc_info=e)
            sys.exit(100)

        except Exception as e:
            logger.error(e)
            sys.exit(1)

        if template_out:
            output_handler.write_file(content=template_out)
            output_handler.write_stdout(content=template_out)
            try:
                # Hand the output string over to the file handler
                pass


            except FileExistsError as e:
                logger.error(e)
                sys.exit(200)

            except Exception as e:
                logger.error(e)
                sys.exit(1)



