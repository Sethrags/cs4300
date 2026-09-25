import pytest

from src.task4 import calculate_discount


@pytest.mark.parametrize(
    "price, discount, expected",
    [
        (100, 20, 80),
        (50.0, 10, 45.0),
        (19.99, 25.0, 14.9925),
    ],
)
def test_calculate_discount(price, discount, expected):
    assert calculate_discount(price, discount) == expected


@pytest.mark.parametrize(
    "price, discount, error",
    [
        (-10, 20, ValueError),
        (100, -5, ValueError),
        (100, 101, ValueError),
        ("100", 20, TypeError),
        (100, "20", TypeError),
    ],
)
def test_invalid_discount_values(price, discount, error):
    with pytest.raises(error):
        calculate_discount(price, discount)