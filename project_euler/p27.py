from project_euler.solution_set.solution_set import SolutionSet

from mathlib.primality.miller_rabin import miller_rabin


solution_set = SolutionSet(27, "Find the product of the coefficients, a and b, for the quadratic expression that produces the maximum number of primes for consecutive values of n, starting with n = 0.")


N = 1000

@solution_set.register()
def solution():
    
    best = 0
    ab = 0
    
    for a in range(-N, N):
        for b in range(-N, N+1):
            n = 0
            while True:
                y = (n**2) - (a*n) + b

                if y <= 0 or not miller_rabin(y, 100):
                    break
                else:
                    n += 1
                    
            if n > best:
                best = n
                ab = a*b
                
    return ab
                    
if __name__ == "__main__":
    solution_set.main()