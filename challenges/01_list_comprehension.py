"""
Challenge 01: List Comprehension & Pythonic Iteration

PROBLEM:
--------
Given a list of integers, implement a function that:
1. Filters out all negative numbers
2. Squares the remaining numbers
3. Returns the result as a new list

This challenge introduces list comprehensions—the idiomatic Python way to
transform and filter sequences. Coming from imperative languages, you might
be tempted to use traditional for loops, but Python's comprehension syntax
is more concise, readable, and performant.

EXAMPLE:
--------
>>> square_positives([1, -2, 3, -4, 5])
[1, 9, 25]

>>> square_positives([])
[]

>>> square_positives([-1, -2, -3])
[]

REQUIREMENTS:
-------------
- Use a list comprehension (not a traditional for loop)
- The solution should be a one-liner
- Include type hints for the function signature
"""


def square_positives(numbers: list[int]) -> list[int]:
    return [x**2 for x in numbers if x >= 0]


# Test cases
def test_basic():
    assert square_positives([1, -2, 3, -4, 5]) == [1, 9, 25]


def test_empty():
    assert square_positives([]) == []


def test_all_negative():
    assert square_positives([-1, -2, -3]) == []


def test_single_positive():
    assert square_positives([10]) == [100]


def test_mixed_with_zero():
    assert square_positives([0, 1, -1]) == [0, 1]
