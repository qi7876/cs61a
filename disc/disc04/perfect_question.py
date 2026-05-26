def fit(total, n):
    """Return whether there are n positive perfect squares that sums to total.

    >>> [fit(4, 1), fit(4, 2), fit(4, 3), fit(4, 4)]  # 1*(2*2) for n=1; 4*(1*1) for n=4
    [True, False, False, True]
    >>> [fit(12, n) for n in range(3, 8)]  # 3*(2*2), 3*(1*1)+3*3, 4*(1*1)+2*(2*2)
    [True, True, False, True, False]
    >>> [fit(32, 2), fit(32, 3), fit(32, 4), fit(32, 5)] # 2*(4*4), 3*(1*1)+2*2+5*5
    [True, False, False, True]
    """
    def f(total, n, k):
        if n == 0 and total == 0:
            return True
        elif (n == 0 and total != 0) or k * k > total:
            return False
        else:
            return f(total - k ** 2, n - 1, k + 1) or f(total - k ** 2, n - 1, k) or f(total, n, k + 1)
    return f(total, n, 1)
