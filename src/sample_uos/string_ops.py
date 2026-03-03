"""String Unit Operations."""

from pydantic import BaseModel, Field

from uoroboros import unit_operation, uoroboros_type


@uoroboros_type()
class ConcatInput(BaseModel):
    """Input for string concatenation."""

    a: str = Field(description="First string")
    b: str = Field(description="Second string")


@uoroboros_type()
class ConcatOutput(BaseModel):
    """Output for concatenation."""

    result: str = Field(description="Concatenated string")


@unit_operation(description="Concatenate two strings")
def concat(input: ConcatInput) -> ConcatOutput:
    """Concatenate two strings together."""
    return ConcatOutput(result=input.a + input.b)


@uoroboros_type()
class UppercaseInput(BaseModel):
    """Input for uppercase conversion."""

    text: str = Field(description="Text to convert")


@uoroboros_type()
class UppercaseOutput(BaseModel):
    """Output for uppercase conversion."""

    result: str = Field(description="Uppercased text")


@unit_operation(description="Convert text to uppercase")
def uppercase(input: UppercaseInput) -> UppercaseOutput:
    """Convert text to uppercase."""
    return UppercaseOutput(result=input.text.upper())
