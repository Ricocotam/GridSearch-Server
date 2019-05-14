import itertools
import threading

class LockedIterator(object):
    def __init__(self, it):
        self.lock = threading.Lock()
        self.it = it.__iter__()

    def __iter__(self):
        return self

    def __next__(self):
        with self.lock:
            return next(self.it)
        

def kwargs_product(**kwargs):
    for combination in itertools.product(kwargs.values()):
        return dict(zip(kwargs.keys(), combination))