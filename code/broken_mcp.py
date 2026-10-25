"""
This server contains bugs.
Connect it to an MCP client via stdio and fix them.
"""
from fastmcp import FastMCP

mcp = FastMCP("Fibonacci")


@mcp.tool
def fibonacci(n):
    """Calculates the n-th number of the Fibonacci series."""
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


if __name__ == "__main__":
    print("starting Fibonacci server", flush=True)
    mcp.run()
