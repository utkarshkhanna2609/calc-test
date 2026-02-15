import pytest
from unittest.mock import patch
from src.operations.operation import Operation, helper_function
import src.operations.operation as operation_module


class AddOperation(Operation):
    """Concrete operation for testing that uses the module's helper_function."""

    def execute(self, a: float, b: float) -> float:
        return operation_module.helper_function(a, b)

    def get_symbol(self) -> str:
        return "+"


class PartialOperation(Operation):
    """Concrete operation missing one abstract method for testing abstract enforcement."""

    def execute(self, a: float, b: float) -> float:
        return a + b


@pytest.fixture
def add_operation_instance():
    """Create a concrete AddOperation instance for testing."""
    return AddOperation()


def test_Operation_instantiation_abstract_class_raises_type_error():
    """Test that instantiating the abstract Operation class raises TypeError."""
    with pytest.raises(TypeError):
        Operation()  # noqa: F841


def test_Operation_partial_subclass_missing_method_raises_type_error():
    """Test that instantiating a subclass missing an abstract method raises TypeError."""
    with pytest.raises(TypeError):
        PartialOperation()  # noqa: F841


def test_Operation_execute_adds_floats(add_operation_instance):
    """Test execute adds two float operands and returns a float using approx."""
    result = add_operation_instance.execute(1.5, 2.25)
    assert result == pytest.approx(3.75)


def test_Operation_execute_with_negative_numbers(add_operation_instance):
    """Test execute handles negative numbers correctly."""
    result = add_operation_instance.execute(-5.0, 2.0)
    assert result == pytest.approx(-3.0)


def test_Operation_execute_with_zero(add_operation_instance):
    """Test execute correctly handles zero values."""
    result = add_operation_instance.execute(0.0, 0.0)
    assert result == pytest.approx(0.0)


def test_Operation_get_symbol_returns_plus(add_operation_instance):
    """Test get_symbol returns the expected '+' symbol."""
    assert add_operation_instance.get_symbol() == "+"


def test_Operation_execute_calls_helper_function_via_patch(add_operation_instance):
    """Test execute delegates to helper_function by patching it."""
    with patch("src.operations.operation.helper_function", return_value=123.456) as mock_helper:
        result = add_operation_instance.execute(3.0, 4.0)
        mock_helper.assert_called_once_with(3.0, 4.0)
        assert result == pytest.approx(123.456)


def test_Operation_execute_incompatible_types_raises_type_error(add_operation_instance):
    """Test execute raises TypeError when operands are incompatible for addition."""
    with pytest.raises(TypeError):
        add_operation_instance.execute("1", 2)  # str + int raises TypeError


def test_helper_function_adds_numbers():
    """Test the module-level helper_function adds two numbers correctly."""
    assert helper_function(10, 5) == 15
    # Also test with floats using approx
    assert operation_module.helper_function(1.1, 2.2) == pytest.approx(3.3)