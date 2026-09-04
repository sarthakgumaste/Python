import timeit

def fib_recursive(n):
    """Naive recursive Fibonacci.
    Time complexity: O(2^n) \u2014 exponential. Only usable for small n."""
    if n <= 1:
        return n
    return fib_recursive(n - 1) + fib_recursive(n - 2)

def fib_memo(n, memo=None):
    """Recursive Fibonacci with a cache.
    Time complexity: O(n)."""
    if memo is None:
        memo = {}
    if n <= 1:
        return n
    if n in memo:
        return memo[n]
    memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]

def fib_dp(n):
    """Bottom-up iterative Fibonacci.
    Time complexity : O(n)
    Space complexity: O(1) \u2014 only two numbers are ever stored."""
    if n <= 1:
        return n
    a, b = 0, 1          # a = F(0), b = F(1)
    for _ in range(2, n + 1):
        a, b = b, a + b  # slide the window forward by one step
    return b

def fib_fast_doubling(n):
    """Computes F(n) in O(log n) time using the fast-doubling method.
    Returns F(n) directly (an internal helper also tracks F(n+1))."""

    def _fib_pair(k):
        """Returns (F(k), F(k+1))."""
        if k == 0:
            return (0, 1)
        a, b = _fib_pair(k // 2)
        c = a * (2 * b - a)      # F(2*(k//2))
        d = a * a + b * b        # F(2*(k//2) + 1)
        if k % 2 == 0:
            return (c, d)
        else:
            return (d, c + d)

    return _fib_pair(n)[0]

if __name__ == "__main__":

    n = 10
    print(f"Computing Fibonacci({n}) with four different approaches:\n")
    print(f"[1] Naive recursion    : {fib_recursive(n)}")
    print(f"[2] Memoized recursion : {fib_memo(n)}")
    print(f"[3] Iterative DP       : {fib_dp(n)}")
    print(f"[4] Fast doubling      : {fib_fast_doubling(n)}")

    print("\nFirst 15 Fibonacci numbers (using the iterative DP version):")
    print([fib_dp(i) for i in range(15)])

    n_big = 28
    t_naive = timeit.timeit(lambda: fib_recursive(n_big), number=1)
    t_dp = timeit.timeit(lambda: fib_dp(n_big), number=1)
    print(f"\nTiming fib({n_big}):")
    print(f"  naive recursion : {t_naive:.5f} sec")
    print(f"  iterative DP    : {t_dp:.8f} sec  (thousands of times faster)")

    n_huge = 100
    print(f"\nFibonacci({n_huge}) via iterative DP  : {fib_dp(n_huge)}")
    print(f"Fibonacci({n_huge}) via fast doubling : {fib_fast_doubling(n_huge)}")