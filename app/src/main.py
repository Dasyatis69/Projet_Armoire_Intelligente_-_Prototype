import core_classes as core
from time import time


def measure_runtime(func):
    def wrapper():
        t = time()
        func()
        t = time() - t
        print(f'{func.__name__} took {t} seconds to run')
    return wrapper


@measure_runtime
def main():
    pole = core.Pole(core.Armoire(core.Drawer()))
    return 0


if __name__ == "__main__":
    main()
