from mathlib.quadratic_residue import legendre_symbol

def _seperate_powers_of_2(n):
        
    s = 0
    n_0 = n
    while n % 2 == 0:
        n //= 2
        s += 1
    
    q = n_0//pow(2, s)
    return s, q

def _find_first_z_st_non_qr_mod_p(p):

    for z in range(2, p):
        if legendre_symbol(z, p) == -1:
            return z
        
    raise RuntimeError

def _least_i_st_t2_i_is_1(t:int, p:int, m:int) -> int:

    t2 = pow(t, 2, p)
    for i in range(1, m):
        if t2 % p == 1:
            return i
        t2 = pow(t2, 2, p)

    raise RuntimeError   

def tonelli_shanks(n: int, p: int) -> int:

    assert n > 0 and p > 0
    assert legendre_symbol(n, p) == 1, "not a square (mod p)"
    
    s, q = _seperate_powers_of_2(p-1)

    if s == 1:
        return pow(n, (p + 1) // 4, p)
    
    z = _find_first_z_st_non_qr_mod_p(p)

    c = pow(z, q, p)
    r = pow(n, (q + 1) // 2, p)
    t = pow(n, q, p)
    m = s

    while True:

        if t % p == 0:
            return 0

        elif t % p == 1:
            return r
        
        else:
        
            i = _least_i_st_t2_i_is_1(t, p, m)

            b = pow(c, pow(2, m - i - 1), p)
            r = (r * b) % p
            c = (b * b) % p
            t = (t * c) % p
            m = i

        