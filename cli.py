import sys

import click
from click.testing import CliRunner
from ez_temp.config import config, configure_default_app_directory
from ez_temp.__main__ import main

@click.command(context_settings={"ignore_unknown_options": True})
@click.option(
    "-c",
    "--config-file",
    envvar="EZT_CONF",
    default=configure_default_app_directory(),
    help="The location of the yaml configuration file",
    show_default=True,
)
@click.option(
    "-v",
    "--var-file",
    help="The relative or absolute path of the variable file to fill the template with",
)
@click.argument("templates", nargs=-1)
def run(config_file: str, var_file: str, templates: list):
    config.configure_from_file(config_file)
    main(config, var_file, [t for t in templates])


if getattr(sys, 'frozen', False):
    run(sys.argv[1:])