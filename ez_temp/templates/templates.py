import logging

from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from ez_temp.config import config
from ez_temp.templates.jinja_funcs import jinja_filters, jinja_tests, get_functions_from_dir
from ez_temp.templates.encodings import check_encoding, change_encoding


logger = logging.getLogger(__name__)


class Templates(object):
    def __init__(self, jinja_conf: dict):
        self.template_path = config.template_file
        self.tree_dir = config.tree_directory
        if self.template_path:
            self.template_parent = Path(self.template_path).parent
            self.template_name = Path(self.template_path)
            self.env = Environment(
                    loader=FileSystemLoader(self.template_parent),
                    autoescape=select_autoescape(),
            )
        elif self.tree_dir:
            self.tree_dir = Path(config.tree_directory)
            self.env = Environment(
                    loader=FileSystemLoader(self.tree_dir),
                    autoescape=select_autoescape(),
            )

        # Check if external_function_dir has subdirectories "filters" and "tests"
        if config.external_function_dir and Path(config.external_function_dir).exists():
            external_function_dir = Path(config.external_function_dir)

            # Handle filters
            filters_dir = external_function_dir.joinpath("filter")
            if filters_dir.exists():
                filters = get_functions_from_dir()
                if filters:
                    jinja_filters.update(filters)
                    for k, v in jinja_filters.items():
                        self.env.filters[k] = v

            # Handle tests
            tests_dir = external_function_dir.joinpath("tests")
            if tests_dir.exists():
                tests = get_functions_from_dir()
                if tests:
                    jinja_tests.update(tests)
                    for k, v in jinja_tests.items():
                        self.env.tests[k] = v

        # Load jinja settings
        for attr in jinja_conf.keys():
            if hasattr(self.env, attr):
                try:
                    setattr(self.env, attr, jinja_conf[attr])
                except Exception as e:
                    logger.error(e)

    def compile_tree(self):
        output_path = Path(config.output)
        if not output_path.exists() or config.force_overwrite:
            template_list = self.env.loader.list_templates()
            template_path_list = [Path(self.tree_dir).joinpath(path) for path in template_list]
            output_path_list = [self.transform_path_name(path) for path in template_list]
            for template_path in [str(p) for p in template_path_list]:
                encoding = check_encoding(template_path)
                if encoding == "binary":
                    logger.warning(f"Detected binary file {template_path}. Skipping.")

                    continue
                if encoding != "utf-8":
                    change_encoding(template_path, encoding)

            template_dict = {
                name: {
                    'path': path,
                    'content': self.env.get_template(name).render()
                } for name, path in zip(template_list, output_path_list)
            }
            return template_dict
        else:
            logger.warning(f"{output_path} already exists. Use --force flag to write to an existing directory.")

    def compile_template(self):
        if not config.output.exists() or config.force_overwrite:
            encoding = check_encoding(self.template_path)

            if encoding != "utf-8":
                change_encoding(self.template_path, encoding)

            template_name = Path(self.template_path).name
            template_dict = {
                template_name: {
                    'path': config.output,
                    'content': self.env.get_template(template_name).render()
                }
            }
            return template_dict
        else:
            logger.warning(f"{config.output} already exists. Use --force flag to overwrite an existing file.")

    def transform_path_name(self, name):
        name_path = Path(config.output).joinpath(name).resolve()
        templated_path = self.env.from_string(str(name_path)).render()
        return Path(str(templated_path))

