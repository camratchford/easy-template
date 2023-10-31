import logging

from pathlib import Path
from os import getcwd

from rich.console import Console
from rich.syntax import Syntax
from rich.markdown import Markdown
from pygments.styles import STYLE_MAP

logger = logging.getLogger(__name__)


class OutputHandler(object):
    def __init__(self, config):
        self.config = config

    def write_tree(self, template_dict: dict):
        if not Path(self.config.output).exists():
            Path(self.config.output).mkdir(mode=755)
        if template_dict:
            for template, properties in template_dict.items():
                name = template
                path = properties.get("path")
                parent_path = path.parent.resolve()
                content = properties.get('content')
                print(str(path))

                if not parent_path.exists():
                    parent_path.mkdir(mode=755)

                try:
                    logger.info(f"Writing {name}")

                    path.touch(exist_ok=True)
                    path.write_text(content, encoding='utf-8')
                except Exception as e:
                    logger.error(e, f"Could not write {name}")

    def write_file(self, template_dict: dict):
        if template_dict:
            name, properties = template_dict.popitem()
            path = properties.get('path')
            parent_path = path.parent.resolve()
            content = properties.get('content')

            if not parent_path.exists():
                parent_path.mkdir(mode=755)
            try:
                logger.info(f"Writing {name}")
                path.touch(exist_ok=True)
                path.write_text(content, encoding='utf-8')
            except Exception as e:
                logger.error(e, f"Could not write {name}")

    def write_stdout(self, output_path: Path):
        content = output_path.read_text()
        console = Console()
        theme = "zenburn"

        output = ""
        if self.config.rich_theme != "zenburn" and self.config.rich_theme in STYLE_MAP.keys():
            theme = self.config.rich_theme

        if self.config.rich_stdout:
            output = Syntax.from_path(str(output_path), theme=theme, background_color="default")

        elif self.config.rich_markdown_stdout:
            output = Markdown(content)

        if output and not self.config.silent:
            console.print(output)



