"""
Challenge 07: functools - Functional Programming Patterns

PROBLEM:
--------
Build a configurable data processing pipeline using functools to demonstrate
Python's functional programming capabilities.

Create a pipeline system that:
1. Applies transformations to data streams
2. Uses memoization for expensive computations
3. Implements function composition
4. Uses partial application for configuration

Coming from Clojure, you'll recognize these patterns:
- `partial` is like Clojure's `partial`
- `reduce` is like Clojure's `reduce`
- `lru_cache` is like Clojure's `memoize`
- Function composition is like `comp`

From JavaScript/TypeScript, think of:
- `reduce` as Array.reduce
- `partial` as function currying
- `lru_cache` as memoization decorators

TASKS:
------
1. Implement `compose(*functions)`:
   Composes functions right-to-left (like math: f(g(x)))
   Example: compose(str.upper, str.strip)(" hello ") => "HELLO"

2. Implement `pipe(*functions)`:
   Composes functions left-to-right (like Unix pipes or Clojure's ->>)
   Example: pipe(str.strip, str.upper)(" hello ") => "HELLO"

3. Implement `memoized_fibonacci(n)`:
   Calculate Fibonacci using functools.lru_cache for memoization
   Should be dramatically faster than naive recursion

4. Implement `create_multiplier(factor)`:
   Use functools.partial to create a multiplier function
   Example: times_three = create_multiplier(3)
            times_three(4) => 12

5. Implement `process_data(data, *, filter_fn=None, transform_fn=None, reduce_fn=None)`:
   A flexible data pipeline that:
   - Filters data (optional)
   - Transforms each item (optional)
   - Reduces to final result (optional, defaults to list)
   Use functools.reduce for the reduction step

6. BONUS: Implement `@count_calls` decorator:
   Counts how many times a function is called
   Use functools.wraps to preserve function metadata

REQUIREMENTS:
-------------
1. Use functools.partial, reduce, lru_cache, wraps
2. Include type hints for all functions
3. Functions should be composable and reusable
4. Handle edge cases (empty inputs, None values)
5. Write tests using pytest

HINTS:
------
- functools.reduce(fn, iterable, initial) applies fn cumulatively
- functools.lru_cache(maxsize=128) caches function results
- functools.partial(fn, *args, **kwargs) creates partially applied function
- functools.wraps(fn) copies metadata to wrapper function
- compose applies functions right-to-left: compose(f, g, h)(x) = f(g(h(x)))
- pipe applies functions left-to-right: pipe(f, g, h)(x) = h(g(f(x)))

LEARNING GOALS:
---------------
- Master functools for functional programming in Python
- Understand function composition and partial application
- Use memoization for performance optimization
- Write higher-order functions (functions that take/return functions)
- Compare Python's functional style with Clojure's approach
"""

import functools
import operator
from typing import Callable, Iterable, Optional, TypeVar, Any
import pytest

T = TypeVar('T')
R = TypeVar('R')


def compose(*functions: Callable) -> Callable:
    """
    Compose functions right-to-left.

    compose(f, g, h)(x) equals f(g(h(x)))

    Args:
        *functions: Variable number of functions to compose

    Returns:
        A new function that is the composition of all input functions

    Example:
        >>> add_one = lambda x: x + 1
        >>> double = lambda x: x * 2
        >>> f = compose(add_one, double)  # f(x) = (x * 2) + 1
        >>> f(3)
        7
    """
    # TODO: Implement compose
    # Hint: Apply functions from right to left
    # Hint: Use functools.reduce
    # Hint: Handle empty functions case
    if not functions:
        return lambda x: x  # Identity function
    def composed_function(x):
        for func in reversed(functions):
            x = func(x)
        return x
    return composed_function


def pipe(*functions: Callable) -> Callable:
    """
    Compose functions left-to-right (like Unix pipes or Clojure's ->>).

    pipe(f, g, h)(x) equals h(g(f(x)))

    Args:
        *functions: Variable number of functions to pipe

    Returns:
        A new function that pipes input through all functions

    Example:
        >>> add_one = lambda x: x + 1
        >>> double = lambda x: x * 2
        >>> f = pipe(add_one, double)  # f(x) = (x + 1) * 2
        >>> f(3)
        8
    """
    # TODO: Implement pipe
    # Hint: Similar to compose but left-to-right
    # Hint: You can reverse functions and use compose!
    if not functions:
        return lambda x: x  # Identity function
    def piped_function(x):
        for func in functions:
            x = func(x)
        return x
    return piped_function

