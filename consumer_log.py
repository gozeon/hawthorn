import os
import logging
from datetime import datetime

ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
LOG_PATH = os.path.join(ROOT_DIR, 'log')
if not os.path.exists(LOG_PATH):
    os.makedirs(LOG_PATH)
dynamic_log = '{:%Y-%m-%d}.log'.format(datetime.now())

# create logger
logger = logging.getLogger('queue_log')
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.FileHandler(os.path.join(LOG_PATH, dynamic_log))
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)


# 'application' code
# logger.debug('debug message')
# logger.info('info message')
# logger.warning('warn message')
# logger.error('error message')
# logger.critical('critical message')

def callback(ch, method, properties, body):
    # print(ch)
    # print(method.exchange)
    # print(properties)
    logger.info(datetime.now().timestamp())
    logger.info('ch: {}'.format(ch))
    logger.info('method: {}'.format(method))
    logger.info('properties: {}'.format(properties))
    logger.info('body: {}'.format(body))
    # print(" [x] %r" % body)
    # print(method.delivery_tag)
    # 消息确认，否则重启文件，会把原先的记录重新开启，no_ack 也是这样
    ch.basic_ack(delivery_tag=method.delivery_tag)
