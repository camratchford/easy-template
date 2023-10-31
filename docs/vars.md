## Variables

The variables are applied in the following order, with each instance of a variable being overwritten by any subsequent instances.

1. Global variables (defined in the config file under the key `global_variables`)
2. Environment Variables (If the `--env/--load-environment-vars` flag is set)
3. Variable Files (Variables within a yaml file defined in the `-V/--var-file` argument)
4. Argument Variables (Variables defined using the `-v/--variables` argument)



## Environment Variables

You can enable the loading of environment variables by supplying either of the `--env/--load-environment-variables` flags during command execution
or adding `load_env_vars: true` to the ezt config file (which is defined with the `-c path_to_config.yml` argument)


### Dynamic variables
When the load_environment_variables configuration item is enabled, the following variables will be available for use within the template engine:

- `now` (The string output of datetime.now() method)
- `os`
  - `os.name` (The name of the current machine's operating system)
- `sys`
  - `sys.defaultencoding` (the output of sys.getdefaultencoding() method)
  - `sys.platform` (the output of sys.platform variable)
  - `sys.winver` (If the detected OS is windows, it will output the current major version of windows)
- `environ`
  - `environ.PATH` (Will output the value of the environment variable `PATH`)
  - `environ.RANDOM_VARIABLE_I_SET` (Will output the value of the environment variable `RANDOM_VARIABLE_I_SET`)
  - Every other environment variable in the user's current environment will be exposed under the `environ` key

### Usage

Template:
```jinja2
Date: {{ now }}
Operating system: {{ os.name }}
PATH: {{ environ.PATH }}
```

Result:
```text
Date: 30-10-23 16:38
Operating system: posix
PATH: /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
```


## Argument Variables

- You can define variables using the `-v "variable_name=variable_value"` argument
- You may use multiple `-v` arguments
- One variable per `-v` argument, where the variable name (key) to the left of a `=`, with the value of the variable to the right of the `=`.
- Lists can be used as values by separating list items with the two characters `\,`
  - For example: `-v "my_list=item 1\,item 2\,item 3\,"`
  - Which turns into a python list object equivalent to `{my_list: ["item 1", "item 2", "item 3"]}`