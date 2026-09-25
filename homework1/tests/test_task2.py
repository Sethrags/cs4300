import pytest

from src.task2 import integer_number, float_number, is_student, message


@pytest.mark.parametrize(
    "value, expected_type, expected_value",
    [
        (integer_number, int, 10),
        (float_number, float, 3.14),
        (message, str, "Hello"),
        (is_student, bool, True),
    ],
)
def test_data_types_and_values(value, expected_type, expected_value):
    assert isinstance(value, expected_type)
    assert value == expected_value