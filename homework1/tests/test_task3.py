import pytest

from src.task3 import classify_number, first_ten_primes, sum_one_to_one_hundred


@pytest.mark.parametrize(
    "number, expected",
    [
        (5, "positive"),
        (-5, "negative"),
        (0, "zero"),
    ],
)
def test_classify_number(number, expected):
    assert classify_number(number) == expected


def test_first_ten_primes():
    assert first_ten_primes() == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]


def test_sum_one_to_one_hundred():
    assert sum_one_to_one_hundred() == 5050