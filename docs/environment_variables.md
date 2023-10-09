# Environment Variables

You can enable the loading of environment variables by supplying the flag `--load-environment-variables` during command execution
or adding `load_env_vars: true` to the ezt config file (which is defined with the `-c path_to_config.yml` argument)

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
