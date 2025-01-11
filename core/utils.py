# Utility codes
#
# Created by Yi at 28/12/2024.
#

import sys

from datetime import datetime
from pathlib import Path

from loguru import logger


# logging config
DEFAULT_LOG_DIR = Path('logs')
DEFAULT_LOG_DIR.mkdir(parents=True, exist_ok=True)


def get_timestamp():
    """Generalised timestamp"""
    return datetime.now().strftime('%m%d%H%M%S')


def init_logger(name, out: Path or None = None):
    # remove the initial handler
    logger.remove()
    if out is None:
        out = (DEFAULT_LOG_DIR / name).with_suffix('.log')

    config = {
        "handlers": [
            {"sink": sys.stdout, "format": "{time} - {message}"},
            {"sink": str(out), "serialize": True},
        ],
        "extra": {"user": "Mario"}
    }
    logger.configure(**config)
    return logger
