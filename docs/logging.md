
# Logging
Easy-Template has the ability to keep and store logs. This might be useful for debugging templating errors, and other record keeping tasks.

## Logging config

Configuration of Python's logging module is done via the [`logging.dictConfig`](https://docs.python.org/3/library/logging.config.html#logging.config.dictConfig) method
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

