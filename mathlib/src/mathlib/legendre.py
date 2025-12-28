def legendre_symbol(a: int, p: int):
    
    residue = pow(a, (p-1)//2, p)
    
    return residue - p if residue > 1 else residue
