"""Math Unit Operations."""

from pydantic import BaseModel, Field

from uostore import Error, unit_operation


class AddInput(BaseModel):
    """Input for addition."""

    a: float = Field(description="First number")
    b: float = Field(description="Second number")


class AddOutput(BaseModel):
    """Output for addition."""

    result: float = Field(description="Sum of a and b")


@unit_operation(description="Add two numbers together")
def add(input: AddInput) -> AddOutput | Error:
    """Compute the sum of two numbers."""
    return AddOutput(result=input.a + input.b)


class MultiplyInput(BaseModel):
    """Input for multiplication."""

    a: float = Field(description="First number")
    b: float = Field(description="Second number")


class MultiplyOutput(BaseModel):
    """Output for multiplication."""

    result: float = Field(description="Product of a and b")


@unit_operation(description="Multiply two numbers")
def multiply(input: MultiplyInput) -> MultiplyOutput | Error:
    """Compute the product of two numbers."""
    return MultiplyOutput(result=input.a * input.b)


class DivideInput(BaseModel):
    """Input for division."""

    numerator: float = Field(description="Number to divide")
    denominator: float = Field(description="Number to divide by")


class DivideOutput(BaseModel):
    """Output for division."""

    result: float = Field(description="Result of division")


@unit_operation(
    description="Divide two numbers",
    error_codes=["DIVISION_BY_ZERO"],
)
def divide(input: DivideInput) -> DivideOutput | Error:
    """Divide numerator by denominator. Returns Error if denominator is zero."""
    if input.denominator == 0:
        return Error(code="DIVISION_BY_ZERO", message="Cannot divide by zero")
    return DivideOutput(result=input.numerator / input.denominator)


# === Advanced UOs for comprehensive error handling demonstration ===


class ValidateInput(BaseModel):
    """Input for validation UO."""

    value: float = Field(description="Value to validate")
    min_value: float = Field(default=0, description="Minimum allowed value")
    max_value: float = Field(default=100, description="Maximum allowed value")


class ValidateOutput(BaseModel):
    """Output for validation UO."""

    validated_value: float = Field(description="The validated value")
    is_clamped: bool = Field(description="Whether value was clamped to range")


@unit_operation(
    description="Validate and clamp a value to a range",
    error_codes=["INVALID_INPUT", "RANGE_ERROR", "OVERFLOW"],
)
def validate_range(input: ValidateInput) -> ValidateOutput | Error:
    """Validate value is within range. Multiple error codes for different failures."""
    import math

    # Check for NaN (truly invalid)
    if math.isnan(input.value):
        return Error(
            code="INVALID_INPUT",
            message="Value must be a finite number",
            details={"received": str(input.value)},
        )

    # Check for infinity (overflow)
    if math.isinf(input.value):
        return Error(
            code="OVERFLOW",
            message="Value is infinite (overflow)",
            details={"value": str(input.value)},
        )

    if input.min_value > input.max_value:
        return Error(
            code="RANGE_ERROR",
            message="min_value cannot be greater than max_value",
            details={"min": input.min_value, "max": input.max_value},
        )

    if abs(input.value) > 1e300:
        return Error(
            code="OVERFLOW",
            message="Value exceeds safe range",
            details={"value": input.value},
        )

    # Clamp to range
    clamped = max(input.min_value, min(input.max_value, input.value))
    return ValidateOutput(
        validated_value=clamped,
        is_clamped=(clamped != input.value),
    )


class ErrorInfoInput(BaseModel):
    """Input for error logging UO."""

    error_code: str = Field(description="The error code that occurred")
    error_message: str = Field(description="The error message")
    original_value: float = Field(default=0, description="The value that caused error")


class ErrorInfoOutput(BaseModel):
    """Output for error logging UO."""

    logged: bool = Field(description="Whether error was logged")
    fallback_value: float = Field(description="Fallback value to use")


@unit_operation(description="Log an error and provide fallback value")
def log_error(input: ErrorInfoInput) -> ErrorInfoOutput | Error:
    """Log error info and return a safe fallback value."""
    print(f"[ERROR HANDLER] Code: {input.error_code}, Message: {input.error_message}")
    return ErrorInfoOutput(logged=True, fallback_value=0.0)


class EmergencyInput(BaseModel):
    """Input for emergency stop."""

    reason: str = Field(default="Unknown", description="Reason for emergency stop")


class EmergencyOutput(BaseModel):
    """Output for emergency stop."""

    halted: bool = Field(description="System halted")


@unit_operation(description="Emergency stop - halt all operations")
def emergency_stop(input: EmergencyInput) -> EmergencyOutput | Error:
    """Emergency stop handler. Always succeeds."""
    print(f"[EMERGENCY STOP] Reason: {input.reason}")
    return EmergencyOutput(halted=True)
