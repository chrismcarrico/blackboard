def is_pandigital(n: int, p=None) -> bool:
    
    l = [int(i) for i in str(n)]
    m = max(l) if p is None else p
    
    if len(l) != m:
        return False
    
    for i in range(1, m+1):
        if i not in l:
            return False
        
    return True
        
        