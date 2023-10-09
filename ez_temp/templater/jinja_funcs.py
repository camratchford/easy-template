
import inspect
import logging

import importlib.util
from pathlib import Path

from ez_temp.config import config

logger = logging.getLogger(__name__)


def datetime_format(value, format="%H:%M %d-%m-%y"):
    return value.strftime(format)


def get_functions_from_dir():
    directory_path = config.external_function_dir
    func_dict = {}
    path_dir = Path(directory_path)

    for filename in path_dir.iterdir():
        try:
            if filename.suffix == ".py":
                module_name = filename.name

                # Load the module
                spec = importlib.util.spec_from_file_location(module_name, path_dir.joinpath(filename))
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                # Enumerate functions and add to dictionary
                for name, obj in inspect.getmembers(module):
                    if inspect.isfunction(obj):
                        func_dict[name] = obj
        except Exception as e:
            logger.error(f"Could not import functions from {filename}\n\t{e}")

    return func_dict


jinja_filters = {
    'datetime_format': datetime_format
}



