import sys

from pathlib import Path

import click

from ez_temp.config import config
from ez_temp.__main__ import main



@click.command(context_settings={"ignore_unknown_options": True})
@click.option(
    "-c",
    "--config-file",
    "config_file",
    type=click.Path(file_okay=True, dir_okay=False, resolve_path=True),
    help="The location of the yaml configuration file",
    required=False,
    show_default=True,
)
@click.option(
    "-v",
    "--variables",
    "variables",
    multiple=True,
    required=False,
    type=str,
    help="A 'a_variable=some value' pair representing a variable, may be used multiple times",

)
@click.option(
    "-V",
    "--var-file",
    'var_file',
    required=False,
    type=click.Path(file_okay=True, dir_okay=False, resolve_path=True),
    help="The path to a yaml file containing key: value pairs, representing variables",
)
@click.option(
    '-o',
    "--output",
    "output",
    required=True,
    type=click.Path(file_okay=True, dir_okay=True),
    help="The path where you'll find the output of ezt",
)
@click.option(
    '-t',
    "--template-file",
    "template_file",
    required=False,
    type=click.Path(file_okay=True, dir_okay=False, resolve_path=True),
    help="The path pointing toward the jinja template that ezt will use to create it's output",
)
@click.option(
    "-d",
    "--tree-dir",
    "tree_dir",
    required=False,
    type=click.Path(file_okay=False, dir_okay=True, resolve_path=True),
    help="Specifies the directory to recursively perform templating on",
)
@click.option(
    "-e",
    "--external-function-dir",
    "external_function_dir",
    required=False,
    type=click.Path(file_okay=False, dir_okay=True, resolve_path=True),
    help="The path pointing toward a folder of python files which contain jinja2 filter functions",
)
@click.option(
    "-l",
    "--log-path",
    "log_path",
    type=click.Path(exists=False, file_okay=True, dir_okay=False, resolve_path=True),
    help="The location of the log file",
    required=False,
)
@click.option(
    "--export-config",
    "export_config",
    type=bool,
    help="When True, the current set pf configuration parameters will be exported to $PWD as ./export_config.yml",
    required=False,
    is_flag=True
)
@click.option(
    "-f",
    "--force",
    "force",
    default=False,
    type=bool,
    is_flag=True,
    help="When true, output will overwrite any file in that path",
)
@click.option(
    "--silent",
    "silent",
    default=False,
    type=bool,
    is_flag=True,
    help="Suppress logging to stdout and stderr",
)
@click.option(
    "--load-environment-vars",
    "load_environment_vars",
    required=False,
    type=bool,
    is_flag=True,
    help="Will load environment variables in as jinja variables",
)
@click.option(
    "--no-rich-stdout",
    "no_rich_stdout",
    default=False,
    type=bool,
    is_flag=True,
    help="Disabled output string formatting with Rich",
)
@click.option(
    "--markdown",
    "markdown",
    required=False,
    type=bool,
    is_flag=True,
    help="Formats output string with Rich's Markdown module",
)
@click.option(
    "--rich-theme",
    "rich_theme",
    required=False,
    type=str,
    help="Changes the output theme for Rich to one of the Python Pygment module's styles",
)
def run(
        config_file: str,
        variables: list,
        var_file: str,
        output: str,
        tree_dir: str,
        template_file: str,
        external_function_dir: str,
        log_path: str,
        export_config: bool,
        force: bool,
        silent: bool,
        load_environment_vars: bool,
        no_rich_stdout: bool,
        markdown: bool,
        rich_theme: str,
):
    if (not template_file and not tree_dir) or (template_file and tree_dir):
        raise click.exceptions.BadArgumentUsage("You must specify one of either: '--template-file' or '--tree'")

    if config_file:
        config.configure_from_file(config_file)
    if log_path:
        config.log_path = log_path
    if variables:
        config.variables = variables
    if var_file:
        config.var_file = Path(var_file)
    if tree_dir:
        config.tree_directory = Path(tree_dir)
    if template_file:
        config.template_file = Path(template_file)
    if output:
        config.output = Path(output)
    if external_function_dir:
        config.external_function_dir = Path(external_function_dir)
    if rich_theme:
        config.rich_theme = rich_theme

    config.rich_stdout = not no_rich_stdout
    config.rich_markdown_stdout = markdown
    config.load_env_vars = load_environment_vars
    config.force_overwrite = force
    config.silent = silent

    if export_config:
        config.export_config()

    main(config)


if getattr(sys, 'frozen', False):
    try:
        run.invoke(run.make_context(info_name="ezt", args=sys.argv[1:]))

    except click.exceptions.Exit as code:
        if code == 0:
            pass

    except click.exceptions.ClickException as e:
        print(e.message)

    except TypeError as type_err:
        print(run.get_help(click.Context(run)))
        print(f"\nEZT ERROR: {type_err} Invalid arugment")

    except Exception as e:
        print(e)