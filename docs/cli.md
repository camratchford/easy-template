## Command-line arguments

| Configuration Item    | Abrv  | Keyword Argument        | Config File Key       | Default   | Required | Description                                                                                              | 
|-----------------------|-------|-------------------------|-----------------------|-----------|---------|----------------------------------------------------------------------------------------------------------|
| config_file           | -c    | --config                | N/A                   | N/A       | No      | The location of the yaml configuration file.                                                             |
| variables             | -v    | --variables             | variables             | []        | No      | A 'a_variable=some value' pair representing a variable, [Variable arguments](vars.md)                    |
| var_file              | -V    | --var-file              | var_file              | ""        | No      | The path to a yaml file containing key: value pairs, representing variables                              |
| output                | -o    | --output                | output                | ""        | No*     | The path where you'll find the output of ezt                                                             |
| template_file         | -t    | --template-file         | N/A                   | ""        | No**    | The path pointing toward the jinja template that ezt will use to create it's output                      |
| tree_dir              | -d    | --tree-dir              | tree_directory        | ""        | No**    | Specifies the directory to recursively perform templating on                                             | 
| external_function_dir | -e    | --external-function-dir | external_function_dir | ""        | No      | The path pointing toward a folder of python files which contain jinja2 filter/test functions             |
| force_overwrite       | -f    | --force                 | force_overwrite       | False     | No      | When true, output will overwrite any file in that path                                                   | 
| load_env_vars         | --env | --load-environment-vars | load_env_vars         | False     | No      | Will load [Environment variables](vars.md) in as jinja variables                                         | 
| jinja_config          | N/A   | N/A                     | jinja_config          | ""        | No      | [Jinja templating engine options](https://jinja.palletsprojects.com/en/3.1.x/api/#high-level-api)        | 
| log_config            | N/A   | N/A                     | log_config            | {}        | No      | [logging.dictConfig](https://docs.python.org/3/library/logging.config.html#logging.config.dictConfig)    |
| global_variables      | N/A   | N/A                     | global_variables      | {}        | No      | Another, more static, way to set variables.***                                                           |
| rich_std_out          | N/A   | --no-rich-stdout        | rich_std_out          | True      | No      | Formats output string with [Rich](https://rich.readthedocs.io/en/latest/syntax.html)                     |
| rich_markdown_stdout  | N/A   | --markdown              | rich_markdown_stdout  | False     | No      | Formats output string with [Rich's Markdown module](https://rich.readthedocs.io/en/latest/markdown.html) |
| rich_theme            | N/A   | --rich-theme            | rich_theme            | "zenburn" | No      | Changes the output theme for Rich to one of the [Pygment Styles](https://pygments.org/styles/)           |


| Key | Notes                                                                                                                                                 |
|-----|-------------------------------------------------------------------------------------------------------------------------------------------------------|
| *   | Unless rich_stdout is disabled.                                                                                                                       |
| **  | You must use either the --tree or --template-file option. Using both or neither will result in an error.                                              |
| *** | Variables declared in this way will be over-ridden by any successive variable declarations. It is advised to use this method to store default values. |

