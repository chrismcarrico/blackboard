import pytest

from project_euler import registry
from project_euler.problem.problem import Problem


def test_discovers_every_problem_file():
    files = {path.stem for path in registry.PROBLEMS_DIR.glob("p*.py")}
    assert files == set(registry.module_names())
    assert [f"p{number}" for number in registry.discover()] == registry.module_names()


@pytest.mark.parametrize("name", registry.module_names())
def test_problem_is_well_formed(name):
    number = int(name[1:])
    problem = registry.discover()[number]
    assert isinstance(problem, Problem)
    assert problem.number == number
    assert problem.solutions
    assert problem.default is None or problem.default in problem.solutions