def memoized_fibonacci(n: int) -> int:
    """
    Calculate nth Fibonacci number using memoization.

    Use functools.lru_cache for automatic memoization.
    Should be much faster than naive recursion.

    Args:
        n: The position in Fibonacci sequence (0-indexed)

    Returns:
        The nth Fibonacci number

    Example:
        >>> memoized_fibonacci(10)
        55
        >>> memoized_fibonacci(100)  # Fast even for large n!
        354224848179261915075
    """
    # TODO: Implement using @functools.lru_cache decorator
    # Hint: Define an inner function with @lru_cache
    # Hint: Base cases: fib(0) = 0, fib(1) = 1
    # Hint: Recursive case: fib(n) = fib(n-1) + fib(n-2)
    @functools.lru_cache(maxsize=None)
    def fib(n: int) -> int:
        if n == 0:
            return 0
        elif n == 1:
            return 1
        else:
            return fib(n - 1) + fib(n - 2)
    return fib(n)


def create_multiplier(factor: int) -> Callable[[int], int]:
    """
    Create a multiplier function using partial application.

    Args:
        factor: The number to multiply by

    Returns:
        A function that multiplies its input by factor

    Example:
        >>> times_three = create_multiplier(3)
        >>> times_three(4)
        12
        >>> times_ten = create_multiplier(10)
        >>> times_ten(5)
        50
    """

    # TODO: Implement using functools.partial
    # Hint: Use operator.mul (multiply operator as a function)
    # Hint: partial(operator.mul, factor) creates a function that multiplies by factor
    return functools.partial(operator.mul, factor)


def process_data(
    data: Iterable[T],
    *,
    filter_fn: Optional[Callable[[T], bool]] = None,
    transform_fn: Optional[Callable[[T], R]] = None,
    reduce_fn: Optional[Callable[[Any, R], Any]] = None,
    initial: Any = None
) -> Any:
    """
    Process data through a flexible pipeline.

    Args:
        data: Input data to process
        filter_fn: Optional function to filter items (keeps items where fn returns True)
        transform_fn: Optional function to transform each item
        reduce_fn: Optional function to reduce items to single value
        initial: Initial value for reduction (defaults to empty list if reduce_fn is None)

    Returns:
        Processed data (list if no reduce_fn, otherwise the reduced value)

    Example:
        >>> data = [1, 2, 3, 4, 5]
        >>> process_data(data, filter_fn=lambda x: x % 2 == 0)
        [2, 4]
        >>> process_data(data, transform_fn=lambda x: x * 2)
        [2, 4, 6, 8, 10]
        >>> process_data(data, reduce_fn=lambda acc, x: acc + x, initial=0)
        15
        >>> process_data(
        ...     data,
        ...     filter_fn=lambda x: x % 2 == 0,
        ...     transform_fn=lambda x: x * 2,
        ...     reduce_fn=operator.add,
        ...     initial=0
        ... )
        12  # (2 + 4) * 2 = 12
    """
    # TODO: Implement data processing pipeline
    # Hint: Apply filter_fn if provided
    # Hint: Apply transform_fn if provided
    # Hint: Use functools.reduce if reduce_fn provided, otherwise return list
    # Hint: Handle None cases gracefully
    processed_data = data
    if filter_fn is not None:
        processed_data = filter(filter_fn, processed_data)
    if transform_fn is not None:
        processed_data = map(transform_fn, processed_data)
    if reduce_fn is not None:
        return functools.reduce(reduce_fn, processed_data, initial)
    else:
        return list(processed_data)

def count_calls(func: Callable) -> Callable:
    """
    Decorator that counts how many times a function is called.

    The wrapped function will have a 'call_count' attribute.

    Args:
        func: Function to wrap

    Returns:
        Wrapped function with call counting

    Example:
        >>> @count_calls
        ... def greet(name):
        ...     return f"Hello, {name}"
        >>> greet("Alice")
        'Hello, Alice'
        >>> greet("Bob")
        'Hello, Bob'
        >>> greet.call_count
        2
    """
    # TODO: Implement decorator with call counting
    # Hint: Use functools.wraps to preserve function metadata
    # Hint: Use a mutable container (like list) to store count
    # Hint: Add call_count as an attribute to the wrapper
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.call_count += 1
        return func(*args, **kwargs)
    wrapper.call_count = 0
    return wrapper


# ============================================================================
# TESTS
# ============================================================================

