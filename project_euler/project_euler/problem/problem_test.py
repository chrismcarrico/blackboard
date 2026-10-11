import time

import pytest

from project_euler.problem.problem import Problem, SolutionTimeoutError

problem = Problem(1, "Fake Solution")

@problem.register()
def fake_solution():
    return 42

@problem.register("wrong")
def wrong_solution():
    return 41

@problem.register("sleepy", slow=True)
def sleepy_solution():
    time.sleep(5)
    return 42

@problem.register("broken")
def broken_solution():
    raise RuntimeError("boom")

problem.register_answer(42)


def test_run_solution():
    assert problem.run_solution("fake_solution") == 42

def test_solutions():
    assert problem.solutions == ["fake_solution", "wrong", "sleepy", "broken"]

def test_slow():
    assert problem.slow == {"sleepy"}

def test_default_falls_back_to_first_registered():
    assert problem.default is None
    assert problem.resolve_solution_name() == "fake_solution"

def test_explicit_default():
    p = Problem(2)
    p.register("first")(lambda: 1)
    p.register("second", default=True)(lambda: 2)
    assert p.resolve_solution_name() == "second"
    assert p.run_solution() == 2

def test_register_answer():
    p = Problem(2)
    assert p.answer is None
    p.register_answer(7)
    assert p.answer == 7
    with pytest.raises(ValueError):
        p.register_answer(8)

def test_duplicate_name():
    p = Problem(2)
    p.register("name")(lambda: 1)
    with pytest.raises(ValueError):
        p.register("name")(lambda: 2)

def test_no_solutions():
    with pytest.raises(LookupError):
        Problem(2).run_solution()

def test_unknown_name():
    with pytest.raises(LookupError, match="fake_solution"):
        problem.run_solution("missing")

def test_run_solution_timeout():
    with pytest.raises(SolutionTimeoutError):
        problem.run_solution("sleepy", timeout=0.05)

def test_execute_ok():
    result = problem.execute("fake_solution")
    assert (result.problem, result.solution, result.answer, result.expected) == (1, "fake_solution", 42, 42)
    assert result.status == "ok"
    assert result.ok

def test_execute_wrong():
    result = problem.execute("wrong")
    assert result.status == "wrong"
    assert not result.ok
    assert result.detail == "got 41, expected 42"

def test_execute_unchecked():
    p = Problem(2)
    p.register()(lambda: 7)
    result = p.execute()
    assert result.status == "unchecked"
    assert result.ok

def test_execute_timeout():
    result = problem.execute("sleepy", timeout=0.05)
    assert result.status == "timeout"
    assert not result.ok
    assert result.seconds < 1

def test_execute_error():
    result = problem.execute("broken")
    assert result.status == "error"
    assert not result.ok
    assert result.detail == "RuntimeError: boom"

@pytest.mark.parametrize("argv, code", [
    (["run"], 0),
    (["run", "-s", "fake_solution", "-t"], 0),
    (["run", "-s", "wrong"], 1),
    (["run", "-s", "sleepy", "-T", "0.05"], 1),
    (["run", "-s", "broken"], 1),
    (["check"], 1),
    (["list"], 0),
])
def test_main_exit_code(argv, code):
    assert problem.main(argv) == code

def test_main_check_passes_when_every_solution_is_right():
    p = Problem(2)
    p.register("a")(lambda: 3)
    p.register("b", slow=True)(lambda: 4)
    p.register_answer(3)
    assert p.main(["check"]) == 0
    assert p.main(["check", "--slow"]) == 1

def test_main_rejects_unknown_solution():
    with pytest.raises(SystemExit):
        problem.main(["run", "-s", "missing"])
