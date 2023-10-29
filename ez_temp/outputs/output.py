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

    def write_file(self, content):
        output_file = Path(self.config.output_file)
        if content:
            try:
                if output_file.exists() and not self.config.force_overwrite:
                    raise FileExistsError(
                        f"File {output_file.name} not rendered because the file already exists\n"
                        "Use the --force option to override."
                    )
                with open(output_file, "w") as writer:
                    writer.write(content)
                    logger.debug(f"Rendered {output_file.name} template")
            except FileExistsError as e:
                logger.warning(e)

    def write_stdout(self, content):
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
            return output

        return ""

