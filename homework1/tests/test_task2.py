import pytest

from src.task2 import integer_number, float_number, message, is_student


@pytest.mark.parametrize(
    "value, expected_type",
    [
        (integer_number, int),
        (float_number, float),
        (message, str),
        (is_student, bool),
    ],
)
def test_data_types(value, expected_type):
    assert isinstance(value, expected_type)