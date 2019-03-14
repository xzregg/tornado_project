# -*- coding: utf-8 -*-

from functools import wraps
import fcntl
import os
import logging


class PidFileError(Exception): pass


class PidFile(object):

    def __init__(self, path):
        self.path = '.%s' % path
        self.pidfile = None

    def acquire(self):
        self.__enter__()

    def release(self):
        self.__exit__()

    def __enter__(self):
        self.pidfile = open(self.path, "a+")
        try:
            fcntl.flock(self.pidfile.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except IOError:
            fpid = open(self.path, "r").read()
            raise PidFileError("Process id %s Already running , pid to " % fpid + self.path)
        self.pidfile.seek(0)
        self.pidfile.truncate()
        self.pidfile.write(str(os.getpid()))
        self.pidfile.flush()
        self.pidfile.seek(0)
        return self.pidfile

    def __exit__(self, exc_type=None, exc_value=None, exc_tb=None):
        try:
            self.pidfile.close()
        except IOError as err:
            if err.errno != 9:
                raise
        os.remove(self.path)


def SignleProcessDeco(path):
    '''保证只有单个进程在执行
    '''

    def repl(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                with PidFile(path):
                    return f(*args, **kwargs)
            except PidFileError, e:
                logging.warning(e)
                return None

        return wrapper

    return repl


if __name__ == "__main__":
    @SignleProcessDeco('my.pid')
    def main():
        import time
        print 'running'
        time.sleep(1)


    main()
    print 1
