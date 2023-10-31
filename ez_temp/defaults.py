default_log_config = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "default": {
            "format": "%(process)d:%(filename)s:%(module)s.%(funcName)s -> %(lineno)d:%(message)s",
        },
        "rich": {
            "format": "(%(name)s)[/] %(message)s",
        }
    },
    "handlers": {
        # "file": {
        #     "formatter": "default",
        #     "level": "ERROR",
        #     "class": "logging.handlers.RotatingFileHandler",
        #     "filename": "/var/log/ez_temp.log",
        #     "maxBytes": 1074120,
        #     "backupCount": 3,
        #     "encoding": "utf-8",
        #     "delay": False
        # },
        "custom": {
            "()": "rich.logging.RichHandler"
        }
    },
    "loggers": {
        "ez_temp": {
            "handlers": ["custom"],
            "level": "INFO",
            "propagate": True
        },
    }
}