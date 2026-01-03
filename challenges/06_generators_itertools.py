"""
Challenge 06: Generators & Itertools - Lazy Evaluation

PROBLEM:
--------
Implement a memory-efficient log file analyzer that processes large files
without loading everything into memory.

Create a function `analyze_logs` that:
1. Takes a file path and optional filters
2. Returns statistics about log entries using generators
3. Processes the file lazily (line by line)
4. Supports filtering by log level (INFO, WARNING, ERROR)
5. Returns: total count, counts by level, and top 3 most common messages

Coming from Clojure, you'll recognize this as similar to lazy sequences.
Generators are Python's approach to lazy evaluation—they compute values
on-demand rather than all at once. The `yield` keyword makes a function
into a generator.

From JavaScript/TypeScript, think of generators as similar to async iterators,
but for synchronous lazy computation.

EXAMPLE LOG FORMAT:
-------------------
2024-01-15 10:23:45 INFO User logged in
2024-01-15 10:24:12 ERROR Database connection failed
2024-01-15 10:24:15 WARNING Cache miss for key: user_123
2024-01-15 10:25:01 INFO User logged out

EXPECTED OUTPUT:
----------------
{
    'total': 1000,
    'by_level': {'INFO': 750, 'WARNING': 200, 'ERROR': 50},
    'top_messages': [
        ('User logged in', 300),
        ('User logged out', 280),
        ('Cache miss', 150)
    ]
}

REQUIREMENTS:
-------------
1. Implement helper generators:
   - `read_logs(file_path)`: yields lines from file
   - `parse_log_line(line)`: parses a line into (timestamp, level, message)
   - `filter_by_level(logs, levels)`: filters logs by level(s)

2. Implement `analyze_logs(file_path, levels=None)`:
   - Use generators to avoid loading entire file
   - Count total lines processed
   - Count by log level
   - Find top 3 most common messages (normalized)
   - If `levels` is provided (list), only process those levels

3. Use `itertools` and `collections` where appropriate
4. Include type hints for all functions
5. Handle edge cases (empty files, malformed lines)

HINTS:
------
- Use `yield` to create generator functions
- `itertools` has useful functions like `islice`, `chain`, `groupby`
- `collections.Counter` is perfect for counting occurrences
- Generator expressions: `(x for x in iterable if condition)`
- Remember: generators can only be consumed once!

LEARNING GOALS:
---------------
- Understand generators vs lists (lazy vs eager)
- Use `yield` to create generators
- Chain generators together for data pipelines
- Apply `itertools` for elegant iteration patterns
- Recognize when to use lazy evaluation for efficiency
"""

import os
import pytest
from collections import Counter
from itertools import islice
from typing import Iterator, Optional, Tuple, Dict, List


def read_logs(file_path: str) -> Iterator[str]:
    """
    Generator that yields lines from a log file.

    Args:
        file_path: Path to the log file

    Yields:
        Non-empty lines from the file
    """
    # TODO: Implement this generator
    # Hint: Use a context manager to open the file
    # Hint: Strip whitespace and skip empty lines
    pass


def parse_log_line(line: str) -> Optional[Tuple[str, str, str]]:
    """
    Parse a log line into components.

    Expected format: "YYYY-MM-DD HH:MM:SS LEVEL Message text"

    Args:
        line: A single log line

    Returns:
        Tuple of (timestamp, level, message) or None if malformed

    Example:
        >>> parse_log_line("2024-01-15 10:23:45 INFO User logged in")
        ('2024-01-15 10:23:45', 'INFO', 'User logged in')
    """
    # TODO: Implement parsing logic
    # Hint: Split on whitespace, but be careful with the message part
    # Hint: Return None for malformed lines
    parts = line.split(" ", 3)
    if len(parts) < 4:
        return None
    date, time, level, message = parts
    return (f"{date} {time}", level, message)


def filter_by_level(
    logs: Iterator[Tuple[str, str, str]],
    levels: Optional[List[str]] = None
) -> Iterator[Tuple[str, str, str]]:
    """
    Generator that filters logs by level.

    Args:
        logs: Iterator of (timestamp, level, message) tuples
        levels: List of levels to include (None means include all)

    Yields:
        Log tuples matching the specified levels
    """
    # TODO: Implement filtering generator
    # Hint: If levels is None, yield everything
    # Hint: Use a generator expression or yield in a loop
    pass


