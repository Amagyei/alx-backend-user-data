#!/usr/bin/env python3

def fibonacci(n: int) -> int:
    """ return the nth fibonacci number """
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        sequence = [0, 1]
        for i in range(2, n + 1):
            sequence.append(sequence[-1] + sequence[-2])

        return sequence