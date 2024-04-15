import time


def timer(func):
    """Decorator that times the execution of a function"""

    def wrapper(*args, **kwargs):
        start = time.perf_counter_ns()
        result = func(*args, **kwargs)
        end = time.perf_counter_ns()
        print(f"Execution time: {(end - start) / 1e6} ms for {func.__name__}")
        return result

    return wrapper
