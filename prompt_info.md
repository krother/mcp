
# Feeding the Prompt

The LLM never sees your Python code. It only sees what FastMCP writes into the prompt. In this chapter you place useful instructions in a few places:

- server-wide instructions
- description of each tool
- type hints for each parameter
- description of each parameter

The LLM decides **exclusively based on these texts** whether and how it calls your tool.

----

## Exercise 1: Describe your tools

Start the server and list the tools:

```bash
uv run fastmcp list http://localhost:8000/mcp
```

Write down what is missing.

## Exercise 2: Add server-wide instructions

```python
mcp = FastMCP(
    "Fibonacci",
    instructions="Use this server for anything related to Fibonacci numbers.",
)
```

List the tools again.

## Exercise 3: Add a docstring

```python
@mcp.tool
def fibonacci(n: int) -> int:
    """Calculates the n-th number of the Fibonacci series."""
```

## Exercise 4: Describe parameters with `Annotated`

```python
from typing import Annotated


@mcp.tool
def fibonacci(
    n: Annotated[int, "position in the Fibonacci series, starting at 0"],
) -> int:
    ...
```


## Exercise 5: Describe parameters in the docstring

Add a second tool that returns multiple numbers:

```python
@mcp.tool
def fibonacci_series(start: int, stop: int) -> list[int]:
    """Returns a slice of the Fibonacci series.

    Args:
        start: position of the first number (inclusive)
        stop: position of the last number (exclusive)
    """
    return [fibonacci(i) for i in range(start, stop)]
```

## Exercise 6: View the complete JSON schema

Add to `client.py`:

```python
for t in tools:
    pprint(t.inputSchema)
```

Find your descriptions in the output.

Solution: [code/fibonacci_mcp.py](code/fibonacci_mcp.py)
