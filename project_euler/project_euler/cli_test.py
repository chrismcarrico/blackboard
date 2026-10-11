import runpy
import time

import pytest

from project_euler import cli, registry
from project_euler.problem.problem import Problem


def fake_problems() -> dict[int, Problem]:

    right = Problem(1, "Always right")
    right.register()(lambda: 1)
    right.register_answer(1)

    mixed = Problem(2, "Right by default")
    mixed.register("bad")(lambda: 3)
    mixed.register("good", default=True)(lambda: 2)
    mixed.register("sleepy", slow=True)(lambda: time.sleep(5))
    mixed.register_answer(2)

    unsolved = Problem(3)
    unsolved.register()(lambda: None)

    return {1: right, 2: mixed, 3: unsolved}


@pytest.fixture(autouse=True)
def fake_registry(monkeypatch, tmp_path):
    problems = fake_problems()
    monkeypatch.setattr(registry, "discover", lambda: problems)
    monkeypatch.setattr(registry, "PROBLEMS_DIR", tmp_path)


@pytest.mark.parametrize("argv, code", [
    (["list"], 0),
    (["run", "1", "-t"], 0),
    (["run", "2"], 0),
    (["run", "2", "-s", "bad"], 1),
    (["run", "2", "-s", "sleepy", "-T", "0.05"], 1),
    (["run", "3"], 0),
    (["check"], 0),
    (["check", "1", "3"], 0),
    (["check", "--all-solutions"], 1),
    (["check", "1", "--all-solutions"], 0),
    (["check", "2", "--all-solutions", "--slow", "-T", "0.05"], 1),
])
def test_exit_code(argv, code):
    assert cli.main(argv) == code


@pytest.mark.parametrize("argv", [
    ["run", "99"],
    ["check", "1", "99"],
    ["run", "2", "-s", "missing"],
])
def test_rejects_unknown_problem_or_solution(argv):
    with pytest.raises(SystemExit):
        cli.main(argv)


def test_check_reports_each_solution(caplog):
    with caplog.at_level("INFO"):
        cli.main(["check", "2", "--all-solutions"])
    assert "bad" in caplog.text and "got 3, expected 2" in caplog.text
    assert "sleepy" not in caplog.text
    assert "1 ok, 1 failed, 0 unchecked" in caplog.text


def test_new(tmp_path):
    assert cli.main(["new", "40", "-d", 'Say "hi"']) == 0

    namespace = runpy.run_path(str(tmp_path / "p40.py"))

    created = namespace["problem"]
    assert created.number == 40
    assert created.description == 'Say "hi"'
    assert created.solutions == ["solution"]


def test_new_refuses_to_overwrite(tmp_path):
    (tmp_path / "p40.py").write_text("keep me")
    assert cli.main(["new", "40"]) == 1
    assert (tmp_path / "p40.py").read_text() == "keep me"
