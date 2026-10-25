from fastmcp import FastMCP

mcp = FastMCP("Fibonacci")


@mcp.tool
def hello(name: str) -> str:
    return f"hello {name}"


@mcp.tool
def fibonacci(n: int) -> int:
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=8000)
