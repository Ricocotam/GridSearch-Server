import itertools
import threading


class LockedIterator(object):
    """Thread Safe iterator."""
    def __init__(self, it):
        self.lock = threading.Lock()
        self.it = it.__iter__()

    def __iter__(self):
        return self

    def __next__(self):
        with self.lock:
            return next(self.it)
        

def kwargs_product(**kwargs):
    """Cartesian Product keeping the name of variables."""
    for combination in itertools.product(*kwargs.values()):
        yield dict(zip(kwargs.keys(), combination))


if __name__ == "__main__":
    pass
