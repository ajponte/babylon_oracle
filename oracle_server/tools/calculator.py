"""
Calculator tool for demonstration purposes.
"""


def calculate(expression):
    """Calculate a mathematical expression."""
    try:
        # WARNING: eval is not safe and should not be used in production
        return f"The result of {expression} is {eval(expression)}."  # pylint: disable=eval-used
    except Exception as e:
        return f"Error calculating expression: {e}"
