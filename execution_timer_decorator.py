#!/usr/bin/env python3

import time
import functools


def time_func(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()

        print(f"{func.__name__} took {end-start:.2f}s to complete.")
        return result

    return wrapper
