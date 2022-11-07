import os

PG_CONNECTION_STRING = os.getenv("PG_CONNECTION_STRING")
PG_TABLE = os.getenv("PG_TABLE", "webmon_polls")

KAFKA_HOST = os.getenv("KAFKA_HOST")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "webmon")
KAFKA_CERT_FILE = os.getenv("KAFKA_CERT_FILE", "certs/service.cert")
KAFKA_KEY_FILE = os.getenv("KAFKA_KEY_FILE", "certs/service.key")
KAFKA_CA_FILE = os.getenv("KAFKA_CA_FILE", "certs/ca.pem")

MONITOR_INTERVAL = 15
MONITOR_URLS_FILE = os.getenv("MONITOR_URLS_FILE", "monitoring.json")

LOGGING_LEVEL = {
    "DEBUG": 10,
    "INFO": 20,
    "WARNING": 30,
    "ERROR": 40
}[os.getenv("LOGGING_LEVEL", "ERROR")]

DEFAULT_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s %(module)s: [%(levelname)s] %(message)s',
        }
    },
    'handlers': {
        'console': {
            'level': LOGGING_LEVEL,
            'formatter': 'standard',
            'class': 'logging.StreamHandler'
        }
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': LOGGING_LEVEL
        }
    }
}
