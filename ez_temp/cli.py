import os
import logging
from pathlib import Path

import click
from ez_temp.config import config
from ez_temp.__main__ import main

logger = logging.getLogger("__name__")

base_dir = Path(__file__).resolve().parent
cwd = Path(os.getcwd())


@click.group()
@click.option('--debug/--no-debug', default=False)
def cli(debug):
    if debug:
        click.echo(message="Debug Mode Active\n")


@cli.command(name="one", context_settings={"ignore_unknown_options": True})
@click.option(
    "-c", "--config-file",
    envvar="EZT_CONF",
    default=f"{cwd}/config.yml",
    help="The location of the yaml configuration file",
    show_default=True,
)
@click.option(
    "-v", "--var-file",
    help="The relative or absolute path of the variable file to fill the template with",
)
@click.argument(
    "template",
    nargs=-1,
)
def one(config_file: str, var_file: str, template: str):
    config.configure_from_file(config_file)
    main(config, var_file, template)


@cli.command(name="many", context_settings={"ignore_unknown_options": True})
@click.option(
    "-c", "--config-file",
    envvar="EZT_CONF",
    default=f"{cwd}/config.yml",
    help="The location of the yaml configuration file",
    show_default=True,
)
@click.option(
    "-v", "--var-file",
    help="The relative or absolute path of the variable file to fill the template with",
)
@click.argument(
    "templates",
    nargs=-1
)
def many(config_file: str, var_file: str, templates: list):
    config.configure_from_file(config_file)
    main(config, var_file, [t for t in templates])
