import logging

from jinja2 import Environment, FileSystemLoader, select_autoescape

from ez_temp.config import config

logger = logging.getLogger("__name__")


class Templates(object):
    def __init__(self, jinja_conf):
        self.env = Environment(
            loader=FileSystemLoader(config.template_folder),
            autoescape=select_autoescape(),
        )

        for attr in jinja_conf.keys():
            if hasattr(self.env, attr):
                try:
                    setattr(self.env, attr, jinja_conf[attr])
                except Exception as e:
                    logger.error(e)

    def render(self, template_file):
        if template_file:
            try:
                template = self.env.get_template(template_file)
                template_out = template.render()

                return template_out

            except Exception as e:
                logger.error(e)



