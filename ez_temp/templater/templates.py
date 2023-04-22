import logging
import os

from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from ez_temp.config import config
from ez_temp.templater.jinja_funcs import datetime_format
from ez_temp.templater.encodings import check_encoding, change_encoding

logger = logging.getLogger(__name__)


class Templates(object):
    def __init__(self, jinja_conf):
        self.template_folder = Path(config.template_folder)

        self.env = Environment(
            loader=FileSystemLoader(self.template_folder),
            autoescape=select_autoescape(),
        )
        self.env.filters["datetime_format"] = datetime_format

        for attr in jinja_conf.keys():
            if hasattr(self.env, attr):
                try:
                    setattr(self.env, attr, jinja_conf[attr])
                except Exception as e:
                    logger.error(e)

    def render(self, template_file):
        template_full_path = ""
        # Check if the template is in the template folder
        if os.path.exists(self.template_folder.joinpath(template_file)):
            template_full_path = self.template_folder.joinpath(template_file)
        # check if template is an absolute path
        if os.path.exists(template_file):
            template_full_path = Path(template_file)

        if not template_full_path:
            logger.error(f"{Path(self.template_folder.joinpath(template_file))} not found")
            raise FileNotFoundError

        encoding = check_encoding(template_full_path)
        if encoding != "utf-8":
            change_encoding(template_full_path, encoding)

        template = self.env.get_template(template_file)
        template_out = template.render()

        return template_out
