import logging
from pathlib import Path

logger = logging.getLogger("__name__")


class FileHandler(object):
    def __init__(self, config):
        self.template_dir = config.template_folder
        self.output_dir = config.output_folder
        self.force = config.force_overwrite

    def write_file(self, content, template_name):
        template_file = Path(self.template_dir).joinpath(template_name)

        output_file = template_file.name
        # If the template file ends in `.j2`, then strip it for the output file name.
        extensions = template_file.suffixes
        if extensions and extensions[-1] == ".j2":
            output_file = template_file.name.rstrip(extensions[-1])

        path = Path(self.output_dir).joinpath(output_file)
        if content:
            try:
                if path.exists() and not self.force:
                    raise FileExistsError(f"File {path} not rendered because the file already exists")

                with open(path, "w") as writer:
                    writer.write(content)
                    logger.debug(f"Rendered {path} template")

            except FileExistsError as e:
                logger.warning(e)
