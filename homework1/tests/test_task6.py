from pathlib import Path

import pytest

from src.task6 import count_words


assignment_file = Path(__file__).parent.parent / "task6_read_me.txt"


def test_assignment_file_word_count():
    assert count_words(assignment_file) == 104


@pytest.mark.parametrize(
    "text, expected_count",
    [
        ("", 0),
        ("hello", 1),
        ("one   two\nthree four", 4),
    ],
)
def test_count_words_with_different_files(tmp_path, text, expected_count):
    test_file = tmp_path / "test_file.txt"
    test_file.write_text(text, encoding="utf-8")

    assert count_words(test_file) == expected_count


def test_count_words_missing_file(tmp_path):
    missing_file = tmp_path / "missing.txt"

    with pytest.raises(FileNotFoundError):
        count_words(missing_file)