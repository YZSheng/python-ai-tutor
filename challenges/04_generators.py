"""
Challenge 04: Generators & Lazy Evaluation

PROBLEM:
--------
Implement a generator function that yields Fibonacci numbers indefinitely.

This introduces generators—Python's approach to lazy evaluation. Coming from 
Clojure, you'll recognize this pattern from lazy sequences. In Python, generators 
provide memory-efficient iteration by computing values on-demand rather than 
storing entire sequences in memory.

The key insight: `yield` transforms a function into a generator. Each time you 
call `next()` on the generator, it resumes from where it last yielded.

EXAMPLE:
--------
>>> fib_gen = fibonacci()
>>> next(fib_gen)
0
>>> next(fib_gen)
1
>>> next(fib_gen)
1
>>> next(fib_gen)
2
>>> next(fib_gen)
3
>>> next(fib_gen)
5

>>> # Or use in a loop
>>> fib_gen = fibonacci()
>>> result = []
>>> for num in fib_gen:
...     if num > 20:
...         break
...     result.append(num)
>>> result
[0, 1, 1, 2, 3, 5, 8, 13]

REQUIREMENTS:
-------------
- Implement as a generator function using `yield`
- Should generate Fibonacci numbers indefinitely (infinite sequence)
- Start with 0, 1, 1, 2, 3, 5, 8, 13...
- Include type hints (use `Generator` from typing)
- Must be memory-efficient (don't pre-compute or store all values)

HINT:
-----
Use `yield` to produce values one at a time. Keep track of only the last 
two numbers—you don't need to store the entire sequence.
"""

from typing import Generator


def fibonacci() -> Generator[int, None, None]:
    """
    Generate Fibonacci numbers indefinitely.
    
    Yields:
        The next Fibonacci number in the sequence
    """
    last, current = 0, 1
    while True:
        yield last
        last, current = current, last + current


# Test cases
def test_first_ten():
    fib_gen = fibonacci()
    result = [next(fib_gen) for _ in range(10)]
    assert result == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]


def test_starts_correctly():
    fib_gen = fibonacci()
    assert next(fib_gen) == 0
    assert next(fib_gen) == 1
    assert next(fib_gen) == 1


def test_continues_indefinitely():
    fib_gen = fibonacci()
    # Skip first 20 numbers
    for _ in range(20):
        next(fib_gen)
    # Should still work
    val = next(fib_gen)
    assert val > 0


def test_multiple_generators():
    # Each generator should be independent
    gen1 = fibonacci()
    gen2 = fibonacci()
    
    assert next(gen1) == 0
    assert next(gen2) == 0
    assert next(gen1) == 1
    assert next(gen2) == 1


def test_in_loop():
    fib_gen = fibonacci()
    result = []
    for num in fib_gen:
        if num > 20:
            break
        result.append(num)
    assert result == [0, 1, 1, 2, 3, 5, 8, 13]


def test_is_generator():
    # Verify it's actually a generator, not a list
    gen = fibonacci()
    assert hasattr(gen, '__next__')
    assert hasattr(gen, '__iter__')