def test_compose():
    """Test right-to-left function composition"""
    add_one = lambda x: x + 1
    double = lambda x: x * 2
    square = lambda x: x ** 2

    # compose(f, g)(x) = f(g(x))
    f = compose(add_one, double)
    assert f(3) == 7  # (3 * 2) + 1

    # Three functions
    g = compose(add_one, double, square)
    assert g(3) == 19  # ((3^2) * 2) + 1 = (9 * 2) + 1 = 19

    # Single function
    h = compose(add_one)
    assert h(5) == 6

    # Empty composition should be identity
    identity = compose()
    assert identity(42) == 42


def test_pipe():
    """Test left-to-right function composition"""
    add_one = lambda x: x + 1
    double = lambda x: x * 2
    square = lambda x: x ** 2

    # pipe(f, g)(x) = g(f(x))
    f = pipe(add_one, double)
    assert f(3) == 8  # (3 + 1) * 2

    # Three functions
    g = pipe(add_one, double, square)
    assert g(3) == 64  # ((3 + 1) * 2)^2 = (4 * 2)^2 = 8^2 = 64

    # Should work with strings
    h = pipe(str.strip, str.upper, lambda s: s + "!")
    assert h("  hello  ") == "HELLO!"


def test_memoized_fibonacci():
    """Test memoized Fibonacci calculation"""
    # Basic cases
    assert memoized_fibonacci(0) == 0
    assert memoized_fibonacci(1) == 1
    assert memoized_fibonacci(2) == 1
    assert memoized_fibonacci(10) == 55

    # Large number should be fast due to memoization
    import time
    start = time.time()
    result = memoized_fibonacci(100)
    duration = time.time() - start

    assert result == 354224848179261915075
    assert duration < 0.01  # Should be nearly instant with memoization


def test_create_multiplier():
    """Test partial application for multiplication"""
    times_three = create_multiplier(3)
    assert times_three(4) == 12
    assert times_three(10) == 30

    times_ten = create_multiplier(10)
    assert times_ten(5) == 50

    # Should work with negative numbers
    times_negative = create_multiplier(-2)
    assert times_negative(5) == -10


def test_process_data_filter():
    """Test data processing with filtering"""
    data = [1, 2, 3, 4, 5]

    # Filter even numbers
    result = process_data(data, filter_fn=lambda x: x % 2 == 0)
    assert result == [2, 4]

    # Filter odd numbers
    result = process_data(data, filter_fn=lambda x: x % 2 == 1)
    assert result == [1, 3, 5]


def test_process_data_transform():
    """Test data processing with transformation"""
    data = [1, 2, 3, 4, 5]

    # Double all numbers
    result = process_data(data, transform_fn=lambda x: x * 2)
    assert result == [2, 4, 6, 8, 10]

    # Square all numbers
    result = process_data(data, transform_fn=lambda x: x ** 2)
    assert result == [1, 4, 9, 16, 25]


def test_process_data_reduce():
    """Test data processing with reduction"""
    data = [1, 2, 3, 4, 5]

    # Sum all numbers
    result = process_data(data, reduce_fn=operator.add, initial=0)
    assert result == 15

    # Product of all numbers
    result = process_data(data, reduce_fn=operator.mul, initial=1)
    assert result == 120

    # Concatenate strings
    words = ["Hello", "World", "Python"]
    result = process_data(
        words,
        reduce_fn=lambda acc, x: f"{acc} {x}",
        initial=""
    )
    assert result.strip() == "Hello World Python"


def test_process_data_combined():
    """Test data processing with multiple operations"""
    data = [1, 2, 3, 4, 5, 6]

    # Filter evens, double them, then sum
    result = process_data(
        data,
        filter_fn=lambda x: x % 2 == 0,
        transform_fn=lambda x: x * 2,
        reduce_fn=operator.add,
        initial=0
    )
    assert result == 24  # (2 + 4 + 6) * 2 = 12 * 2 = 24


def test_count_calls():
    """Test call counting decorator"""
    @count_calls
    def greet(name):
        return f"Hello, {name}"

    assert greet.call_count == 0

    greet("Alice")
    assert greet.call_count == 1

    greet("Bob")
    greet("Charlie")
    assert greet.call_count == 3

    # Check that function still works correctly
    assert greet("Dave") == "Hello, Dave"
    assert greet.call_count == 4

    # Check that metadata is preserved
    assert greet.__name__ == "greet"


def test_count_calls_with_args():
    """Test that count_calls works with various function signatures"""
    @count_calls
    def add(a, b, c=0):
        return a + b + c

    assert add(1, 2) == 3
    assert add(1, 2, c=3) == 6
    assert add.call_count == 2
