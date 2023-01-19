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

Ex: `~/.EasyTemplate/config.yml`
```yaml
template_folder: ~/EasyTemplate/templates
output_folder: ~/EasyTemplate/output
vars_folder: ~/EasyTemplate/vars
logs_folder: ~/EasyTemplate/logs
force_overwrite: True

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

Ex: `~/.EasyTemplatee/templates/README.md.j2`
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
Ex: `~/.EasyTemplate/templatesreadme.yml`
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

Ex: Only one file
```shell
# Config path arg is absolute, var and template args are relative to their respective directories defined in the config file
ezt -c ~/.EasyTemplate/config.yml -v readme.yml README.md.j2
```
This command reads in the config file `~/ezt/config.yml`, searches the template directory defined in the file for `readme.yml`,
then searches the template directory for `README.md.j2`.

The command outputs a file `README.md` to the output directory defined in your config.

> You can also define the location of the config file with the environment variable `EZT_CONF` <br>
> For example, you can run:
> `export EZT_CONF="~/.EasyTemplate/config.yml"`

The contents of `~/.EasyTemplate/output/README.md`:
```markdown
# How to make a cheeseburger

A simple step by step guide on how to make juicy burgers

> I am not a professional. Any injury, disablement, or deaths caused by the burgers you consume are not my fault.



- [Get meat](./docs/meats.md)

- [Cook meat](./docs/cooking.md)

- [Enjoy](./docs/enjoy.md)



Author: [Person McPersonface](https://github.com/pmcpface)

Contact: [Person.McPersonface@example.com](mailto:Person.McPersonface@example.com)
```

## Logging
Easy-Template has the ability to keep and store logs. This might be useful for debugging templating errors, and other record keeping tasks.

### Logging config

Configuration of Python's logging module is done bia the [`logging.dictConfig`](https://docs.python.org/3/library/logging.config.html#logging.config.dictConfig) method
Examples of how to implement this can be found in the [official documentation](https://docs.python.org/3/library/logging.config.html#dictionary-schema-details)

Simply add the requisite configuration in your ezt config file under the key `logging_config:`

Ex: `~/.EasyTemplate/config.yml`
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


## Author
[Cam Ratchford](https://github.com/camratchford)

## License
[CC0 1.0 Universal](./LICENSE)
