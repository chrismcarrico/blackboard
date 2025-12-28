import math

def d(n):
    return sum(i for i in range(1, n) if n % i == 0)

def is_amicable_pair(a,b):
    return d(a) == b and d(b) == a
    