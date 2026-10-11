import functools
import importlib
import pathlib
import pkgutil
import re

from project_euler import problems
from project_euler.problem.problem import Problem

PROBLEMS_DIR = pathlib.Path(problems.__file__).parent


def module_names() -> list[str]:
    names = [info.name for info in pkgutil.iter_modules(problems.__path__) if re.fullmatch(r"p\d+", info.name)]
    return sorted(names, key=lambda name: int(name[1:]))


@functools.cache
def discover() -> dict[int, Problem]:

    discovered = {}

    for name in module_names():
        module = importlib.import_module(f"{problems.__name__}.{name}")
        discovered[int(name[1:])] = module.problem

    return discovered
