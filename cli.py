import sys

import click
from ez_temp.config import config, configure_default_app_directory
from ez_temp.__main__ import main


@click.command(context_settings={"ignore_unknown_options": True})
@click.option(
    "-c",
    "--config-file",
    envvar="EZT_CONF",
    default=configure_default_app_directory(),
    help="The location of the yaml configuration file",
    type=click.STRING,
    show_default=True,
)
@click.option(
    "-v",
    "--var-file",
    help="The relative or absolute path of the variable file to fill the template with",
    type=click.STRING
)
@click.argument(
    "templates", 
    nargs=-1,
    type=click.STRING
    )
def run(config_file: str, var_file: str, templates: list):
    config.configure_from_file(config_file)
    main(config, var_file, [t for t in templates])



def exception_handler(e):
    e_type, e_obj, tb = sys.exc_info()
    f = tb.tb_frame
    fn = f.f_code.co_filename
    ln = tb.tb_lineno


if getattr(sys, 'frozen', False):

    try:
        run.invoke(run.make_context(info_name="ezt", args=sys.argv[1:]))

    except click.exceptions.Exit as code:
        if code == 0:
            pass

    except TypeError as type_err:
        print(run.get_help(click.Context(run)))
        print(f"\nEZT ERROR: {type_err} Invalid arugment")


    