"""
Challenge 03: Function Decorators & Metaprogramming

PROBLEM:
--------
Create a decorator that validates function arguments at runtime.

Specifically, build a `@validate_positive` decorator that:
1. Wraps a function to check that all numeric arguments are positive (> 0)
2. Raises a ValueError with a descriptive message if any argument is not positive
3. Otherwise, allows the function to execute normally

This introduces decorators—Python's most elegant metaprogramming tool.
From your Java/Kotlin background, think of decorators as a cleaner alternative
to wrapper classes or aspect-oriented programming. Python's decorator syntax
is syntactic sugar for function composition: `@decorator` is equivalent to
`func = decorator(func)`.

EXAMPLE:
--------
>>> @validate_positive
... def multiply(a: int, b: int) -> int:
...     return a * b
...
>>> multiply(3, 5)
15

>>> multiply(-2, 5)
ValueError: multiply() received non-positive argument: a=-2

>>> multiply(0, 5)
ValueError: multiply() received non-positive argument: a=0

REQUIREMENTS:
-------------
- Create a decorator function named `validate_positive`
- It should check all arguments (both positional and keyword)
- Raise ValueError with the message format: "{func_name}() received non-positive argument: {arg_name}={arg_value}"
- The decorated function should work exactly like the original if validation passes
- Must preserve the original function's name and docstring (use functools.wraps)

HINT:
-----
Use `functools.wraps` to preserve metadata. Access function arguments using *args, **kwargs.
"""

from functools import wraps
from typing import Any, Callable


def validate_positive(func: Callable) -> Callable:
    """
    Decorator that validates all numeric arguments are positive (> 0).

    Args:
        func: The function to decorate

    Returns:
        Wrapped function with validation
    """

    def wrapper(*args, **kwargs):
        from inspect import signature

        sig = signature(func)
        bound_args = sig.bind(*args, **kwargs)
        bound_args.apply_defaults()

        for name, value in bound_args.arguments.items():
            if isinstance(value, (int, float)) and value <= 0:
                raise ValueError(
                    f"{func.__name__}() received non-positive argument: {name}={value}"
                )
        return func(*args, **kwargs)

    wraps(func)(wrapper)
    return wrapper


# Test cases
def test_basic_validation():
    @validate_positive
    def add(x: int, y: int) -> int:
        return x + y

    assert add(3, 5) == 8
    assert add(1, 1) == 2


def test_reject_negative():
    @validate_positive
    def multiply(a: int, b: int) -> int:
        return a * b

    try:
        multiply(-2, 5)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "non-positive argument" in str(e)
        assert "a=-2" in str(e)


def test_reject_zero():
    @validate_positive
    def divide(a: int, b: int) -> float:
        return a / b

    try:
        divide(10, 0)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "b=0" in str(e)


def test_keyword_arguments():
    @validate_positive
    def power(base: int, exponent: int = 2) -> int:
        return base**exponent

    assert power(2, exponent=3) == 8

    try:
        power(2, exponent=-1)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "exponent=-1" in str(e)


def test_preserves_metadata():
    @validate_positive
    def documented_func(x: int) -> int:
        """This is a documented function."""
        return x * 2

    assert documented_func.__name__ == "documented_func"
    assert "documented" in documented_func.__doc__
