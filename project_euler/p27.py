from project_euler.problem.problem import Problem

from mathlib.factorization.naive import naive_factorization
from mathlib.primality.miller_rabin import miller_rabin

problem = Problem(27, "Find the product of the coefficients, a and b, for the quadratic expression that produces the maximum number of primes for consecutive values of n, starting with n = 0.")



@problem.register()
def solution():
    
    N = 1000
    best_n = 0
    best_ab = 0
    
    for a in range(-N, N):
        for b in range(-N, N+1):
            n = 0
            while True:
                y = n**2 + a*n + b
                if y <= 0 or not miller_rabin(y, 20):
                    break
                elif len(naive_factorization(y)) > 1:
                    break
                else:
                    n += 1
                
            if n > best_n:
                best_ab = a*b
                best_n = n
                
    return best_ab
            
                    
if __name__ == "__main__":
    problem.main()