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
