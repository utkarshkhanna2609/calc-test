import pytest
from unittest.mock import patch
from src.operations.subtract_operation import SubtractOperation, Operation


@pytest.fixture
def subtract_op():
    """Create a SubtractOperation instance for testing."""
    return SubtractOperation()


def test_SubtractOperation_initialization(subtract_op):
    """Test that SubtractOperation can be instantiated and is a subclass of Operation."""
    assert isinstance(subtract_op, SubtractOperation)
    assert issubclass(SubtractOperation, Operation)


def test_SubtractOperation_get_symbol_returns_dash(subtract_op):
    """Test that get_symbol returns the subtraction symbol '-'."""
    assert subtract_op.get_symbol() == "-"


def test_SubtractOperation_execute_basic_integers_swapped_operands(subtract_op):
    """Test execute with basic integers ensuring operand order is swapped (b - a) and result is a string."""
    result = subtract_op.execute(2, 5)  # b - a -> 5 - 2 = 3
    assert isinstance(result, str)
    assert result == "3"


def test_SubtractOperation_execute_float_result_string_and_value(subtract_op):
    """Test execute with floats returns string representation and numeric value matches with approx."""
    result = subtract_op.execute(1.1, 3.3)  # 3.3 - 1.1 = 2.2 (string may reflect float precision)
    assert isinstance(result, str)
    assert float(result) == pytest.approx(2.2)


def test_SubtractOperation_execute_negative_numbers(subtract_op):
    """Test execute with negative numbers (b - a) and result as string."""
    result = subtract_op.execute(-5, -2)  # -2 - (-5) = 3
    assert result == "3"


def test_SubtractOperation_execute_zero_and_large_number(subtract_op):
    """Test execute with zero and a large number; validate numeric value with approx."""
    result = subtract_op.execute(0.0, 1_000_000_000_000.0)  # 1e12 - 0 = 1e12
    assert isinstance(result, str)
    assert float(result) == pytest.approx(1_000_000_000_000.0)


def test_SubtractOperation_execute_infinity_result(subtract_op):
    """Test execute with infinity returns appropriate string representation."""
    result = subtract_op.execute(float('inf'), 1.0)  # 1 - inf = -inf
    assert result == "-inf"


def test_SubtractOperation_execute_nan_result(subtract_op):
    """Test execute with NaN results in 'nan' string."""
    result = subtract_op.execute(float('nan'), 5.0)  # 5 - nan = nan
    assert result == "nan"


def test_SubtractOperation_execute_raises_typeerror_for_non_numeric(subtract_op):
    """Test execute raises TypeError when provided non-numeric operands."""
    with pytest.raises(TypeError):
        subtract_op.execute("a", 2)

    with pytest.raises(TypeError):
        subtract_op.execute(1, "b")

    with pytest.raises(TypeError):
        subtract_op.execute(None, 3)


def test_SubtractOperation_execute_raises_typeerror_for_missing_argument(subtract_op):
    """Test execute raises TypeError when missing a required operand."""
    with pytest.raises(TypeError):
        subtract_op.execute(1)  # missing 'b'


def test_SubtractOperation_execute_uses_str_conversion_mocked(subtract_op):
    """Test execute uses str() to convert the numeric result to string by mocking str in module namespace."""
    with patch('src.operations.subtract_operation.str', side_effect=lambda x: f"mocked:{x}") as mock_str:
        result = subtract_op.execute(2, 5)  # numeric result is 3
        assert result == "mocked:3"
        mock_str.assert_called_once()
        # Ensure str was called with the correct numeric result (b - a)
        called_with = mock_str.call_args[0][0]
        assert called_with == 3