def analyze_logs(
    file_path: str,
    levels: Optional[List[str]] = None
) -> Dict[str, any]:
    """
    Analyze a log file and return statistics.

    Args:
        file_path: Path to the log file
        levels: Optional list of levels to analyze (e.g., ['ERROR', 'WARNING'])

    Returns:
        Dictionary with keys:
        - 'total': Total number of logs processed
        - 'by_level': Dict mapping level to count
        - 'top_messages': List of (message, count) tuples for top 3 messages

    Example:
        >>> analyze_logs('app.log', ['ERROR'])
        {
            'total': 50,
            'by_level': {'ERROR': 50},
            'top_messages': [('Database error', 20), ('Timeout', 15), ...]
        }
    """
    # TODO: Implement the main analysis function
    # Hint: Chain generators together: read -> parse -> filter
    # Hint: You'll need to consume the generator to count/analyze
    # Hint: Consider using itertools.tee if you need to iterate multiple times
    # Hint: Use Counter for counting messages
    pass


# Test cases
def test_parse_log_line():
    line = "2024-01-15 10:23:45 INFO User logged in"
    result = parse_log_line(line)
    assert result == ('2024-01-15 10:23:45', 'INFO', 'User logged in')

    # Test malformed line
    assert parse_log_line("invalid") is None
    assert parse_log_line("2024-01-15 10:23:45 INFO") is None


@pytest.mark.skip()
def test_read_logs(tmp_path):
    # Create a test log file
    log_file = tmp_path / "test.log"
    log_file.write_text("""2024-01-15 10:23:45 INFO User logged in
2024-01-15 10:24:12 ERROR Database connection failed
2024-01-15 10:24:15 WARNING Cache miss

2024-01-15 10:25:01 INFO User logged out
""")

    lines = list(read_logs(str(log_file)))
    assert len(lines) == 4  # Empty lines should be skipped
    assert "INFO User logged in" in lines[0]


@pytest.mark.skip()
def test_filter_by_level():
    logs = [
        ('2024-01-15 10:23:45', 'INFO', 'Message 1'),
        ('2024-01-15 10:24:12', 'ERROR', 'Message 2'),
        ('2024-01-15 10:24:15', 'WARNING', 'Message 3'),
        ('2024-01-15 10:25:01', 'INFO', 'Message 4'),
    ]

    # Filter to only ERROR
    filtered = list(filter_by_level(iter(logs), ['ERROR']))
    assert len(filtered) == 1
    assert filtered[0][1] == 'ERROR'

    # No filter (all pass through)
    all_logs = list(filter_by_level(iter(logs), None))
    assert len(all_logs) == 4


@pytest.mark.skip()
def test_analyze_logs(tmp_path):
    log_file = tmp_path / "test.log"
    log_file.write_text("""2024-01-15 10:23:45 INFO User logged in
2024-01-15 10:24:12 ERROR Database connection failed
2024-01-15 10:24:15 WARNING Cache miss
2024-01-15 10:25:01 INFO User logged out
2024-01-15 10:25:02 INFO User logged in
2024-01-15 10:25:03 ERROR Database connection failed
2024-01-15 10:25:04 INFO User logged in
""")

    result = analyze_logs(str(log_file))

    assert result['total'] == 7
    assert result['by_level']['INFO'] == 4
    assert result['by_level']['ERROR'] == 2
    assert result['by_level']['WARNING'] == 1
    assert len(result['top_messages']) <= 3

    # Top message should be "User logged in" (appears 3 times)
    assert result['top_messages'][0] == ('User logged in', 3)


@pytest.mark.skip()
def test_analyze_logs_filtered(tmp_path):
    log_file = tmp_path / "test.log"
    log_file.write_text("""2024-01-15 10:23:45 INFO User logged in
2024-01-15 10:24:12 ERROR Database connection failed
2024-01-15 10:24:15 WARNING Cache miss
2024-01-15 10:25:01 INFO User logged out
2024-01-15 10:25:02 ERROR Database connection failed
""")

    # Only analyze ERROR logs
    result = analyze_logs(str(log_file), levels=['ERROR'])

    assert result['total'] == 2
    assert result['by_level'] == {'ERROR': 2}
    assert result['top_messages'][0] == ('Database connection failed', 2)


@pytest.mark.skip()
def test_generator_memory_efficiency():
    """
    This test verifies that generators are actually lazy.
    We create a generator but don't consume it fully.
    """
    def large_log_generator():
        for i in range(1000000):
            yield f"2024-01-15 10:23:45 INFO Message {i % 100}"

    # Take only first 10 - should not generate all 1,000,000
    gen = large_log_generator()
    first_ten = list(islice(gen, 10))

    assert len(first_ten) == 10
    # If this completes quickly, generators are working correctly!

