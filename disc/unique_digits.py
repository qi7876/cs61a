def unique_digits(n):
    """
    Arguments: A positive number.
    Return: The number of the unique digits in the n.

    >>> unique_digits(891249)
    4
    """
    def unique_digit(n, i):
        """
        Argument: A positive number. Another number i for search(0 <= i < 10).
        Return: The number of i in n.

        >>> has_digit(123, 1)
        1
        """
        counter = 0
        while n > 0:
            if n % 10 == i:
               counter += 1
            n = n // 10
        if counter == 1:
            return True
        else:
            return False

    unique_digits_number = 0
    number_0to9 = 9
    while number_0to9 >= 0:
        if unique_digit(n, number_0to9):
           unique_digits_number += 1
        number_0to9 -= 1 
    
    return unique_digits_number


if __name__ == "__main__":
    print(unique_digits(1345786134))
    