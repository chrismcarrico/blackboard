def fibonacci_sequence_generator():
    
    a, b = 1, 2
    while True:
        yield a
        a, b = b, a + b
