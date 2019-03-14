# -*- coding: utf-8 -*-
# @Time    : 2019-03-14 17:59
# @Author  : xzr
# @Contact : xzregg@gmail.com
# @Desc    : 日志类


import logging
import os
import sys
import time

from utils import mkdirs
from utils.multiprocesslogging import MultiProcessTimedRotatingFileHandler

LOGS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
mkdirs(LOGS_DIR)


class Logger(object):
    '''#使用django 的logging
    @name 记录的名字 需在setting里设置
    '''
    __loggers = {}

    def __new__(cls, name, type_name, when='M', interval=1440, backupCount=10):
        logger_name = '%s_%s' % (name, type_name)
        logger = cls.__loggers.get(logger_name, None)
        if not logger:
            logger = logging.getLogger(name)
            the_game_log_dir = os.path.join(LOGS_DIR, name)
            mkdirs(the_game_log_dir)
            the_game_log_file_name = os.path.join(
                    the_game_log_dir, '%s.log' % type_name)
            fileTimeHandler = MultiProcessTimedRotatingFileHandler(
                    the_game_log_file_name, when, interval, backupCount)
            formatter = logging.Formatter(
                    '%(asctime)s pid:%(process)d %(name)s:%(lineno)d %(levelname)s %(message)s',
                    datefmt='[%Y-%m-%d %H:%M:%S %z]')
            fileTimeHandler.setFormatter(formatter)
            logger.addHandler(fileTimeHandler)
            cls.__loggers[logger_name] = logger
        return logger


if __name__ == '__main__':
    import multiprocessing


    def test(num):
        time.sleep(1)
        log = Logger('cache', 'login', 'S', 2, 300)
        # log.info('info')
        # log.critical('critissscal')
        log.warn('wassrn')
        # log.error('errssor')


    pool = multiprocessing.Pool(processes=5)
    for i in range(20):
        pool.apply_async(func=test, args=(i,))
    pool.close()
    pool.join()
    print '完毕'
