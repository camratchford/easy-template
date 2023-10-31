import logging

from pathlib import Path

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

    def write_stdout(self, content):
        console = Console()
        theme = "zenburn"

        if self.config.rich_theme != "zenburn" and self.config.rich_theme in STYLE_MAP.keys():
            theme = self.config.rich_theme

        output = content
        tempdir = self.config.cwd
        filename = Path(tempdir).joinpath("ezt.tmp")
        with open(filename, "w") as temp_file:
            temp_file.write(content)

        if self.config.rich_stdout:
            output = Syntax.from_path(str(filename), theme=theme, background_color="default")

        if self.config.rich_markdown_stdout:
            output = Markdown(content)

        if not self.config.silent:
            console.print(output)

        filename.unlink()

