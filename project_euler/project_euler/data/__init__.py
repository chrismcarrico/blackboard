import os

def load(string, ext="txt"):
    with open(os.path.join(os.path.dirname(__file__), f"{string}.{ext}"), "r") as r:
        return r.read()
