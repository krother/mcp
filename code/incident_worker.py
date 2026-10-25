"""
Incident server with a long-running background task.

    uv add fastmcp-tasks
"""
import asyncio
from collections import Counter

from fastmcp import Context
from fastmcp_tasks import TasksExtension

from incident_mcp import incidents, mcp

mcp.add_extension(TasksExtension())


@mcp.tool(task=True)
async def generate_report(ctx: Context) -> dict:
    """Analyzes all incidents and creates a report. Takes a while."""
    total = len(incidents)
    for i, incident in enumerate(incidents.values(), start=1):
        await asyncio.sleep(1)  # pretend to do something expensive
        await ctx.report_progress(i, total, f"analyzed incident #{incident['id']}")
    return {
        "total": total,
        "by_status": Counter(i["status"] for i in incidents.values()),
        "by_location": Counter(i["location"] for i in incidents.values()),
    }


if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=8000)
