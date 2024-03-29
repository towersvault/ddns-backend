from functools import wraps

import os


def cleanup(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        try:
            os.remove('test-ddns.sqlite')
        except FileNotFoundError:
            pass

        return function(*args, **kwargs)
    return wrapper


def truthy(value):
    return bool(value)


def falsy(value):
    return not bool(value)
