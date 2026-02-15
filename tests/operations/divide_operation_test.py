import pytest
from unittest.mock import patch
from src.operations.divide_operation import DivideOperation


@pytest.fixture
def divide_operation():
    """Provide a DivideOperation instance for tests"""
    return DivideOperation()


def test_DivideOperation_initialization(divide_operation):
    """Test that DivideOperation can be initialized"""
    assert isinstance(divide_operation, DivideOperation)
    assert callable(divide_operation.execute)
    assert callable(divide_operation.get_symbol)


def test_DivideOperation_get_symbol_returns_slash(divide_operation):
    """Test get_symbol returns the division symbol '/'"""
    symbol = divide_operation.get_symbol()
    assert symbol == '/'
    assert isinstance(symbol, str)
    assert len(symbol) == 1


def test_DivideOperation_execute_basic_positive(divide_operation):
    """Test execute performs basic division with positive integers"""
    result = divide_operation.execute(10, 2)
    assert result == pytest.approx(5.0)


def test_DivideOperation_execute_fractional_result(divide_operation):
    """Test execute returns correct fractional result for non-even division"""
    result = divide_operation.execute(5, 2)
    assert result == pytest.approx(2.5)


def test_DivideOperation_execute_small_fraction(divide_operation):
    """Test execute handles dividend smaller than divisor"""
    result = divide_operation.execute(1, 2)
    assert result == pytest.approx(0.5)


def test_DivideOperation_execute_float_operands(divide_operation):
    """Test execute works correctly with float operands"""
    result = divide_operation.execute(7.5, 2.5)
    assert result == pytest.approx(3.0)


def test_DivideOperation_execute_negative_numerator(divide_operation):
    """Test execute handles negative numerator"""
    result = divide_operation.execute(-5, 2)
    assert result == pytest.approx(-2.5)


def test_DivideOperation_execute_negative_denominator(divide_operation):
    """Test execute handles negative denominator"""
    result = divide_operation.execute(5, -2)
    assert result == pytest.approx(-2.5)


def test_DivideOperation_execute_both_negative(divide_operation):
    """Test execute handles both numerator and denominator negative"""
    result = divide_operation.execute(-5, -2)
    assert result == pytest.approx(2.5)


def test_DivideOperation_execute_zero_numerator(divide_operation):
    """Test execute returns 0 when numerator is zero"""
    result = divide_operation.execute(0, 5)
    assert result == pytest.approx(0.0)


def test_DivideOperation_execute_by_zero_returns_default_default_value(divide_operation):
    """Test execute returns default value when dividing by zero with default parameter"""
    result = divide_operation.execute(10, 0)
    assert result == pytest.approx(1.0)


def test_DivideOperation_execute_by_zero_returns_custom_default(divide_operation):
    """Test execute returns provided custom default when dividing by zero"""
    result = divide_operation.execute(10, 0, default=42.5)
    assert result == pytest.approx(42.5)


def test_DivideOperation_execute_by_zero_returns_custom_default_negative(divide_operation):
    """Test execute returns provided negative default when dividing by zero"""
    result = divide_operation.execute(-10, 0, default=-3.14)
    assert result == pytest.approx(-3.14)


def test_DivideOperation_execute_accuracy_against_python_division(divide_operation):
    """Test execute matches Python true division for representative values"""
    a, b = 10, 3
    result = divide_operation.execute(a, b)
    expected = a / b
    assert result == pytest.approx(expected)


def test_DivideOperation_execute_invalid_types_raise_typeerror(divide_operation):
    """Test execute raises TypeError when non-numeric inputs are provided"""
    with pytest.raises(TypeError):
        divide_operation.execute("not-a-number", 2)  # abs() on string raises TypeError
    with pytest.raises(TypeError):
        divide_operation.execute(2, "not-a-number")


def test_DivideOperation_execute_calls_abs_with_mocking(divide_operation):
    """Test that execute uses abs() for handling operand signs by mocking abs"""
    a, b = -5.0, 2.0
    with patch('src.operations.divide_operation.abs', wraps=abs) as mock_abs:
        result = divide_operation.execute(a, b)
        # Ensure the result is still correct
        assert result == pytest.approx(-2.5)
        # Verify abs is called for both operands
        assert mock_abs.call_count >= 2
        called_args = [call_args[0][0] for call_args in mock_abs.call_args_list]
        assert a in called_args
        assert b in called_args