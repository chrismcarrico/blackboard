def find_longest_cycle(seq: list) -> list:
    
    n = len(seq)//2
    
    for cycle_length in range(1, n+1):
        cycle = seq[:cycle_length]
        
        complete_cycle = len(seq) // cycle_length * len(cycle)
        for i in range(cycle_length, complete_cycle, cycle_length):
            if seq[i:i+cycle_length] != cycle:
                break
        else:
            return cycle   
        
            
    return []
                