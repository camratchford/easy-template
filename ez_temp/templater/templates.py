import logging
import os

from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from ez_temp.config import config
from ez_temp.templater.jinja_funcs import jinja_filters, get_functions_from_dir
from ez_temp.templater.encodings import check_encoding, change_encoding

logger = logging.getLogger(__name__)


class Templates(object):
    def __init__(self, template_path: str, jinja_conf: dict):
        self.template_path = template_path
        self.template_parent = Path(self.template_path).parent
        self.template_name = Path(self.template_path).name
        self.env = Environment(
                loader=FileSystemLoader(self.template_parent),
                autoescape=select_autoescape(),
        )

        funcs = get_functions_from_dir()
        if funcs:
            jinja_filters.update(funcs)
        for k, v in jinja_filters.items():
            self.env.filters[k] = v

        for attr in jinja_conf.keys():
            if hasattr(self.env, attr):
                try:
                    setattr(self.env, attr, jinja_conf[attr])
                except Exception as e:
                    logger.error(e)

    def render(self) -> str:
        # Check if the template is in the template folder

        if os.path.exists(self.template_path):

            encoding = check_encoding(self.template_path)
            if encoding != "utf-8":
                change_encoding(self.template_path, encoding)
            template_name = Path(self.template_path).name
            template = self.env.get_template(template_name)
            template_out = template.render()

        else:
            logger.error(f"{self.template_path} not found")
            raise FileNotFoundError
        return template_out
