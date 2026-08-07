from project_euler.problem.problem import Problem

problem = Problem(1, "Fake Solution")

@problem.register()
def fake_solution():
    return 42

def test_run_solution():
    assert problem.run_solution("fake_solution") == 42

def test_list_solutions():
    assert problem.list_solutions() == ["fake_solution"]


