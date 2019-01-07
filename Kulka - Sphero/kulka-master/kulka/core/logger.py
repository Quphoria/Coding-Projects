from functools import wraps
from itertools import chain
import inspect
import logging
import os


def debuglog(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        argspec = inspect.getargspec(func)
        argstr = dict(chain(zip(argspec.args, args), kwargs.items()))
        logging.debug('%s(%s)', func.__name__, argstr)
        try:
            retval = func(*args, **kwargs)
            logging.debug('%s -> %s)', func.__name__, retval)
            return retval
        except Exception as exc:
            logging.debug('%s => %s)', func.__name__, str(exc))
            raise

    if 'SPHERO_DEBUG' in os.environ:
        logging.basicConfig(level=logging.DEBUG)
        return wrapper
    else:
        return func
