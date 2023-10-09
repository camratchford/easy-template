import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class FileHandler(object):
    def __init__(self, config):
        self.config = config
        self.force = config.force_overwrite

    def write_file(self, content):

        output_file = Path(self.config.output_file)
        if content:
            try:
                if output_file.exists() and not self.force:
                    raise FileExistsError(
                        f"File {output_file.name} not rendered because the file already exists\n"
                        "Use the --force option to override."
                    )
                with open(output_file, "w") as writer:
                    writer.write(content)
                    logger.debug(f"Rendered {output_file.name} template")
            except FileExistsError as e:
                logger.warning(e)
