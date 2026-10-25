
# Validation with Pydantic

A parameter like `data: str` tells the LLM almost nothing. With **Pydantic** you describe exactly which values are allowed.
FastMCP translates the model into a JSON schema for the LLM and **checks every call** before your function runs.

----

## Example: A Pydantic model as a tool parameter

```python
from typing import Literal

from pydantic import BaseModel, Field, field_validator


class Incident(BaseModel):
    """An IT incident reported by a colleague."""

    title: str = Field(min_length=5, max_length=80, description="short summary")
    description: str = Field(description="what happened, in the words of the reporter")
    category: Literal["hardware", "software", "network", "security", "other"]
    severity: int = Field(ge=1, le=5, description="1 = cosmetic, 5 = business stopped")
    affected_users: int = Field(default=1, ge=1, le=10_000)

    @field_validator("location")
    @classmethod
    def check_location(cls, value: str) -> str:
        """Locations have the format <building>-<floor>, e.g. B2-3."""
        building, _, floor = value.partition("-")
        if not building or not floor.isdigit():
            raise ValueError("location must look like 'B2-3' (building-floor)")
        return value.upper()

@mcp.tool
def create_incident(incident: Incident) -> dict:
    ...
```

| Tool | Effect |
|----------|---------|
| `Field(description=...)` | text for the LLM |
| `Field(ge=1, le=5)` | value range for numbers |
| `Field(min_length=5, max_length=80)` | length of strings |
| `Literal["a", "b"]` | allowed values (becomes `enum` in the JSON-RPC schema) |
| `@field_validator` | custom validation function |

----

## Exercise 1: Look at the schema

Start [code/incident_mcp.py](code/incident_mcp.py).
Look at the tool schema of `create_incident` in [code/client.py](code/client.py).
Add the following lines there:

```python
for t in tools:
    pprint(t.input_schema)
```

Find the lowest and highest allowed values for `enum`, `minimum` and `maximum` in the JSON-RPC output.

## Exercise 2: Invalid calls

Call the tool from `client.py` with invalid values, e.g. `severity=9` or `location="kitchen"`.
What does the error message look like? Who gets to see it?

## Exercise 3: Create incidents

Connect an LLM to the MCP service and let it create three different incidents. Observe what arrives in `data`.

Try to send invalid values. How does the LLM react to an error message from the validator? Does it correct itself?

**Tip:** Small models like `qwen3:0.6b` make more mistakes.
