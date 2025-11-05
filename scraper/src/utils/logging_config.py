# logging_config.py
import logging.config

from pathlib import Path

# Absoluter Pfad zur Logdatei, zwei Verzeichnisse über dem aktuellen File
log_path = Path(__file__).resolve().parents[3] / "logs/scraper.log"

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': str(log_path),
            'formatter': 'standard',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
}

# Config ausführen
logging.config.dictConfig(LOGGING_CONFIG)
