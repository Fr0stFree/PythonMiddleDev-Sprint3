import logging
import logging.config


def setup_logging(log_level: str):
	logging.config.dictConfig(
		{
			"version": 1,
			"disable_existing_loggers": False,
			"formatters": {
				"standard": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"},
			},
			"handlers": {
				"default": {
					"level": "DEBUG",
					"formatter": "standard",
					"class": "logging.StreamHandler",
					"stream": "ext://sys.stdout",
				},
			},
			"loggers": {
				"etl": {
					"handlers": ["default"],
					"level": log_level,
					"propagate": True,
				},
			},
		}
	)
	logging.captureWarnings(True)
