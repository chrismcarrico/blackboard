import copy
import itertools
import typing

from mathlib.linalg.transpose import transpose

# https://www.cs.umd.edu/~gasarch/TOPICS/factoring/fastgauss.pdf

Binary = typing.Literal[1, 0]
BinaryMatrix = list[list[Binary]]

def gf2_gaussian_elimination(A:BinaryMatrix) -> tuple[BinaryMatrix, list[bool]]:

    A = copy.deepcopy(A)
    n_rows = len(A)
    n_cols = len(A[0])
    
    marked = [False]*n_rows

    for j in range(n_cols):
        for i in range(n_rows):
            if A[i][j] == 1:
                marked[j] = True
                for k in itertools.chain(range(j), range(j+1, n_cols)):
                    if A[i][k] == 1: 
                        for r in range(n_rows):
                            A[r][k] = A[r][k] ^ A[r][j]
                
                break

    return A, marked

    