def calculate_reciprocal_long(d, max_precision=2000):
    
    digits = []
    n = 10
    precision = 0
    
    while precision < max_precision:
        
        q = n//d
        digits.append(q)
        p = q*d
        r = n - p
        if r == 0:
            return digits
        
        n = r*10
        precision += 1
        
    return digits