"""Given an array of values, find the 13 consecutive numbers with the largest product"""

import math

from project_euler.data import load
from project_euler.problem.problem import Problem

problem = Problem(8, "Given an array of values, find the 13 consecutive numbers with the largest product")

@problem.register()
def solution():
    array = load("p8_input")
    s = "".join(array.split())
        
    chunks = [s[i:i+13] for i in range(len(s)-13)]
    products = [math.prod([int(i) for i in chunk]) for chunk in chunks]
        
    return max(products)

if __name__ == "__main__":
    problem.main()
