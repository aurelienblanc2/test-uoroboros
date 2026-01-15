"""Pipeline Unit Operations with compatible schemas for testing complex flows.

All UOs in this module use the same schema pattern:
- Input: {value: float}
- Output: {value: float}

This allows chaining: A -> B -> C -> D with data flowing through.
"""

from pydantic import BaseModel, Field

from uostore import Error, unit_operation


class ValueInput(BaseModel):
    """Standard input for pipeline UOs."""

    value: float = Field(description="The value to process")


class ValueOutput(BaseModel):
    """Standard output for pipeline UOs."""

    value: float = Field(description="The processed value")


@unit_operation(
    description="Validate that value is positive",
    error_codes=["ZERO", "NEGATIVE", "TOO_LARGE"],
)
def check_positive(input: ValueInput) -> ValueOutput | Error:
    """Check if value is positive. Multiple error codes for different cases."""
    if input.value == 0:
        return Error(code="ZERO", message="Value is zero")
    if input.value < 0:
        return Error(code="NEGATIVE", message="Value is negative")
    if input.value > 1000:
        return Error(code="TOO_LARGE", message="Value exceeds 1000")
    return ValueOutput(value=input.value)


@unit_operation(description="Double the value")
def double_value(input: ValueInput) -> ValueOutput | Error:
    """Multiply the value by 2."""
    return ValueOutput(value=input.value * 2)


@unit_operation(description="Add 10 to the value")
def add_ten(input: ValueInput) -> ValueOutput | Error:
    """Add 10 to the value."""
    return ValueOutput(value=input.value + 10)


@unit_operation(description="Square the value", error_codes=["OVERFLOW"])
def square_value(input: ValueInput) -> ValueOutput | Error:
    """Square the value. Returns OVERFLOW if result > 1e6."""
    result = input.value ** 2
    if result > 1e6:
        return Error(code="OVERFLOW", message=f"Result {result} exceeds 1e6")
    return ValueOutput(value=result)


@unit_operation(description="Negate the value")
def negate(input: ValueInput) -> ValueOutput | Error:
    """Return the negative of the value."""
    return ValueOutput(value=-input.value)


@unit_operation(description="Return absolute value")
def absolute(input: ValueInput) -> ValueOutput | Error:
    """Return absolute value."""
    return ValueOutput(value=abs(input.value))


@unit_operation(description="Identity - pass through unchanged")
def identity(input: ValueInput) -> ValueOutput | Error:
    """Pass the value through unchanged. Useful as recovery/terminal block."""
    return ValueOutput(value=input.value)


@unit_operation(description="Set value to zero (recovery)")
def zero_recovery(input: ValueInput) -> ValueOutput | Error:
    """Recovery block that returns zero regardless of input."""
    return ValueOutput(value=0.0)


@unit_operation(description="Set value to default -1 (error marker)")
def error_marker(input: ValueInput) -> ValueOutput | Error:
    """Mark that an error occurred by returning -1."""
    return ValueOutput(value=-1.0)
