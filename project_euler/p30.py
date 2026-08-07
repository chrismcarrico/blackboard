from project_euler.problem.problem import Problem

problem = Problem(30)


def _sum(n):
    return sum([int(i)**5 for i in str(n)])

@problem.register()
def solution():
    
    i = 2
    limit = 9999999
    total = 0
    
    while i < limit:
        if i == _sum(i):
            total += i
            problem.debug(i)
            
        i+=1
        
    return total

if __name__ == "__main__":
    problem.main()