"""Math Unit Operations."""

from pydantic import BaseModel, Field

from uoroboros import unit_operation, uoroboros_type


@uoroboros_type()
class AddInput(BaseModel):
    """Input for addition."""

    a: float = Field(description="First number")
    b: float = Field(description="Second number")


@uoroboros_type()
class ResultFloat(BaseModel):
    """Single float"""

    result: float = Field(description="result")


@unit_operation(description="Add two numbers together", tags=["kind:computational"])
def add(input: AddInput) -> ResultFloat:
    """Compute the sum of two numbers."""
    return ResultFloat(result=input.a + input.b)


@uoroboros_type()
class MultiplyInput(BaseModel):
    """Input for multiplication."""

    a: float = Field(description="First number")
    b: float = Field(description="Second number")


@unit_operation(description="Multiply two numbers", tags=["kind:computational"])
def multiply(input: MultiplyInput) -> ResultFloat:
    """Compute the product of two numbers."""
    return ResultFloat(result=input.a * input.b)


@uoroboros_type()
class DivideInput(BaseModel):
    """Input for division."""

    numerator: float = Field(description="Number to divide")
    denominator: float = Field(description="Number to divide by")


@uoroboros_type(
    condition="error", code="DIVISION_BY_ZERO", message="Cannot divide by zero"
)
class DivisionByZeroError(BaseModel):
    """Error when dividing by zero."""

    numerator: float = Field(description="The numerator that was being divided")
    denominator: float = Field(description="The denominator (zero)")


@unit_operation(description="Divide two numbers", tags=["kind:computational"])
def divide(input: DivideInput) -> ResultFloat | DivisionByZeroError:
    """Divide numerator by denominator. Returns Error if denominator is zero."""
    if input.denominator == 0:
        return DivisionByZeroError(
            numerator=input.numerator, denominator=input.denominator
        )
    return ResultFloat(result=input.numerator / input.denominator)


# === Advanced UOs for comprehensive error handling demonstration ===


@uoroboros_type()
class ValidateInput(BaseModel):
    """Input for validation UO."""

    value: float = Field(description="Value to validate")
    min_value: float = Field(default=0, description="Minimum allowed value")
    max_value: float = Field(default=100, description="Maximum allowed value")


@uoroboros_type()
class ValidateOutput(BaseModel):
    """Output for validation UO."""

    validated_value: float = Field(description="The validated value")
    is_clamped: bool = Field(description="Whether value was clamped to range")


@uoroboros_type(
    condition="error", code="INVALID_INPUT", message="Value must be a finite number"
)
class InvalidInputError(BaseModel):
    """Error for invalid input values."""

    received: str = Field(default="", description="The received value")


@uoroboros_type(
    condition="error", code="RANGE_ERROR", message="Range parameters are invalid"
)
class RangeError(BaseModel):
    """Error for invalid range parameters."""

    min: float = Field(description="Min value")
    max: float = Field(description="Max value")


@uoroboros_type(condition="error", code="OVERFLOW", message="Value exceeds safe range")
class OverflowError(BaseModel):
    """Error for overflow values."""

    value: float = Field(description="The overflow value")


@unit_operation(
    description="Validate and clamp a value to a range",
    tags=["kind:computational", "kind:validation"],
)
def validate_range(
    input: ValidateInput,
) -> ValidateOutput | InvalidInputError | RangeError | OverflowError:
    """Validate value is within range. Multiple error codes for different failures."""
    import math

    # Check for NaN (truly invalid)
    if math.isnan(input.value):
        return InvalidInputError(received=str(input.value))

    # Check for infinity (overflow)
    if math.isinf(input.value):
        return OverflowError(value=input.value)

    if input.min_value > input.max_value:
        return RangeError(min=input.min_value, max=input.max_value)

    if abs(input.value) > 1e300:
        return OverflowError(value=input.value)

    # Clamp to range
    clamped = max(input.min_value, min(input.max_value, input.value))
    return ValidateOutput(
        validated_value=clamped,
        is_clamped=(clamped != input.value),
    )


@uoroboros_type()
class ErrorInfoInput(BaseModel):
    """Input for error logging UO."""

    error_code: str = Field(description="The error code that occurred")
    error_message: str = Field(description="The error message")
    original_value: float = Field(default=0, description="The value that caused error")


@uoroboros_type()
class ErrorInfoOutput(BaseModel):
    """Output for error logging UO."""

    logged: bool = Field(description="Whether error was logged")
    fallback_value: float = Field(description="Fallback value to use")


@unit_operation(
    description="Log an error and provide fallback value",
    tags=["kind:utility"],
)
def log_error(input: ErrorInfoInput) -> ErrorInfoOutput:
    """Log error info and return a safe fallback value."""
    print(f"[ERROR HANDLER] Code: {input.error_code}, Message: {input.error_message}")
    return ErrorInfoOutput(logged=True, fallback_value=0.0)


@uoroboros_type()
class EmergencyInput(BaseModel):
    """Input for emergency stop safety action."""

    pass


@uoroboros_type()
class EmergencyOutput(BaseModel):
    """Output for emergency stop."""

    halted: bool = Field(description="System halted")


@unit_operation(
    description="Emergency stop - halt all operations", tags=["kind:utility"]
)
def emergency_stop(input: EmergencyInput) -> EmergencyOutput:
    """Emergency stop handler — performs safety actions.

    Error details (code, message, block) are logged and stored in the
    database by the emergency_stop_fn callback, not by this UO.
    """
    print("[EMERGENCY STOP] Halting all operations")
    return EmergencyOutput(halted=True)


@uoroboros_type()
class EmptyType(BaseModel):
    """Empty"""

    pass


@uoroboros_type()
class MessageType(BaseModel):
    """String for a message."""

    message: str = Field(default="Default message", description="Message string")


@unit_operation(description="Print a message to stdout", tags=["kind:utility"])
def print_message(input: MessageType) -> EmptyType:
    """Print a message to stdout."""
    print(input.message)
    return EmptyType()


@uoroboros_type()
class SumListInput(BaseModel):
    """Input for sum_list UO."""

    values: list[float] = Field(description="List of numbers to sum")


@unit_operation(description="Sum all elements of a list", tags=["kind:computational"])
def sum_list(input: SumListInput) -> ResultFloat:
    """Sum all elements of a list and return the total as a float."""
    return ResultFloat(result=sum(input.values))


@uoroboros_type()
class RandomListInput(BaseModel):
    """Input for random_list UO."""

    min_value: float = Field(description="Minimum value (inclusive)")
    max_value: float = Field(description="Maximum value (exclusive)")
    count: int = Field(description="Number of elements to generate")


@uoroboros_type()
class RandomListOutput(BaseModel):
    """Output for random_list UO."""

    values: list[float] = Field(description="Generated random floats")


@unit_operation(
    description="Generate a list of random floats", tags=["kind:computational"]
)
def random_list(input: RandomListInput) -> RandomListOutput | RangeError:
    """Generate a list of random floats between min and max."""
    import random

    if input.min_value >= input.max_value:
        return RangeError(min=input.min_value, max=input.max_value)
    values = [
        random.uniform(input.min_value, input.max_value) for _ in range(input.count)
    ]
    return RandomListOutput(values=values)


@uoroboros_type(condition="input")
class Entry2(BaseModel):
    """Input for double_entries_test workflow."""

    b_entry_2: AddInput = Field(description="Second entry block input")
