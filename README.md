<!--suppress ALL -->
<h1 align="center">Easy Template</h1>
<p align="center">
Quick and Dirty Jinja templating from CLI with YAML
</p>

---

> <p align="center">
>  This is a work in progress, subject to many changes and new instabilities / brokenness.
> </p>

## Introduction
This project was made because I liked the templating workflow that's present in Ansible,
but I found that installing Ansible just for the templating is kind of inconvenient.

So here we have the jinja templating system ingesting YAML, all run via some click CLI commands.  
No inventory, group_vars, hostnames, or other Ansible-related considerations necessary.


## Getting started

### Install easy-template:
```shell
python3 -m venv venv
source venv/bin/activate
pip install git+https://github.com/camratchford/easy-template
```



### Create config file:

Ex: [example_files/config.yml](example_files/config.yml)
```yaml
external_function_dir: ./path/to/jinja_functions
force_overwrite: True
load_env_vars: True
debug: False

# Parameters from https://jinja.palletsprojects.com/en/3.1.x/api/#high-level-api are passed to the Jinja environment object
jinja_config:
  trim_blocks: False
  newline_sequence: '\n'
  keep_trailing_newline: False
  auto_reload: False
  optimized: True

# Will be applied to every template, but can be over-ridden by var files
global_variables:
  name: Person McPersonface
  email: Person.McPersonface@example.com
  github_profile: https://github.com/pmcpface

```

### Create template file

Ex: [example_files/readme_template.md.j2](example_files/readme_template.md.j2)
```markdown


# {{ title }}

{{ description }}

> {{ disclaimer }}

{% if toc %}
{% for t in toc %}
- [{{ t.label }}]({{ t.link }})
{% endfor %}
{% endif %}

Author: [{{ name }}]({{ github_profile }})

Contact: [{{ email }}](mailto:{{ email }})
```

### Create var file:
Ex: [example_files/vars.yml](example_files/vars.yml)
```yaml

title: How to make a cheeseburger
description: A simple step by step guide on how to make juicy burgers
disclaimer: I am not a professional. Any injury, disablement, or deaths caused by the burgers you consume are not my fault.
toc:
  - label: Get meat
    link: ./docs/meats.md
  - label: Cook meat
    link: ./docs/cooking.md
  - label: Enjoy
    link: ./docs/enjoy.md
```

### Run

Ex: [example_files/example_script.sh](example_files/example_script.sh)
```shell
# Config path arg is absolute, var and template args are relative to their respective directories defined in the config file
ezt.exe --force \
  -c "example_files/config.yml" \
  -t "example_files/readme_template.md.j2" \
  -v "title=How do you make a cheeseburger?" \
  --var-file "example_files/vars.yml" \
  -o "example_files/README.md"
```
This command reads in the config file `~/ezt/config.yml`, parses the variables in `~/vars/templatesreadme.yml`,
loads the variables defined in the `-v` argument, then processes the template with the loaded variables, outputting the file
in the path defined with the `-o` argument

The command outputs a file `README.md` to the output directory defined in your config.

Ex: The contents of [example_files/README.md](example_files/README.md)

```markdown
# How do you make a cheeseburger?

A simple step by step guide on how to make juicy burgers

> I am not a professional. Any injury, disablement, or deaths caused by the burgers you consume are not my fault.



- [Get meat](./docs/meats.md)

- [Cook meat](./docs/cooking.md)

- [Enjoy](./docs/enjoy.md)



Author: [Person McPersonface](https://github.com/pmcpface)

Contact: [Person.McPersonface@example.com](mailto:Person.McPersonface@example.com)
```

---

## Command-line arguments

