from project_euler.problem.problem import Problem
from project_euler.data import load

problem = Problem(22, "What is the total of all the name scores in the file.")


alpha = "abcdefghijklmnopqrstuvwxyz"

@problem.register()
def solution():

    total = 0

    data = load("p22_input")
    data = data.replace('"', '')
    data = data.split(",")
    data = sorted(data)

    for i, name in enumerate(data):
        total += sum(alpha.index(j.lower()) + 1 for j in name)*(i+1)

    return total

if __name__ == "__main__":
    problem.main()