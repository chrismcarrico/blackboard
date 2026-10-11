from project_euler.problem.problem import Problem

problem = Problem(31)


p1 = (1, 200)
p2 = (2, 100)
p5 = (5, 40)
p10 = (10, 20)
p20 = (20, 10)
p50 = (50, 4)
e1 = (100, 2)
e2 = (200, 1)

coins = [
    e2, e1, p50, p20, p10, p5, p2, p1
]

def _solution(total: int, coin: tuple[int, int], remaining_coins: list) -> int:
    
    v, n = coin
    solutions = 0
    
    if remaining_coins:
        for i in range(n+1):
            if total + v*i == 200:
                solutions += 1
            elif total + v*i < 200:
                solutions += _solution(total+v*i, remaining_coins[0], remaining_coins[1:])
            else:
                break
    else:
        solutions +=  int((200 - total) % v == 0 and ((200 - total) // v) <= n)
        
    return solutions
    
@problem.register()
def solution():
    return _solution(0, coins[0], coins[1:])

problem.register_answer(73682)

if __name__ == "__main__":
    raise SystemExit(problem.main())
