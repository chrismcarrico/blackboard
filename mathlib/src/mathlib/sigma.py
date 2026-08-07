def sigma(n:int, z:int=0) -> int:
    """Returns the sum of the z-th powers of the divisors of n."""
    
    s = 0
    i = 1
    greatest_factor = n
    
    while i < greatest_factor:
        if n%i ==0:
            s += pow(i, z)
            s += pow(n//i, z)
            greatest_factor = n//i
        i += 1
    
    return s
    