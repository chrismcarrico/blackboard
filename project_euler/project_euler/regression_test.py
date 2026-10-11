import pytest

from project_euler import registry

TIMEOUT = 300

pytestmark = pytest.mark.euler


def cases():
    for problem in registry.discover().values():
        for solution in problem.solutions:
            slow = solution in problem.slow
            yield pytest.param(
                problem,
                solution,
                None if slow else TIMEOUT,
                id=f"p{problem.number}-{solution}",
                marks=[pytest.mark.slow] if slow else [],
            )


@pytest.mark.parametrize("problem, solution, timeout", cases())
def test_problems(problem, solution, timeout):

    if problem.answer is None:
        pytest.skip(f"p{problem.number} has no expected answer")

    result = problem.execute(solution, timeout=timeout)

    assert result.status == "ok", f"{result.status} after {result.seconds:.2f}s: {result.detail}"
