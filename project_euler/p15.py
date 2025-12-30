"""All paths through a lattice"""

import math
from project_euler.solution_set.solution_set import SolutionSet

solution_set = SolutionSet(15, "All paths through a lattice")

@solution_set.register()
def solution_1():
    import networkx as nx

    rows, cols = 20, 20
    nrows, ncols = rows+1,cols+1
    nnodes=(nrows)*(ncols)
    
    graph = nx.DiGraph()
    graph.add_nodes_from(range(nnodes))
    
    def good_node(n):
        # 0 okay
        return -1 < n[0] < nrows and -1 <  n[1] < ncols
    
    def add_edge(u, v):
        if good_node(u) and good_node(v):
            graph.add_edge(u[0]*ncols+u[1], v[0]*ncols+v[1])
            
    for r in range(nrows):
        for c in range(ncols):
            add_edge((r,c), (r+1, c))
            add_edge((r,c), (r, c+1))
    
    
    return len([i for i in nx.all_simple_paths(graph, 0, nnodes-1)])


@solution_set.register(default=True)
def solution():
    return math.comb(2*20, 20)

if __name__ == "__main__":
    solution_set.main()
