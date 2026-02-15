import pytest
from unittest.mock import patch

from src.operations.multiply_operation import MultiplyOperation


@pytest.fixture
def multiply_operation():
    """Create a MultiplyOperation instance for testing."""
    return MultiplyOperation()


def test_multiplyoperation_initialization(multiply_operation):
    """Test MultiplyOperation initialization returns a valid instance."""
    assert isinstance(multiply_operation, MultiplyOperation)


def test_multiplyoperation_get_symbol_returns_asterisk(multiply_operation):
    """Test get_symbol returns '*' as the multiplication symbol."""
    assert multiply_operation.get_symbol() == '*'


def test_multiplyoperation_get_symbol_called_on_class_raises_typeerror():
    """Test calling get_symbol on the class (without instance) raises TypeError."""
    with pytest.raises(TypeError):
        MultiplyOperation.get_symbol()


def test_multiplyoperation_execute_positive_integers(multiply_operation):
    """Test execute with positive integers."""
    result = multiply_operation.execute(3, 5)
    assert result == pytest.approx(15)


def test_multiplyoperation_execute_negative_and_positive(multiply_operation):
    """Test execute with one negative and one positive operand."""
    result = multiply_operation.execute(-2, 4)
    assert result == pytest.approx(-8)


def test_multiplyoperation_execute_both_negative_floats(multiply_operation):
    """Test execute with both operands negative floats."""
    result = multiply_operation.execute(-2.5, -3.7)
    assert result == pytest.approx(7.4)


def test_multiplyoperation_execute_fractional_left_operand_truncates(multiply_operation):
    """Test execute truncates the left operand by using int(abs(a)) for loop count."""
    result = multiply_operation.execute(2.5, 2)
    # int(abs(2.5)) == 2, so 2 * abs(2) == 4, both positive -> 4
    assert result == pytest.approx(4.0)


def test_multiplyoperation_execute_fractional_right_operand_accumulates(multiply_operation):
    """Test execute accumulates abs(right) value, even if right is fractional."""
    result = multiply_operation.execute(2, -2.5)
    # int(abs(2)) == 2, sum of 2 times abs(-2.5) == 5, then sign becomes negative
    assert result == pytest.approx(-5.0)


def test_multiplyoperation_execute_zero_handling(multiply_operation):
    """Test execute handles zero correctly regardless of sign of the other operand."""
    assert multiply_operation.execute(0, 100) == pytest.approx(0)
    assert multiply_operation.execute(-3, 0) == pytest.approx(0)
    assert multiply_operation.execute(0.0, -5.5) == pytest.approx(0)


def test_multiplyoperation_execute_small_fraction_left_results_zero(multiply_operation):
    """Test execute returns zero when left operand fractional part truncates to zero."""
    result = multiply_operation.execute(0.5, 100)
    # int(abs(0.5)) == 0, so the loop never runs
    assert result == pytest.approx(0)


def test_multiplyoperation_execute_non_integer_left_truncation_behavior(multiply_operation):
    """Test execute with non-integer left operand truncates toward zero."""
    result = multiply_operation.execute(1.9, 3)
    # int(abs(1.9)) == 1 -> result is 3
    assert result == pytest.approx(3)


def test_multiplyoperation_execute_uses_abs_function_mocked(multiply_operation):
    """Test execute uses abs for both operands by mocking abs in the module."""
    a, b = -3.2, -4.8
    with patch('src.operations.multiply_operation.abs', wraps=abs, create=True) as mock_abs:
        result = multiply_operation.execute(a, b)
        # Expect two calls: abs(a) and abs(b)
        assert mock_abs.call_count == 2
        called_args = [call.args[0] for call in mock_abs.call_args_list]
        assert a in called_args
        assert b in called_args
        # Check the computed result with expected behavior: int(abs(-3.2)) == 3; 3 * abs(-4.8) == 14.4; both negatives -> positive
        assert result == pytest.approx(14.4)


def test_multiplyoperation_execute_raises_typeerror_for_non_numeric(multiply_operation):
    """Test execute raises TypeError when non-numeric left operand is provided."""
    with pytest.raises(TypeError):
        multiply_operation.execute("not-a-number", 2)


def test_multiplyoperation_execute_raises_valueerror_for_nan_left(multiply_operation):
    """Test execute raises ValueError when left operand is NaN (int(abs(nan)) invalid)."""
    with pytest.raises(ValueError):
        multiply_operation.execute(float('nan'), 1.0)


def test_multiplyoperation_execute_raises_overflowerror_for_infinite_left(multiply_operation):
    """Test execute raises OverflowError when left operand is infinity (int(abs(inf)) invalid)."""
    with pytest.raises(OverflowError):
        multiply_operation.execute(float('inf'), 2.0)