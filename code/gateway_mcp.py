"""
Combines several MCP servers into one.
"""
from fastmcp import FastMCP

from full_mcp import mcp as fibonacci_mcp
from incident_mcp import mcp as incident_mcp


gateway = FastMCP("Gateway")
gateway.mount(incident_mcp, namespace="incidents")
gateway.mount(fibonacci_mcp, namespace="fibonacci")


if __name__ == "__main__":
    gateway.run(transport="http", host="127.0.0.1", port=8000)
