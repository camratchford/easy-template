import sys
import click
from ez_temp.config import config, configure_default_app_directory
from ez_temp.__main__ import main


@click.command(context_settings={"ignore_unknown_options": True})
@click.option(
    "-c",
    "--config-file",
    envvar="EZT_CONF",
    default=config.config_file,
    help="The location of the yaml configuration file",
    show_default=True,
)
@click.option(
    "-s",
    "--var-set",
    help="The name of variable set (name of the file without file extension) that will be used to template with",
)
@click.option(
    "--vars-dir",
    help="The relative or absolute path of the folder containing your vars files",
    default=config.vars_folder
)
@click.option(
    "-t",
    "--template-dir",
    help="The relative or absolute path of the folder containing your template files",
    default=config.template_folder
)
@click.option(
    "-o",
    "--output-dir",
    help="The relative or absolute path of the folder that EZT's output will be written to",
    default=config.output_folder
)
@click.option(
    "-l",
    "--logs-dir",
    help="The relative or absolute path of the folder that EZT's logs will be written to",
    default=config.logs_folder
)
@click.option(
    "-x",
    "--examples",
    is_flag=True,
    help="Will write example template and variable file to the template and vars folder.",
    # Flags always default to false
)
@click.option(
    "-f",
    "--force",
    is_flag=True,
    help="Will cause EZT to overwrite the output file if it already exists",
    # Flags always default to false
)
@click.option(
    "--debug",
    is_flag=True,
    help="Causes the logger to output to the terminal window",
    # Flags always default to false
)
@click.argument(
    "templates",
    nargs=-1,
    )
def run(
    config_file: str, var_set: str, vars_dir: str,
    template_dir: str, output_dir: str, logs_dir: str,
    examples: bool, force: bool, debug: bool, templates: list
):

    config.configure_from_file(config_file)
    configure_default_app_directory(
        config=config,
        template_dir=template_dir, vars_dir=vars_dir,
        output_dir=output_dir, logs_dir=logs_dir,
        examples=examples
    )
    config.dry_run = examples
    config.force_overwrite = force
    config.debug = debug
    main(config, var_set, [t for t in templates])


if getattr(sys, 'frozen', False):
    try:
        run.invoke(run.make_context(info_name="ezt", args=sys.argv[1:]))

    except click.exceptions.Exit as code:
        if code == 0:
            pass

    except TypeError as type_err:
        print(run.get_help(click.Context(run)))
        print(f"\nEZT ERROR: {type_err} Invalid arugment")
