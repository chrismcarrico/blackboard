import itertools

from project_euler.problem.problem import Problem

problem = Problem(32)



def _get_int(l):
    return int("".join(l))


@problem.register("factors", default=True)
def solution():
    # 9 digits in total forces 1-digit x 4-digit or 2-digit x 3-digit,
    # each with a 4-digit product.
    products = set()
    for a in range(1, 100):
        lo, hi = (1000, 10000) if a < 10 else (100, 1000)
        for b in range(lo, min(hi, 10000 // a + 1)):
            c = a * b
            if "".join(sorted(f"{a}{b}{c}")) == "123456789":
                problem.debug((a, b, c))
                products.add(c)

    return sum(products)


@problem.register("permutations")
def permutations():
    numbers = [str(i) for i in range(1, 10)]
    products = set()
    for perm in itertools.permutations(numbers):
        c = _get_int(perm[5:])
        for split in (1, 2):
            a, b = _get_int(perm[:split]), _get_int(perm[split:5])
            if a * b == c:
                problem.debug((a, b, c))
                products.add(c)

    return sum(products)


problem.register_answer(45228)

if __name__ == "__main__":
    raise SystemExit(problem.main())
