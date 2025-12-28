def is_perfect(n):
    return n == sum([i for i in range(1,n) if n%i == 0])

def is_deficient(n):
    return n > sum([i for i in range(1,n) if n%i == 0])

def is_abundent(n):
    return n < sum([i for i in range(1,n) if n%i == 0])