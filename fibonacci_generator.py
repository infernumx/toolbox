#!/usr/bin/env python3

import random
from typing import Generator


def is_perfect_square(n: int) -> bool:
    return n == int(n ** 0.5) ** 2


def is_fibonnaci(n: int) -> bool:
    return is_perfect_square(5 * n ** 2 + 4) or is_perfect_square(5 * n ** 2 - 4)


def generate_data(
    size: int, int_range: tuple[int, int]
) -> Generator[tuple[int, bool], None, None]:
    for _ in range(size):
        yield (n := random.randrange(*int_range)), is_fibonnaci(n)


def main() -> None:
    states = ["not a fibonacci number", "a fibonacci number"]
    for n, fib_state in generate_data(10, (1, 100)):
        print(f"{n} is {states[fib_state]}")


if __name__ == "__main__":
    main()
