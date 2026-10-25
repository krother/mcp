from typing import Annotated

from fastmcp import FastMCP
from prefab_ui.app import PrefabApp
from prefab_ui.components import Badge, Column, Heading, Row, Text

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


@mcp.tool
def fibonacci_series(start: int, stop: int) -> list[int]:
    """Returns a slice of the Fibonacci series.

    Args:
        start: position of the first number (inclusive)
        stop: position of the last number (exclusive)
    """
    return [fibonacci(i) for i in range(start, stop)]


@mcp.tool(app=True)
def fibonacci_card(n: int) -> PrefabApp:
    """Shows a Fibonacci number as a visual card."""
    with Column(gap=4, css_class="p-6") as view:
        Heading(f"Fibonacci #{n}")
        with Row(gap=2, align="center"):
            Text("Result")
            Badge(str(fibonacci(n)), variant="success")
    return PrefabApp(view=view)


if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=8000)
