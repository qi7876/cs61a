from collections.abc import Iterator


def differences(t: Iterator[int]):
    """Yield the differences between adjacent values from iterator t.

    >>> list(differences(iter([5, 2, -100, 103])))
    [-3, -102, 203]
    >>> next(differences(iter([39, 100])))
    61
    """
    "*** YOUR CODE HERE ***"
    current_num: int = next(t)

    for i in t:
        last_num = current_num
        current_num = i
        yield current_num - last_num






















