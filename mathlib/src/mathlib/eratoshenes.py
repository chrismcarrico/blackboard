import typing

def eratoshenes(n: int) -> list[int]:
    raise NotImplementedError

def eratosthenes_generator(n: int) -> typing.Generator[int]:
    
    integers = [1]*(n)
    integers[0] = 0
    integers[1] = 0
    
    for i, is_prime in enumerate(integers):
        if is_prime:
            yield i
            for k in range(i*i, n, i):
                integers[k] = 0
                