| Configuration Item    | Abrv  | Keyword Argument        | Config File Key       | Default   | Required | Description                                                                                              | 
|-----------------------|-------|-------------------------|-----------------------|-----------|---------|----------------------------------------------------------------------------------------------------------|
| config_file           | -c    | --config                | N/A                   | N/A       | No      | The location of the yaml configuration file.                                                             |
| variables             | -v    | --variables             | variables             | []        | No      | A 'a_variable=some value' pair representing a variable, [Variable arguments](docs/variable_arguments.md) |
| var_file              | -V    | --var-file              | var_file              | ""        | No      | The path to a yaml file containing key: value pairs, representing variables                              |
| output                | -o    | --output                | output                | ""        | No*     | The path where you'll find the output of ezt                                                             |
| template_file         | -t    | --template-file         | N/A                   | ""        | No**    | The path pointing toward the jinja template that ezt will use to create it's output                      |
| tree_dir              | -d    | --tree-dir              | tree_directory        | ""        | No**    | Specifies the directory to recursively perform templating on                                             | 
| external_function_dir | -e    | --external-function-dir | external_function_dir | ""        | No      | The path pointing toward a folder of python files which contain jinja2 filter/test functions             |
| force_overwrite       | -f    | --force                 | force_overwrite       | False     | No      | When true, output will overwrite any file in that path                                                   |
| load_env_vars         | --env | --load-environment-vars | load_env_vars         | False     | No      | Will load [Environment variables](docs/environment_variables.md) in as jinja variables                   | 
| jinja_config          | N/A   | N/A                     | jinja_config          | ""        | No      | [Jinja templating engine options](https://jinja.palletsprojects.com/en/3.1.x/api/#high-level-api)        | 
| log_config            | N/A   | N/A                     | log_config            | {}        | No      | [logging.dictConfig](https://docs.python.org/3/library/logging.config.html#logging.config.dictConfig)    |
| global_variables      | N/A   | N/A                     | global_variables      | {}        | No      | Another, more static, way to set variables.***                                                           |
| rich_std_out          | N/A   | --no-rich-stdout        | rich_std_out          | True      | No      | Formats output string with [Rich](https://rich.readthedocs.io/en/latest/syntax.html)                     |
| rich_markdown_stdout  | N/A   | --markdown              | rich_markdown_stdout  | False     | No      | Formats output string with [Rich's Markdown module](https://rich.readthedocs.io/en/latest/markdown.html) |
| rich_theme            | N/A   | --rich-theme            | rich_theme            | "zenburn" | No      | Changes the output theme for Rich to one of the [Pygment Styles](https://pygments.org/styles/)           |
| export_config         | N/A   | --export-config         | export_config         | False     | No      | When true, the current set of configuration items will be exported to ./export_config.yml                | 


| Key | Notes                                                                                                                                                 |
|-----|-------------------------------------------------------------------------------------------------------------------------------------------------------|
| *   | Unless rich_stdout is disabled.                                                                                                                       |
| **  | You must use either the --tree or --template-file option. Using both or neither will result in an error.                                              |
| *** | Variables declared in this way will be over-ridden by any successive variable declarations. It is advised to use this method to store default values. |


---

## Variables

The variables are applied in the following order, with each instance of a variable being overwritten by any subsequent instances.

1. Global variables (defined in the config file under the key `global_variables`)
2. [Environment variables](docs/environment_variables.md) (If the `load_env_vars` configuration item is set to True)
3. Variable file (Variables within a yaml file defined in the --var-file argument)
4. [Variable arguments](docs/variable_arguments.md) (Variables defined using the `-v` argument)

---

## External Jinja2 Functions (Filters and Tests)

To use external Jinja2 filter functions, you may the switch `--external-function-dir path/to/function/dir` or the config file key `external_function_dir: some/path/to/function/`,
to point to a path containing any number of the 2 python modules "filters" and "tests".

> Setting the variable
> `--external-function-dir ~\ezt\example_external_functions`

```yaml
# Example directory tree:
~\ezt\example_external_functions\
~\ezt\example_external_functions\filters\
~\ezt\example_external_functions\filters\filters.py
~\ezt\example_external_functions\tests\
~\ezt\example_external_functions\tests\tests.py
```

Each function contained in either "filters" or "tests" modules will be merged into the set of filters and tests available to the user in jinja template tags 
It will be helpful to read the official Jinja2 documentation on the subjects 
 - [fiters](https://jinja.palletsprojects.com/en/3.1.x/api/#writing-filters)
 - [tests](https://jinja.palletsprojects.com/en/3.1.x/api/#custom-tests)

---

## Logging
Easy-Template has the ability to keep and store logs. This might be useful for debugging templating errors, and other record keeping tasks.

### Logging config

Configuration of Python's logging module is done bia the [`logging.dictConfig`](https://docs.python.org/3/library/logging.config.html#logging.config.dictConfig) method
Examples of how to implement this can be found in the [official documentation](https://docs.python.org/3/library/logging.config.html#dictionary-schema-details)

Simply add the requisite configuration in your ezt config file under the key `logging_config:`

Ex: `~/example_files/config.yml`
```yaml
# ...
# Your normal config keys above

log_config:
  version: 1
  disable_existing_loggers: True
  formatters:
    verbose:
      fmt: |
        %(process)s -> %(filename)s -> %(levelprefix)s -> %(module)s -> %(funcName)s -> %(lineno)s ->> %(message)s
      use_colors: True
  handlers:
    default:
      class : logging.handlers.RotatingFileHandler
      formatter: verbose
      filename: ez_temp.log
      maxBytes: 1024
      backupCount: 3
  loggers:
    ez_temp:
      handlers: default
      level: DEBUG
      propagate: True
```

---

## Compiling

### Linux

- Make sure you have the python & python-dev >= 3.8 installed
- Create a virtual environment
- Install the package

```shell
cd ./EasyTemplate
python3 -m venv venv
source venv/bin/activate
pip install .
```

- Compile

```shell
cd ./compilation
bash ./compile.sh
```

- Copy it somewhere in $PATH

```shell
cp ./build/ezt /usr/bin/ezt
```

### Windows

- Make sure Python >= 3.8 is installed
- (for some reason) Install pyinstaller to your system Python interpreter's library

```powershell
pip install pyinstaller
```

- Run the PowerShell script

```powershell
cd .\EasyTemplate\compilation\
# It will create the venv and test the program
.\compile.ps1
```

---

## Author
[Cam Ratchford](https://github.com/camratchford)

---

## License
[CC0 1.0 Universal](./LICENSE)

---