from pathlib import Path

import pytest

from src.task6 import count_words


file_path = Path(__file__).parent.parent / "task6_read_me.txt"


@pytest.mark.parametrize(
    "file_name, expected_count",
    [
        (file_path, 104),
    ],
)
def test_count_words(file_name, expected_count):
    assert count_words(file_name) == expected_count