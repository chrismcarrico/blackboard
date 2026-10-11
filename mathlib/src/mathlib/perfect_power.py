def integer_root(n: int, k: int) -> int:
    """The largest r with r^k <= n"""

    low, high = 1, 1 << (n.bit_length() // k + 1)
    while low < high:
        mid = (low + high + 1) // 2
        if mid**k <= n:
            low = mid
        else:
            high = mid - 1

    return low

def perfect_power(n: int) -> tuple[int, int] | None:
    """Returns (r, k) if n = r^k for some k > 1, with k as small as possible"""

    for k in range(2, n.bit_length()):
        root = integer_root(n, k)
        if root**k == n:
            return root, k

    return None

def perfect_power_root(n: int) -> int | None:
    """Returns r if n = r^k for some k > 1"""

    power = perfect_power(n)
    return power[0] if power is not None else None
