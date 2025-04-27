def stake_martingala(base_stake, nivel):
    return base_stake * (2 ** nivel)

def stake_fibonacci(n):
    fib = [1, 1]
    for _ in range(2, n):
        fib.append(fib[-1] + fib[-2])
    return fib[n-1]
