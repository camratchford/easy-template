## Quickstart

## Install easy-template:
```shell
python3 -m venv venv
source venv/bin/activate
pip install git+https://github.com/camratchford/easy-template
```



## Create config file:

Ex: Repository's [example_files/config.yml](https://github.com/camratchford/easy-template/example_files/config.yml)

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

## Create template file

Ex: Repository's [example_files/readme_template.md.j2](https://github.com/camratchford/easy-template/example_files/readme_template.md.j2)

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

## Create var file:

Ex: Repository's [example_files/vars.yml](https://github.com/camratchford/easy-template/example_files/vars.yml)

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

## Run

Ex: Repository's [example_files/example_script.sh](https://github.com/camratchford/easy-template/example_files/example_script.sh)

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

Ex: The contents of the repository's [example_files/README.md](https://github.com/camratchford/easy-template/example_files/README.md)

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