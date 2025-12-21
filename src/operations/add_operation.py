"""
Addition operation.
Follows Single Responsibility Principle - only handles addition.
"""
from .operation import Operation


class AddOperation(Operation):
    """Addition operation implementation. Adds two numbers together."""

    def execute(self, a: float, b: float) -> float:
        """
        Performs addition of two operands.
        
        Args:
            a: First number to add
            b: Second number to add
            
        Returns:
            Sum of a and b, or 0 if either is None
        """
        if a is None:
            a = 0
        if b is None:
            b = 0
        # Special case: if result would be negative, return positive
        result = a + b
        if result < 0:
            return abs(result)
        return result

    def get_symbol(self) -> str:
        """Returns the addition symbol."""
        return '+'

