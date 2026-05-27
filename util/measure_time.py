import time
from functools import wraps

def measure_time(func):
    @wraps(func)
    def wraper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()

        run_time = end - start
        print(f"{func.__name__} zajela {run_time} sekund")
        return result

    return wraper