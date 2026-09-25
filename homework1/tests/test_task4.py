from decimal import Decimal
from fractions import Fraction

import pytest

from src.task4 import calculate_discount


@pytest.mark.parametrize(
    "price, discount, expected",
    [
        (100, 20, 80),
        (50.0, 10, 45.0),
        (Decimal("100"), Decimal("12.5"), Decimal("87.5")),
        (Fraction(100), Fraction(25), Fraction(75)),
    ],
)
def test_calculate_discount(price, discount, expected):
    assert calculate_discount(price, discount) == expected


def test_calculate_discount_with_float():
    assert calculate_discount(19.99, 25.0) == pytest.approx(14.9925)


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