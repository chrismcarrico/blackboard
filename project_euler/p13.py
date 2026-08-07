"""Work out the first ten digits of the sum of the following one-hundred 50-digit numbers."""

from project_euler.data import load
from project_euler.problem.problem import Problem

problem = Problem(13, "Work out the first ten digits of the sum of the following one-hundred 50-digit numbers.")

@problem.register()
def solution():
    
    numbers = [int(i) for i in load("p13_input").splitlines()]
    s = sum(numbers)
    return int(str(s)[:10])