def f(x, y):
    def g(a):
        return a + y
    return g(x)