from solution_set.solution_set import SolutionSet

solution_set = SolutionSet(1, "Fake Solution")

@solution_set.register()    
def fake_solution():
    return 42

def test_run_solution():
    assert solution_set.run_solution("fake_solution") == 42

def test_list_solutions():
    assert solution_set.list_solutions() == ["fake_solution"]

    