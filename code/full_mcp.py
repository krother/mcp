from typing import Annotated

from fastmcp import FastMCP

mcp = FastMCP(
    "Fibonacci",
    instructions="Use this server for anything related to Fibonacci numbers.",
)


@mcp.tool
def fibonacci(
    n: Annotated[int, "position in the Fibonacci series, starting at 0"],
) -> int:
    """Calculates the n-th number of the Fibonacci series."""
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


@mcp.resource("info://about")
def about() -> str:
    """Background information on the Fibonacci series."""
    return (
        "The Fibonacci series starts with 0, 1. "
        "Every further number is the sum of the two previous ones. "
        "It was described by Leonardo of Pisa in 1202."
    )


@mcp.resource("fibonacci://{n}")
def fibonacci_resource(n: int) -> dict:
    """The n-th Fibonacci number with its neighbours."""
    return {
        "n": n,
        "previous": fibonacci(n - 1) if n > 0 else None,
        "value": fibonacci(n),
        "next": fibonacci(n + 1),
    }


@mcp.prompt
def explain_number(n: int) -> str:
    """Asks the LLM to explain a Fibonacci number to a child."""
    return (
        f"Calculate the Fibonacci number at position {n} using the tools. "
        "Then explain to a 10-year-old how it was calculated."
    )


if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=8000)
