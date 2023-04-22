
default_config = r"""
template_folder: ./templates
output_folder: ./outputs
vars_folder: ./vars
logs_folder: ./logs
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

# https://docs.python.org/3/library/logging.config.html#dictionary-schema-details
log_config:
  version: 1
  disable_existing_loggers: True
  formatters:
    brief:
      format: '%(message)s'
      use_colors: True
    verbose:
      format: |
        %(asctime)s:
          Level:   %(levelname)s
          File:    %(filename)s
          LineNo:  %(lineno)d
          Msg:     %(message)s
  handlers:
    file:
      class : logging.handlers.RotatingFileHandler
      formatter: verbose
      filename: ez_temp.log
      maxBytes: 1048576 # 1MB
      backupCount: 3
    console:
      class : logging.StreamHandler
      formatter: brief
      level   : DEBUG
      stream  : ext://sys.stdout
  loggers:
    ez_temp:
      handlers:
        - file
        - console
      level: DEBUG
      propagate: False

"""
