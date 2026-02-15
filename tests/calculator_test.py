import math
import pytest
from unittest.mock import Mock, patch

from src.calculator import Calculator


@pytest.fixture
def calculator():
    """Create a Calculator instance for testing."""
    return Calculator()


def test_Calculator_init_sets_defaults_and_sum_zero(calculator):
    """Test Calculator initialization sets default operations and sum to zero."""
    ops = set(calculator.get_supported_operations())
    assert ops == {'+', '-', '*', '/'}
    assert calculator.default_value == 0
    assert calculator.sum == 0


def test_Calculator_init_uses_strategy_classes_mocked():
    """Test that __init__ constructs default operation strategies."""
    with patch('src.calculator.AddOperation') as mock_add, \
         patch('src.calculator.SubtractOperation') as mock_sub, \
         patch('src.calculator.MultiplyOperation') as mock_mul, \
         patch('src.calculator.DivideOperation') as mock_div:
        c = Calculator()
        mock_add.assert_called_once()
        mock_sub.assert_called_once()
        mock_mul.assert_called_once()
        mock_div.assert_called_once()
        assert set(c.get_supported_operations()) == {'+', '-', '*', '/'}


def test_Calculator_register_operation_registers_and_prints_and_calls_execute(calculator, monkeypatch):
    """Test registering a custom operation prints and execute is used in calculate."""
    mock_op = Mock(spec=['execute'])
    mock_op.execute.return_value = 7.0
    with patch('builtins.print') as mock_print:
        calculator.register_operation('^', mock_op)
        mock_print.assert_called_once()
        assert '^' in calculator.get_supported_operations()

    result = calculator.calculate(2, 3, '^')
    assert result == pytest.approx(7.0)
    mock_op.execute.assert_called_once_with(2, 3)


def test_Calculator_calculate_addition_and_running_sum_positive(calculator):
    """Test calculate with addition and running sum updates positively."""
    result = calculator.calculate(2, 3, '+')
    assert result == pytest.approx(5)
    assert calculator.sum == 5


def test_Calculator_calculate_negative_result_updates_sum(calculator):
    """Test calculate with negative result updates running sum by truncated magnitude."""
    result = calculator.calculate(0.0, 2.7, '-')
    assert result == pytest.approx(-2.7)
    # int(abs(-2.7)) == 2
    assert calculator.sum == -2


def test_Calculator_calculate_truncates_float_for_sum(calculator):
    """Test that running sum uses truncated absolute value of the float result."""
    result = calculator.calculate(1.9, 2.0, '+')
    assert result == pytest.approx(3.9)
    assert calculator.sum == 3


def test_Calculator_calculate_unknown_operation_returns_default():
    """Test unknown operation returns the calculator's default_value."""
    c = Calculator(default_value=42)
    result = c.calculate(5, 6, '?')
    assert result == pytest.approx(42)


def test_Calculator_calculate_divide_by_zero_returns_none_and_prints_error(calculator):
    """Test divide by zero returns None and prints an error message."""
    with patch('builtins.print') as mock_print:
        result = calculator.calculate(1, 0, '/')
    assert result is None
    # It should have printed an error
    assert any(str(call.args[0]).startswith("Error occurred:") for call in mock_print.call_args_list)


def test_Calculator_calculate_skips_validation_if_operand_none_and_returns_none(calculator):
    """Test that when an operand is None, validation is skipped and errors are handled gracefully."""
    with patch.object(calculator, '_validate_operands', side_effect=AssertionError("Should not be called")):
        with patch('builtins.print') as mock_print:
            result = calculator.calculate(None, 2, '+')
    assert result is None
    assert any(str(call.args[0]).startswith("Error occurred:") for call in mock_print.call_args_list)


def test_Calculator_calculate_expression_eval_success_does_not_update_sum(calculator):
    """Test expression evaluation via eval returns expected result and does not change running sum."""
    result = calculator.calculate(None, None, '2 + 3 * 4')
    assert result == pytest.approx(14)
    assert calculator.sum == 0


def test_Calculator_calculate_expression_eval_failure_falls_back_to_symbol(calculator):
    """Test invalid expression falls back to performing the provided operation with a and b."""
    # Invalid expression "2 + " will cause eval to fail; should then compute 5 + 7 = 12
    result = calculator.calculate(5, 7, '2 + ')
    assert result == pytest.approx(12)


def test_Calculator_calculate_operation_execute_exception_returns_none_and_prints(calculator):
    """Test that if an operation's execute raises, calculate returns None and prints error."""
    failing_op = Mock(spec=['execute'])
    failing_op.execute.side_effect = RuntimeError("boom")
    calculator.register_operation('X', failing_op)
    with patch('builtins.print') as mock_print:
        result = calculator.calculate(1, 2, 'X')
    assert result is None
    assert any("Error occurred:" in str(call.args[0]) for call in mock_print.call_args_list)


def test_Calculator_validate_operands_raises_for_non_numbers(calculator):
    """Test _validate_operands raises ValueError for non-number operands."""
    with pytest.raises(ValueError):
        calculator._validate_operands("a", 1)
    with pytest.raises(ValueError):
        calculator._validate_operands(1, object())


def test_Calculator_validate_operands_raises_for_nan_and_inf(calculator):
    """Test _validate_operands raises ValueError for NaN and infinite values."""
    with pytest.raises(ValueError):
        calculator._validate_operands(float('nan'), 1.0)
    with pytest.raises(ValueError):
        calculator._validate_operands(1.0, float('nan'))
    with pytest.raises(ValueError):
        calculator._validate_operands(float('inf'), 1.0)
    with pytest.raises(ValueError):
        calculator._validate_operands(1.0, float('-inf'))


def test_Calculator_validate_operands_allows_valid_numbers_and_none(calculator):
    """Test _validate_operands allows valid finite numbers and returns silently for None."""
    # Should not raise
    calculator._validate_operands(1, 2.5)
    calculator._validate_operands(None, 5)
    calculator._validate_operands(5, None)


def test_Calculator_get_supported_operations_reflects_registration(calculator):
    """Test get_supported_operations reflects newly registered operations."""
    initial = set(calculator.get_supported_operations())
    assert initial == {'+', '-', '*', '/'}
    mock_op = Mock(spec=['execute'])
    mock_op.execute.return_value = 1.0
    calculator.register_operation('%', mock_op)
    ops = set(calculator.get_supported_operations())
    assert '%' in ops
    assert {'+', '-', '*', '/'} <= ops