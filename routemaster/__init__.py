import logging

from . import db
from . import web

# Configure a better log formatter and use it globally
formatter = logging.Formatter(fmt='{levelname}:{name}:{message}', style='{')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(handler)
logger.setLevel(logging.INFO)
