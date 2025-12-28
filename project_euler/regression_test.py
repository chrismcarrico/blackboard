import pytest
import importlib
import yaml
import os

REGRESSION_TEST_CASES_YAML = os.path.join(os.path.dirname(__file__), "regression_test.yaml")

with open(REGRESSION_TEST_CASES_YAML, "r") as f:
    REGRESSION_TEST_CASES = yaml.safe_load(f)

@pytest.mark.parametrize("problem, answer", REGRESSION_TEST_CASES.items())
def test_problems(problem, answer):

    problem_module = importlib.import_module(f"{problem}")
    solution_set = problem_module.solution_set
    
    assert solution_set.run_solution(solution_set.default) == answer
