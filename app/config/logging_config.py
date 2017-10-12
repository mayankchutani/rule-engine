config = {
    "version": 1,
    "handlers": {
        "fh_info": {
            "class": "logging.StreamHandler",
            "formatter": "csFormatter",
            "stream": "ext://sys.stdout"
        },
        "fh_debug": {
            "class": "logging.StreamHandler",
            "formatter": "csFormatter",
            "stream": "ext://sys.stderr"
        },
        "fh_error": {
            "class": "logging.StreamHandler",
            "formatter": "csFormatter",
            "stream": "ext://sys.stderr"
        }
    },
    "loggers": {
        "info_logger": {
            "handlers": ["fh_info"],
            "level": "INFO"
        },
        "debug_logger": {
            "handlers": ["fh_debug"],
            "level": "DEBUG"
        },
        "error_logger": {
            "handlers": ["fh_error"],
            "level": "ERROR"
        }
    },
    "formatters": {
        "csFormatter": {
            "format": "%(filename)s|%(funcName)s %(asctime)s-%(levelname)s- %(message)s"
        }
    },
    "root": {
        "level": "INFO",
        "handlers": []
    }
}
