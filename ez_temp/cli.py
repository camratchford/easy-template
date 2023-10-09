import os.path
import sys
import click
from ez_temp.config import config
from ez_temp.__main__ import main


@click.command(context_settings={"ignore_unknown_options": True})
@click.option(
    "-c",
    "--config-file",
    type=str,
    help="The location of the yaml configuration file",
    required=False,
    show_default=True,
)
@click.option(
    "-v",
    "--variables",
    multiple=True,
    required=False,
    type=str,
    help="A 'a_variable=some value' pair representing a variable, may be used multiple times",

)
@click.option(
    "--var-file",
    required=False,
    type=str,
    help="The path to a yaml file containing key: value pairs, representing variables",
)
@click.option(
    '-o',
    "--output-file",
    required=True,
    type=str,
    help="The path where you'll find the output of ezt",
)
@click.option(
    '-t',
    "--template-file",
    required=True,
    type=str,
    help="The path pointing toward the jinja template that ezt will use to create it's output",
)
@click.option(
    "--external-function-dir",
    required=False,
    type=str,
    help="The path pointing toward a folder of python files which contain jinja2 filter functions",
)
@click.option(
    "-f",
    "--force",
    default=False,
    type=bool,
    is_flag=True,
    help="When true, output will overwrite any file in that path",
)
@click.option(
    "--silent",
    default=False,
    type=bool,
    is_flag=True,
    help="Suppress logging to stdout and stderr",
)
@click.option(
    "--load-environment-vars",
    required=False,
    type=bool,
    is_flag=True,
    help="Will load environment variables in as jinja variables",
)
@click.option(
    "--no-rich-stdout",
    default=False,
    type=bool,
    is_flag=True,
    help="Disabled output string formatting with Rich",
)
@click.option(
    "--markdown",
    required=False,
    type=bool,
    is_flag=True,
    help="Formats output string with Rich's Markdown module",
)
@click.option(
    "--rich-theme",
    required=False,
    type=str,
    help="Changes the output theme for Rich to one of the Python Pygment module's styles",
)
def run(
    config_file: str,
    variables: list,
    var_file: str,
    output_file: str,
    template_file: str,
    external_function_dir: str,
    force: bool,
    silent: bool,
    load_environment_vars: bool,
    no_rich_stdout: bool,
    markdown: bool,
    rich_theme: str,
):
    if config_file:
        if not os.path.exists(config_file):
            print(f"{config_file} not found")
            raise FileNotFoundError
        config.configure_from_file(config_file)
    config.variables = variables
    if var_file:
        if not os.path.exists(var_file):
            print(f"{var_file} not found")
            raise FileNotFoundError
        config.var_file = var_file
    config.output_file = output_file
    if external_function_dir:
        if not os.path.exists(external_function_dir):
            print(f"{external_function_dir} not found")
            raise FileNotFoundError
        config.external_function_dir = external_function_dir
    if no_rich_stdout:
        config.rich_stdout = False
    if markdown:
        config.rich_markdown_stdout = True
    if rich_theme:
        config.rich_theme = rich_theme
    config.load_env_vars = load_environment_vars

    config.force_overwrite = force
    config.silent = silent
    main(config, template_file)


if getattr(sys, 'frozen', False):
    try:
        run.invoke(run.make_context(info_name="ezt", args=sys.argv[1:]))

    except click.exceptions.Exit as code:
        if code == 0:
            pass

    except TypeError as type_err:
        print(run.get_help(click.Context(run)))
        print(f"\nEZT ERROR: {type_err} Invalid arugment")
