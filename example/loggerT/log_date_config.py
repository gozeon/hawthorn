import logging.config
from datetime import datetime
import os

BASE_ROOT = os.path.dirname(os.path.realpath(__file__))

logging.config.fileConfig(os.path.join(BASE_ROOT, 'aaa.conf'))
logger = logging.getLogger('MainLogger')

fh = logging.FileHandler('{:%Y-%m-%d}.log'.format(datetime.now()))
formatter = logging.Formatter(
    '%(asctime)s | %(levelname)-8s | %(lineno)04d | %(message)s')
fh.setFormatter(formatter)

logger.addHandler(fh)
logger.debug("TEST")
