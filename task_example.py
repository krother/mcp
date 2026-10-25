"""
requires 

   uv add fastmcp-tasks
"""
import asyncio

from fastmcp import FastMCP
from fastmcp_tasks import TasksExtension

mcp = FastMCP("MyServer")
mcp.add_extension(TasksExtension())


@mcp.tool(task=True)
async def slow_computation(duration: int) -> str:
    """Run a long computation."""
    await asyncio.sleep(duration)
    return f"Completed in {duration} seconds"