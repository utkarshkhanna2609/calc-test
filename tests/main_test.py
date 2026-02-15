import pytest
from unittest.mock import patch, MagicMock
from src.main import main


@pytest.fixture
def patched_calculator():
    """Patch src.main.Calculator and return the mock instance."""
    with patch('src.main.Calculator') as Calc:
        instance = MagicMock(name='CalculatorInstance')
        Calc.return_value = instance
        yield instance


def test_main_happy_path_and_errors(patched_calculator, capsys):
    """Test main prints correct outputs for demo, expression, and error cases."""
    # Configure return values and exceptions in the exact order of calls
    patched_calculator.calculate.side_effect = [
        15,   # 10 + 5
        5,    # 10 - 5
        50,   # 10 * 5
        2,    # 10 / 5
        5,    # 0 + 5
        -30,  # -10 * 3
        20,   # expression "10 + 5 * 2"
        ValueError('division by zero'),      # 10 / 0
        ValueError('unsupported operation'), # 10 % 5
    ]
    patched_calculator.get_supported_operations.return_value = ['+', '-', '*', '/']

    # Execute main and capture output
    main()
    captured = capsys.readouterr().out

    # Headers
    assert 'Calculator Demo' in captured
    assert '===============' in captured
    assert '--- Expression Evaluation ---' in captured
    assert '--- Error Handling ---' in captured

    # Basic operations outputs
    assert '10 + 5 = 15' in captured
    assert '10 - 5 = 5' in captured
    assert '10 * 5 = 50' in captured
    assert '10 / 5 = 2' in captured
    assert '0 + 5 = 5' in captured
    assert '-10 * 3 = -30' in captured

    # Expression evaluation
    assert "Expression '10 + 5 * 2' = 20" in captured

    # Error cases
    assert 'Division by zero: division by zero' in captured
    assert 'Unsupported operation: unsupported operation' in captured

    # Supported operations
    assert 'Supported operations: +, -, *, /' in captured

    # Verify call counts
    assert patched_calculator.calculate.call_count == 9
    patched_calculator.get_supported_operations.assert_called_once()


@pytest.mark.parametrize(
    "a,op,b,expected",
    [
        (10, '+', 5, '15'),
        (10, '-', 5, '5'),
        (10, '*', 5, '50'),
        (10, '/', 5, '2'),
        (0, '+', 5, '5'),
        (-10, '*', 3, '-30'),
    ],
)
def test_main_basic_operations_parametrized_prints_results(patched_calculator, capsys, a, op, b, expected):
    """Test main prints each basic operation result as expected (parametrized)."""
    # Side-effect function that mirrors expected behavior for all calls within main
    def calc_side_effect(x, y, oper):
        # Expression path
        if isinstance(oper, str) and ' ' in oper:
            return 20
        # Error paths
        if oper == '/' and y == 0:
            raise ValueError('division by zero')
        if oper == '%':
            raise ValueError('unsupported operation')
        # Basic operations
        if oper == '+':
            return x + y
        if oper == '-':
            return x - y
        if oper == '*':
            return x * y
        if oper == '/':
            # Return int for clean divisions to match expected output
            return int(x / y) if y != 0 and x % y == 0 else x / y
        # Default (shouldn't occur in this test)
        return None

    patched_calculator.calculate.side_effect = calc_side_effect
    patched_calculator.get_supported_operations.return_value = ['+', '-', '*', '/']

    main()
    out = capsys.readouterr().out
    assert f"{a} {op} {b} = {expected}" in out