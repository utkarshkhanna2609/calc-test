import math
import pytest
from unittest.mock import patch
from src.operations.add_operation import AddOperation


@pytest.fixture
def add_operation_instance():
    """Create an AddOperation instance for testing."""
    return AddOperation()


def test_addoperation_initialization(add_operation_instance):
    """Test that AddOperation can be initialized."""
    assert isinstance(add_operation_instance, AddOperation)


def test_addoperation_get_symbol_returns_plus(add_operation_instance):
    """Test that get_symbol returns the '+' symbol."""
    assert add_operation_instance.get_symbol() == '+'


def test_addoperation_execute_adds_positive_numbers(add_operation_instance):
    """Test execute with simple positive integers."""
    result = add_operation_instance.execute(2, 3)
    assert result == pytest.approx(5.0)


def test_addoperation_execute_handles_floats(add_operation_instance):
    """Test execute correctly adds floating point numbers."""
    result = add_operation_instance.execute(2.5, 3.1)
    assert result == pytest.approx(5.6)


def test_addoperation_execute_treats_none_as_zero_first_operand(add_operation_instance):
    """Test execute treats None as 0 when first operand is None."""
    result = add_operation_instance.execute(None, 5)
    assert result == pytest.approx(5.0)


def test_addoperation_execute_treats_none_as_zero_second_operand(add_operation_instance):
    """Test execute treats None as 0 when second operand is None."""
    result = add_operation_instance.execute(5, None)
    assert result == pytest.approx(5.0)


def test_addoperation_execute_both_none_returns_zero(add_operation_instance):
    """Test execute returns 0 when both operands are None."""
    result = add_operation_instance.execute(None, None)
    assert result == pytest.approx(0.0)


def test_addoperation_execute_negative_sum_returns_absolute(add_operation_instance):
    """Test execute returns absolute value when sum is negative (mixed signs)."""
    result = add_operation_instance.execute(-10, 3)
    assert result == pytest.approx(7.0)


def test_addoperation_execute_both_negative_returns_abs_sum(add_operation_instance):
    """Test execute returns absolute value when both operands are negative."""
    result = add_operation_instance.execute(-2, -4)
    assert result == pytest.approx(6.0)


def test_addoperation_execute_zero_sum_returns_zero(add_operation_instance):
    """Test execute returns 0 when the sum is zero."""
    result = add_operation_instance.execute(-1, 1)
    assert result == pytest.approx(0.0)


def test_addoperation_execute_handles_infinity(add_operation_instance):
    """Test execute handles positive infinity correctly."""
    result = add_operation_instance.execute(float('inf'), -5.0)
    assert math.isinf(result) and result > 0


def test_addoperation_execute_handles_negative_infinity_abs(add_operation_instance):
    """Test execute returns positive infinity when sum is negative infinity."""
    result = add_operation_instance.execute(float('-inf'), 10.0)
    assert math.isinf(result) and result > 0


def test_addoperation_execute_with_nan_propagates_nan(add_operation_instance):
    """Test execute propagates NaN when any operand is NaN."""
    result = add_operation_instance.execute(float('nan'), 1.0)
    assert math.isnan(result)


def test_addoperation_execute_raises_typeerror_for_incompatible_types(add_operation_instance):
    """Test execute raises TypeError for incompatible operand types."""
    with pytest.raises(TypeError):
        add_operation_instance.execute("1", 2)


def test_addoperation_execute_wrong_number_of_arguments_raises_typeerror(add_operation_instance):
    """Test execute raises TypeError when called with wrong number of arguments."""
    with pytest.raises(TypeError):
        add_operation_instance.execute(1, 2, 3)


def test_addoperation_execute_calls_abs_when_result_negative(add_operation_instance):
    """Test execute calls built-in abs when the sum is negative."""
    with patch('builtins.abs', autospec=True) as mock_abs:
        mock_abs.return_value = 999.0
        result = add_operation_instance.execute(-3, -4)  # Sum is -7
        assert result == pytest.approx(999.0)
        mock_abs.assert_called_once()
        called_with = mock_abs.call_args[0][0]
        assert called_with == pytest.approx(-7.0)