"""
a month's worth of expenditures are stored together in an object pickled to disk.
"""

import pickle





SINKS = [
    "food",
    "shared meals",
    "amazon",
    "small shopping",
    "rent",
    "internet",
    "subscriptions",
    "gas tolls",
    "health",
    "entertainment",
    "atm",
    "lyft bart"
]

class Expenditures(object):
    def __init__(self):
        self.data = {sink: [] for sink in SINKS}
        self.one_offs = []

    def add_sink(self, day, cost, sink):
        """
        add an entry under one type of sink
        """
        self.data[sink].append((day, cost))
        
    def add_one_off(self, day, cost, explanation):
        """
        for large expenses
        """
        self.one_offs.append((day, cost, explanation))
    
    def pickle(self, name):
        with open(name, "wb") as the_file:
            pickle.dump(self, the_file)


def unpickle(name):
    with open(name, "rb") as the_file:
        expenditures = pickle.load(the_file)
        return expenditures
