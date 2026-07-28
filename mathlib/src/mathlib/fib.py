def get_next_fib():
    a, b = 1, 1
    while True:
        yield a
        a, b = b, a + b