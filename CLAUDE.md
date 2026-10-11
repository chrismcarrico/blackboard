# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

A uv workspace (Python 3.13) with two members:

- `mathlib/` — number-theory / algorithm implementations (src layout: `mathlib/src/mathlib/`).
- `project_euler/` — Project Euler solutions (`project_euler/project_euler/problems/p<N>.py`) built on a small `Problem` framework and on `mathlib`.

## Commands

```sh
uv sync                                               # install workspace + dev tools (pytest, ruff, black)

uv run pytest                                         # everything, incl. the slow Euler regression run
uv run pytest -m "not euler"                          # fast: unit tests only
uv run pytest mathlib/src/mathlib/gcd_test.py         # one test file
uv run pytest mathlib/src/mathlib/gcd_test.py::test_gcd_prime   # one test

uv run pytest -m euler -n auto                        # all Euler answers, in parallel (pytest-xdist)
uv run pytest -m euler -k p27                         # one problem's regression check
uv run pytest -m slow                                 # solutions registered slow=True (excluded by default, no timeout)

uv run python -m project_euler list                   # every problem and its solutions
uv run python -m project_euler run 27 -t              # run a solution, print timing
uv run python -m project_euler run 27 -s <name> -T 10 -v        # pick a solution, 10s timeout, debug logging
uv run python -m project_euler check                  # every default solution against its expected answer
uv run python -m project_euler check 5 --all-solutions          # every solution of one problem (add --slow for slow ones)
uv run python -m project_euler new 32 -d "description"          # scaffold problems/p32.py
uv run python -m project_euler.problems.p27 run -t   # each solution module is also runnable (run / check / list)

uv run python -m mathlib.factorization -t 360 '2**89 - 1'      # factor integers from the command line (-h for options)

uv run ruff check .                                   # not currently clean (~65 existing findings)
uv run black .
```

Pytest is configured in the root `pyproject.toml` (`[tool.pytest.ini_options]`): test files are `*_test.py`, collected from `mathlib/src` and `project_euler`. Two markers are registered: `euler` (the Euler answer regression) and `slow` (solutions too slow for a normal run). The root `conftest.py` deselects `slow` tests unless the `-m` expression mentions `slow`, so a bare `uv run pytest` includes the Euler regression run but not the slow solutions; use `-m "not euler"` for a fast pass.

## Architecture

### mathlib

- One algorithm per module, with its tests alongside as `<module>_test.py` (not in a separate `tests/` dir).
- Modules import each other by absolute path (`from mathlib.gcd import gcd`); `__init__.py` files re-export nothing, so always import from the concrete module.
- Subpackages: `factorization/` (naive, Fermat, Pollard rho, classical order-finding "Shor's", quadratic sieve), `primality/` (Miller–Rabin), `linalg/` (GF(2) Gaussian elimination, transpose).
- `factorization/factor.py` is the entry point: `factor(n)` returns `{prime: exponent}`. It strips small primes, then recursively splits each composite using `plan(n)` — Pollard rho for small cofactors; otherwise a few Fermat steps, a budgeted Pollard rho, then the quadratic sieve. `method=` forces one algorithm, and the thresholds are keyword arguments. `factorization/cli.py` (run via `__main__.py`) exposes all of it, generating one flag per keyword argument of `factor`. Every splitting algorithm (`fermat_factorization`, `pollard_rho`, `quadratic_sieve`, `shors.find_factor`, `trial_division`) shares one shape: take `n`, return a non-trivial factor or `None`. `shors` and `naive_factorization` instead return the list of distinct primes.
- The quadratic sieve (`factorization/qs.py`) is the most cross-cutting piece. `quadratic_sieve` is the real one (log sieve over `[-m, m]`, large-prime variation, multiple polynomials); `quadratic_sieve_v1` finds relations by trial division. Both compose `eratoshenes` (factor base primes), `quadratic_residue.legendre_symbol`, `factorization/vector.py` (exponent vectors over the factor base) and `linalg/gf2_gaussian_elimination.find_dependencies`; the sieve also uses `tonelli_shanks` and `primality/miller_rabin`.
- `mathlib.data.get_known_primes()` loads `data/known_primes.txt` via `importlib.resources` — used as a test fixture/reference list.
- Note the module is spelled `eratoshenes` (sic); match the existing name when importing.

### project_euler

- `project_euler/project_euler/problem/problem.py` defines `Problem`, which is a solution registry plus argparse CLI. Every `problems/p<N>.py` follows the same shape:

  ```python
  from project_euler.problem.problem import Problem

  problem = Problem(N, "description")

  @problem.register()            # optional: register("name", default=True, slow=True)
  def solution():
      return answer              # solutions take no args and return the answer

  problem.register_answer(12345) # the expected answer; omit until solved

  if __name__ == "__main__":
      raise SystemExit(problem.main())
  ```

  A problem may register several named solutions; the one marked `default=True` (else the first registered) is what `run` uses by default. `slow=True` marks a solution too slow for a normal run. The module-level name must be `problem` — `registry.discover()` imports every `problems/p<N>.py` and reads `.problem`.
- `Problem.run_solution(name, timeout)` returns the raw answer; `Problem.execute(name, timeout)` wraps it and returns a `Result` whose `status` is `ok`, `wrong`, `unchecked` (no expected answer), `timeout` or `error`. The CLIs and the regression test are built on `execute`.
- `project_euler/project_euler/cli.py` (run via `__main__.py`) is the cross-problem runner: `list`, `run N`, `check [N ...]`, `new N`. `run` and `check` exit non-zero on a wrong answer, timeout or exception.
- Expected answers live in the problem file, registered with `problem.register_answer(...)` at the bottom (just above the `__main__` guard), not in a separate data file. `regression_test.py` is parametrized over every registered solution of every problem, with a per-solution timeout; problems with no `answer` are skipped. When adding a solved problem, register its answer.
- Input files live in `project_euler/project_euler/data/p<N>_input.txt` and are read with `from project_euler.data import load; load("p<N>_input")`.
- Timeouts (`-T`) are implemented with `SIGALRM`, so they are Unix-only and main-thread-only.
