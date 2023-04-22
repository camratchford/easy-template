
import logging
import sys

from ez_temp.config import Config
from ez_temp.templater import Templates
from ez_temp.ingester import TemplateVars
from ez_temp.outputs import FileHandler

logger = logging.getLogger(__name__)


def main(config: Config, var_file: str, templates):
    # Create the Jinja environment
    if not config.dry_run:
        templater = Templates(config.jinja_config)
        # Load the TemplateVars object with the app config
        template_vars = TemplateVars(config)

        # Load the vars file into the TemplateVars object (takes precedence over global vars)
        template_vars.ingest(var_file)
        templater.env.globals = template_vars.vars
        file_handler = FileHandler(config)
        if not isinstance(templates, list):
            templates = [templates]
        for t in templates:
            try:
                template_out = templater.render(t)

            except FileNotFoundError as e:
                logger.error(msg=f"Template [{t}] not found", exc_info=e)
                sys.exit(100)

            except Exception as e:
                logger.error(e)
                sys.exit(1)

            if template_out:
                try:
                    # Hand the output string over to the file handler
                    file_handler.write_file(content=template_out, template_name=t)

                except FileExistsError as e:
                    logger.error(e)
                    sys.exit(200)

                except Exception as e:
                    logger.error(e)
                    sys.exit(1)



