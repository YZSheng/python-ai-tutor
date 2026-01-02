"""
Challenge 02: Dictionary Comprehension & Word Frequency

PROBLEM:
--------
Given a list of words, count the frequency of each word and return a dictionary.

This challenge introduces dictionary comprehensions—the dict analog to list 
comprehensions. In imperative languages, you'd use a mutable map and loop to 
accumulate counts. Python offers more elegant approaches through both dict 
comprehensions AND the built-in `Counter` from collections.

For this challenge, use ONLY dict comprehension (we'll cover Counter later).

EXAMPLE:
--------
>>> word_frequency(["apple", "banana", "apple", "cherry", "banana", "apple"])
{"apple": 3, "banana": 2, "cherry": 1}

>>> word_frequency([])
{}

>>> word_frequency(["single"])
{"single": 1}

REQUIREMENTS:
-------------
- Use a dictionary comprehension (not a for loop)
- Include type hints
- Should handle edge cases (empty list, single word)
- The core logic should be concise and readable

HINT:
-----
Think about what you need to iterate over and how to count occurrences.
You might find the `.count()` method on lists useful.
"""


def word_frequency(words: list[str]) -> dict[str, int]:
    """
    Count the frequency of each word in the list.
    
    Args:
        words: List of words
        
    Returns:
        Dictionary mapping words to their frequency counts
    """
    from collections import Counter
    return dict(Counter(words))


# Test cases
def test_basic():
    assert word_frequency(["apple", "banana", "apple", "cherry", "banana", "apple"]) == {
        "apple": 3,
        "banana": 2,
        "cherry": 1,
    }


def test_empty():
    assert word_frequency([]) == {}


def test_single_word():
    assert word_frequency(["single"]) == {"single": 1}


def test_duplicates():
    assert word_frequency(["a", "a", "a"]) == {"a": 3}


def test_all_unique():
    assert word_frequency(["x", "y", "z"]) == {"x": 1, "y": 1, "z": 1}
