
# MCP as a Backend Worker

An MCP server doesn't need an LLM. Any Python script, pipeline or cron job can call its tools.

## Long-running tasks

Some tools take minutes: generating reports, importing data, training models.
A normal tool call would block for that long.
With **Tasks**, the tool runs in the background:

| Term | Meaning |
|---------|-----------|
| **Task** | a tool call that runs in the background and gets an ID |
| **Progress** | the tool reports intermediate status with `ctx.report_progress()` |
| **Cancellation** | the client cancels a task |

----

## Exercise 1: Create a task


```bash
uv add fastmcp-tasks
```

Add code to the example from the pydantic chapter:


```python
import asyncio

from fastmcp import Context
from fastmcp_tasks import TasksExtension

mcp.add_extension(TasksExtension())


@mcp.tool(task=True)
async def generate_report(ctx: Context) -> dict:
    """Analyzes all incidents and creates a report. Takes a while."""
    total = len(incidents)
    for i, incident in enumerate(incidents.values(), start=1):
        await asyncio.sleep(1)  # pretend to do something expensive
        await ctx.report_progress(i, total, f"analyzed incident #{incident['id']}")
    return {"total": total}
```

Solution: [code/incident_worker.py](code/incident_worker.py)


## Exercise 2: CSV import

Use [code/import_csv.py](code/import_csv.py) to import all rows from [code/incidents.csv](code/incidents.csv) via `create_incident`
and then generate the report.

Add code to generate the report:

```python
from fastmcp_tasks import call_tool_task

...

task = await call_tool_task(client, "generate_report")
status = await task.status()
print(status.status, status.status_message)
report = await task.result()
```

Print the report at the end.

----

### Question

When are tasks the right abstraction, and when is a REST API simpler?
