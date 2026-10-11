# project_euler

Project Euler solutions, one module per problem in `project_euler/problems/p<N>.py`, built on the small `Problem` framework in `project_euler/problem/problem.py`.

## Running

```sh
uv run python -m project_euler list                       # every problem and its solutions
uv run python -m project_euler run 27 -t                  # run a problem's default solution, with timing
uv run python -m project_euler run 5 -s naive -T 10       # pick a solution, 10s timeout
uv run python -m project_euler check                      # every default solution against its expected answer
uv run python -m project_euler check 5 15 --all-solutions # every solution of the given problems
uv run python -m project_euler new 32 -d "Pandigital products"   # scaffold problems/p32.py
```

`run` and `check` exit non-zero on a wrong answer, a timeout or an exception. Each solution module is also runnable on its own, with `run`, `check` and `list` subcommands:

```sh
uv run python -m project_euler.problems.p27 run -t
```

## Writing a solution

```python
from project_euler.problem.problem import Problem

problem = Problem(N, "description")

@problem.register()                # optional: register("name", default=True, slow=True)
def solution():
    return answer                  # solutions take no args and return the answer

problem.register_answer(12345)     # the expected answer; omit until the problem is solved

if __name__ == "__main__":
    raise SystemExit(problem.main())
```

- The default solution is the one registered with `default=True`, else the first registered.
- `slow=True` marks a solution that is too slow for a normal run. `check` skips it unless given `--slow`, and its regression test only runs under `pytest -m slow`.
- Input files live in `project_euler/data/p<N>_input.txt` and are read with `project_euler.data.load("p<N>_input")`.

## Testing

```sh
uv run pytest -m "not euler"          # fast: framework, registry and CLI tests
uv run pytest -m euler -n auto        # every solution against its expected answer, in parallel
uv run pytest -m euler -k p27         # one problem
uv run pytest -m slow                 # the solutions registered as slow, with no timeout
```

The regression test (`project_euler/regression_test.py`) covers every registered solution of every problem, with a per-solution timeout. Problems with no registered answer are reported as skipped.
