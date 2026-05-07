"""Pipeline Unit Operations with compatible schemas for testing complex flows.

All UOs in this module use the same schema pattern:
- Input: {value: float}
- Output: {value: float}

This allows chaining: A -> B -> C -> D with data flowing through.
"""

from pydantic import BaseModel, Field

from uoroboros import OutputCondition, unit_operation, uoroboros_type


@uoroboros_type()
class ValueInput(BaseModel):
    """Standard input for pipeline UOs."""

    value: float = Field(description="The value to process")


@uoroboros_type()
class ValueOutput(BaseModel):
    """Standard output for pipeline UOs."""

    value: float = Field(description="The processed value")


@uoroboros_type()
class ZeroError(BaseModel):
    """Error when value is zero."""

    pass


@uoroboros_type()
class NegativeError(BaseModel):
    """Error when value is negative."""

    pass


@uoroboros_type()
class TooLargeError(BaseModel):
    """Error when value exceeds 1000."""

    pass


@uoroboros_type()
class OverflowValueError(BaseModel):
    """Error when squared result exceeds 1e6."""

    pass


@unit_operation(
    description="Validate that value is positive",
    tags=["kind:computational", "kind:validation"],
    outputs={
        ZeroError: OutputCondition(
            condition="error",
            condition_code="ZERO",
            condition_message="Value is zero",
        ),
        NegativeError: OutputCondition(
            condition="error",
            condition_code="NEGATIVE",
            condition_message="Value is negative",
        ),
        TooLargeError: OutputCondition(
            condition="error",
            condition_code="TOO_LARGE",
            condition_message="Value exceeds 1000",
        ),
    },
)
def check_positive(
    input: ValueInput,
) -> ValueOutput | ZeroError | NegativeError | TooLargeError:
    """Check if value is positive. Multiple error codes for different cases."""
    if input.value == 0:
        return ZeroError()
    if input.value < 0:
        return NegativeError()
    if input.value > 1000:
        return TooLargeError()
    return ValueOutput(value=input.value)


@unit_operation(description="Double the value", tags=["kind:computational"])
def double_value(input: ValueInput) -> ValueOutput:
    """Multiply the value by 2."""
    return ValueOutput(value=input.value * 2)


@unit_operation(description="Add 10 to the value", tags=["kind:computational"])
def add_ten(input: ValueInput) -> ValueOutput:
    """Add 10 to the value."""
    return ValueOutput(value=input.value + 10)


@unit_operation(
    description="Square the value",
    tags=["kind:computational"],
    outputs={
        OverflowValueError: OutputCondition(
            condition="error",
            condition_code="OVERFLOW",
            condition_message="Result exceeds 1e6",
        ),
    },
)
def square_value(input: ValueInput) -> ValueOutput | OverflowValueError:
    """Square the value. Returns OVERFLOW if result > 1e6."""
    result = input.value**2
    if result > 1e6:
        return OverflowValueError()
    return ValueOutput(value=result)


@unit_operation(description="Negate the value", tags=["kind:computational"])
def negate(input: ValueInput) -> ValueOutput:
    """Return the negative of the value."""
    return ValueOutput(value=-input.value)


@unit_operation(description="Return absolute value", tags=["kind:computational"])
def absolute(input: ValueInput) -> ValueOutput:
    """Return absolute value."""
    return ValueOutput(value=abs(input.value))


@unit_operation(description="Identity - pass through unchanged", tags=["kind:utility"])
def identity(input: ValueInput) -> ValueOutput:
    """Pass the value through unchanged. Useful as recovery/terminal block."""
    return ValueOutput(value=input.value)


@unit_operation(description="Set value to zero (recovery)", tags=["kind:utility"])
def zero_recovery(input: ValueInput) -> ValueOutput:
    """Recovery block that returns zero regardless of input."""
    return ValueOutput(value=0.0)


@unit_operation(
    description="Set value to default -1 (error marker)",
    tags=["kind:utility"],
)
def error_marker(input: ValueInput) -> ValueOutput:
    """Mark that an error occurred by returning -1."""
    return ValueOutput(value=-1.0)
