def nth_triangular_number(n):
    return sum(range(n+1))

def nth_triangular_number_formula(n):
    return (n**2 + n) // 2
 
def triangular_number_generator():
    
    a, b = 1, 1
    
    while True:
        yield a,b 
        a += 1
        b += a