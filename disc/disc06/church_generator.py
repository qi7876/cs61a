from collections.abc import Callable
from typing import Any


def church_generator(f: Callable[..., Any]):
    """Takes in a function f and yields functions which apply f
    to their argument one more time than the previously generated
    function.

    >>> increment = lambda x: x + 1
    >>> church = church_generator(increment)
    >>> for _ in range(5):
    ...     fn = next(church)
    ...     print(fn(0))
    0
    1
    2
    3
    4
    """

    g = lambda x: x
    while True:
        yield g
        g = lambda x, g=g: f(g(x))
