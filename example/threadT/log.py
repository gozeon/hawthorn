# -*- coding: utf-8 -*-
import threading
import logging
from datetime import datetime


def get_logger():
    logger = logging.getLogger('threading_example')
    logger.setLevel(logging.DEBUG)
    # fh = logging.FileHandler('threading.log')
    fh = logging.FileHandler('{:%Y-%m-%d}.log'.format(datetime.now()))
    fmt = '[%(levelname)s] %(asctime)s - %(threadName)s - %(message)s'
    formatter = logging.Formatter(fmt)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger


def doubler(number, logger):
    """
    可以被线程使用的一个函数
    """
    logger.debug('doubler function executing')
    result = number * 2
    logger.debug('doubler function ended with: {}'.format(result))


if __name__ == '__main__':
    logger = get_logger()
    thread_names = ['Mike', 'George', 'Wanda', 'Dingbat', 'Nina']
    for i in range(5):
        my_thread = threading.Thread(
            target=doubler,
            name=thread_names[i],
            args=(i, logger))
        my_thread.start()
