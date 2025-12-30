import math

from mathlib.eratoshenes import primes_less_than_n_generator
from mathlib.factorization.vector import vector_factorization

# https://risencrypto.github.io/QuadraticSieve/#kraitchiks-factorization


def polynomial_factory(n):
    def f(x):
        return (x + math.ceil(math.sqrt(n)))**2 - n

    return f

def calculate_b(n):

    ln_n = math.log(n)
    l = math.exp(math.sqrt(ln_n* math.log(ln_n)))
    return math.ceil(l**(1/math.sqrt(2)))

def build_factor_base(n: int):
    b = calculate_b(n)
    return [i for i in primes_less_than_n_generator(b) if pow(n, (i-1)//2, i) == 1]


def build_relations(
        n: int, 
        factor_base: list[int], 
        num_relations: int, 
        last_seen_index: int
    ) -> dict[int, dict]:
    
    index = last_seen_index + 1
    relations = {}
    polynomial = polynomial_factory(n)

    while len(relations) < num_relations:
        
        next_value = polynomial(index)
        if vector := vector_factorization(next_value, factor_base):
            relations[index] = vector

        index += 1

    return relations

        