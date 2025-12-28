def step(n):
    if n%2: # odd
        return 3*n + 1
    return n // 2

def collatz_chain_length(n):
    
    chain_length = 1
    
    while True:  
        n = step(n)
        chain_length += 1
        
        if n == 1:
            break
        
    return chain_length