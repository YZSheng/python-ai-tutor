"""
Challenge 05: Context Managers & Resource Management

PROBLEM:
--------
Implement a context manager that temporarily changes the current working directory.

Create a class `ChangeDirectory` that:
1. Changes to a specified directory when entering the context
2. Returns to the original directory when exiting the context
3. Works with Python's `with` statement
4. Handles exceptions gracefully (always restores original directory)

This introduces context managers—Python's elegant pattern for resource
management. You've seen this with file handling (`with open(...)`), but
context managers are much more general. Coming from Java, think of this
as a better alternative to try-finally blocks or try-with-resources.

The protocol: implement `__enter__()` and `__exit__()` methods.

EXAMPLE:
--------
>>> import os
>>> original = os.getcwd()
>>> print(original)
'/home/user/project'

>>> with ChangeDirectory('/tmp'):
...     print(os.getcwd())
...     # Do work in /tmp
'/tmp'

>>> print(os.getcwd())  # Back to original
'/home/user/project'

>>> # Even if exception occurs
>>> try:
...     with ChangeDirectory('/tmp'):
...         raise ValueError("Something went wrong")
... except ValueError:
...     pass
>>> print(os.getcwd())  # Still restored!
'/home/user/project'

REQUIREMENTS:
-------------
- Implement `__enter__` and `__exit__` methods
- Save the original directory on entry
- Change to the target directory on entry
- Restore the original directory on exit (even if exception occurs)
- Include type hints
- The context manager should be reusable

HINT:
-----
Use `os.getcwd()` to get current directory and `os.chdir()` to change it.
The `__exit__` method receives exception info, but you should always restore
the directory regardless of whether an exception occurred.
"""

import os
from typing import Optional


class ChangeDirectory:
    """
    Context manager for temporarily changing the working directory.

    Example:
        with ChangeDirectory('/tmp'):
            # Work in /tmp
            pass
        # Back to original directory
    """

    def __init__(self, path: str) -> None:
        """
        Initialize the context manager.

        Args:
            path: The directory to change to
        """
        self.new_path = path

    def __enter__(self) -> str:
        """
        Enter the context: save current directory and change to target.

        Returns:
            The target directory path
        """
        self.original_path = os.getcwd()
        os.chdir(self.new_path)
        return self.new_path

    def __exit__(
        self,
        exc_type: Optional[type],
        exc_val: Optional[BaseException],
        exc_tb: Optional[object],
    ) -> None:
        """
        Exit the context: restore the original directory.

        Args:
            exc_type: Exception type if an exception occurred
            exc_val: Exception value if an exception occurred
            exc_tb: Exception traceback if an exception occurred
        """
        os.chdir(self.original_path)


# Test cases
def test_basic_change():
    original = os.getcwd()
    test_dir = os.path.dirname(os.path.abspath(__file__))

    with ChangeDirectory(test_dir):
        assert os.getcwd() == test_dir

    assert os.getcwd() == original


def test_restores_on_exception():
    original = os.getcwd()
    test_dir = os.path.dirname(os.path.abspath(__file__))

    try:
        with ChangeDirectory(test_dir):
            assert os.getcwd() == test_dir
            raise ValueError("Test exception")
    except ValueError:
        pass

    assert os.getcwd() == original


def test_nested_contexts():
    original = os.getcwd()
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    test_dir = os.path.dirname(os.path.abspath(__file__))

    with ChangeDirectory(parent_dir):
        assert os.getcwd() == parent_dir

        with ChangeDirectory(test_dir):
            assert os.getcwd() == test_dir

        assert os.getcwd() == parent_dir

    assert os.getcwd() == original


def test_reusable():
    original = os.getcwd()
    test_dir = os.path.dirname(os.path.abspath(__file__))

    cd = ChangeDirectory(test_dir)

    with cd:
        assert os.getcwd() == test_dir
    assert os.getcwd() == original

    # Use again
    with cd:
        assert os.getcwd() == test_dir
    assert os.getcwd() == original


def test_returns_path():
    test_dir = os.path.dirname(os.path.abspath(__file__))

    with ChangeDirectory(test_dir) as path:
        assert path == test_dir
