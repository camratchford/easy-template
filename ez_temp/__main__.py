from ez_temp.config import Config

from ez_temp.templater import Templates
from ez_temp.ingester import TemplateVars
from ez_temp.outputs import FileHandler


def main(config: Config, var_file: str, templates):
    # Create the Jinja environment
    templater = Templates(config.jinja_conf)

    # Load the TemplateVars object with the app config

    template_vars = TemplateVars(config)
    # Load the vars file into the TemplateVars object (takes precedence over global vars)
    template_vars.ingest(var_file)
    templater.env.globals = template_vars.vars

    if isinstance(templates, list):
        for t in templates:

            template_out = templater.render(t)
            # Hand the output string over to the file handler
            file_handler = FileHandler(config)

            file_handler.write_file(content=template_out, template_name=t)
        exit(0)
    else:
        template_out = templater.render(templates)
        # Hand the output string over to the file handler
        file_handler = FileHandler(config)
        file_handler.write_file(content=template_out, template_name=templates)
        exit(0)

