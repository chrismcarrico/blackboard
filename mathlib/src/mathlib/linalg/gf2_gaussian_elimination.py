import typing

# https://www.cs.umd.edu/~gasarch/TOPICS/factoring/fastgauss.pdf

Binary = typing.Literal[1, 0]
BinaryMatrix = list[list[Binary]]

def _to_columns(A: typing.Sequence[typing.Sequence[int]]) -> list[int]:
    """Packs each column of A into an int, bit i of column j is A[i][j]"""

    columns = [0]*len(A[0])
    for i, row in enumerate(A):
        for j, value in enumerate(row):
            if value == 1:
                columns[j] |= 1 << i

    return columns

def _eliminate(columns: list[int], n_rows: int) -> tuple[list[int], list[bool], dict[int, int]]:

    columns = list(columns)
    marked = [False]*n_rows
    pivot_row_for_col = {}

    for j, column in enumerate(columns):

        if column == 0:
            continue

        # first row with a 1 in column j
        i = (column & -column).bit_length() - 1
        marked[i] = True
        pivot_row_for_col[j] = i

        # adding column j to column k is a single xor
        for k in range(len(columns)):
            if k != j and (columns[k] >> i) & 1:
                columns[k] ^= column

    return columns, marked, pivot_row_for_col

def gf2_gaussian_elimination(A:BinaryMatrix) -> tuple[BinaryMatrix, list[bool]]:

    n_rows = len(A)

    columns, marked, _ = _eliminate(_to_columns(A), n_rows)

    return [[1 if (column >> i) & 1 else 0 for column in columns] for i in range(n_rows)], marked

def find_dependencies(A: typing.Sequence[typing.Sequence[int]]) -> list[list[int]]:
    """Returns sets of row indices of A whose rows sum to zero over GF(2)"""

    n_rows = len(A)

    columns, marked, pivot_row_for_col = _eliminate(_to_columns(A), n_rows)

    # after elimination each marked row has a single 1, in its pivot column
    dependencies = []
    for i in range(n_rows):
        if not marked[i]:
            dependencies.append([i] + [pivot_row_for_col[j] for j, column in enumerate(columns) if (column >> i) & 1])

    return dependencies
