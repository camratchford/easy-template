
# External Jinja2 Functions (Filters and Tests)

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
