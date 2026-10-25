
# UI with Prefab

An MCP server can return not only text, but also **user interfaces**.
Clients like Claude display them directly in the chat.
FastMCP uses the component library **Prefab** for this.

```bash
uv add "fastmcp[apps]"
```

There are two variants:

| | Decorator | How it works | Example |
|--|-----------|---------------|----------|
| **App tool** | `@mcp.tool(app=True)` | the server builds the view once and returns it | dashboard, card, table |
| **FastMCPApp** | `@app.ui()` + `@app.tool()` | the view calls tools on the server when clicked | forms, confirmations |

----

## Exercise 1: Load incidents

The following code should load a few example incidents in `incident_mcp.py`.

Add the JSON file [code/incidents.json](code/incidents.json) in the same directory.

```
import json

incidents: dict[int, dict] = {
    i["id"]: i
    for i in json.loads((Path(__file__).parent / "incidents.json").read_text())
}
```

## Exercise 2: A dashboard

Display the incidents as a table:

```python
from prefab_ui.app import PrefabApp
from prefab_ui.components import Column, DataTable, DataTableColumn, Heading, Metric, Row


@mcp.tool(app=True)
def incident_dashboard() -> PrefabApp:
    """Shows all incidents as a table."""
    open_incidents = [i for i in incidents.values() if i["status"] == "open"]
    with Column(gap=4, css_class="p-6") as view:
        Heading("Incidents")
        with Row(gap=4):
            Metric(label="open", value=len(open_incidents))
            Metric(label="total", value=len(incidents))
        DataTable(
            columns=[
                DataTableColumn(key="id", header="#"),
                DataTableColumn(key="title", header="Title", sortable=True),
                DataTableColumn(key="location", header="Location"),
                DataTableColumn(key="status", header="Status"),
            ],
            rows=list(incidents.values()),
            search=True,
        )
    return PrefabApp(view=view)
```

## Exercise 3: Run the example

Start the preview:

```bash
uv run fastmcp dev apps incident_ui.py
```

Select `incident_dashboard`. Sort and search the table.

## Exercise 4: Browse the catalog

Open the [Prefab components](https://prefab.prefect.io/docs/welcome) and pick two components
that would improve the dashboard, e.g. a `Badge` for the severity or a chart.
Add them.

----

## Exercise 5: A form that calls the server

A `FastMCPApp` separates the user interface (`@app.ui`) from the tools the view calls (`@app.tool`).
Input fields with `name="..."` store their value in the state; `{{ title }}` reads it back.

Add the code to the program. The old function `create_incident()` is no longer needed. You can delete it.

```python
from fastmcp import FastMCP, FastMCPApp
from prefab_ui.actions import SetState, ShowToast
from prefab_ui.actions.mcp import CallTool
from prefab_ui.rx import RESULT
from prefab_ui.components import (
    Badge, Button, Card, CardContent, CardFooter, CardHeader, CardTitle,
    Column, DataTable, DataTableColumn, Heading, If, Input, Metric, Row,
    Select, SelectOption, Text, Textarea,
)


app = FastMCPApp("Incident App")


@app.tool()
def create_incident(title: str, location: str, severity: str) -> dict:
    """Records a new incident."""
    incident_id = len(incidents) + 1
    incidents[incident_id] = {
        "id": incident_id,
        "title": title,
        "location": location,
        "severity": int(severity),
        "status": "open",
    }
    return incidents[incident_id]


@app.ui()
def incident_form() -> PrefabApp:
    """Opens a form for reporting an incident."""
    with Column(gap=4, css_class="p-6") as view:
        Heading("Report an incident")
        Input(name="title", placeholder="What happened?", required=True)
        Input(name="location", placeholder="e.g. B2-3", required=True)
        with Select(name="severity", placeholder="Severity"):
            for level in range(1, 6):
                SelectOption(value=str(level), label=str(level))
        Button(
            "Submit",
            on_click=CallTool(
                "create_incident",
                arguments={
                    "title": "{{ title }}",
                    "location": "{{ location }}",
                    "severity": "{{ severity }}",
                },
                on_success=[
                    SetState("created", RESULT),
                    ShowToast("Incident recorded", variant="success"),
                ],
                on_error=ShowToast("{{ $error }}", variant="error"),
            ),
        )
        with If("created"):
            Text("Recorded incident #{{ created.id }}")
    return PrefabApp(view=view, state={"created": None})


mcp.add_provider(app)
```

Restart the server.

Select `incident_form` in the preview, create an incident and then check it in the dashboard.

**Tip:** `Form.from_model(Incident, on_submit=CallTool("create_incident"))` generates a form directly from a Pydantic model.

----

## Exercise 6: Human-in-the-Loop

Before an incident is closed, a human should approve it.

For this, FastMCP comes with a ready-made confirmation dialog, `Approval`.
It provides the tool `request_approval`: the LLM passes a summary, the human clicks **Approve** or **Reject**,
and the decision ends up as a message in the chat.

Add the following code to the server:

```python
from fastmcp.apps.approval import Approval

mcp.add_provider(Approval(title="Close incident?", approve_text="Close", approve_variant="destructive"))
```

Extend the docstring of `close_incident` so that the LLM calls `request_approval` first and only continues after **Close**:

```
    Before calling this tool, call request_approval with a summary of the
    incident and the resolution. Only call close_incident after the user
    has selected Approve.
```

Try it out in Claude.

What happens when you click **Reject**?

----

## Exercise 7: Elicitation

In exercise 6, the LLM still makes the final decision: the approval only ends up as a message in the chat,
and the LLM could call `close_incident` without it.

With **elicitation**, the server asks by itself. On the first call, `close_incident` returns
an `InputRequiredResult` instead of a result. The client shows the question to the human and calls the tool again with the answer.
The LLM cannot skip this step.

Replace `close_incident` with:

```python
from fastmcp import Context
from mcp_types import ElicitRequest, ElicitRequestFormParams, InputRequiredResult


@mcp.tool()
def close_incident(
    incident_id: int, resolution: str, ctx: Context
) -> dict | InputRequiredResult:
    """Closes an incident."""
    incident = incidents[incident_id]
    answers = ctx.input_responses
    if answers is None:
        # first call: ask the user, the client calls the tool again with the answer
        question = ElicitRequest(params=ElicitRequestFormParams(
            message=f"Close incident #{incident_id} '{incident['title']}'?\nResolution: {resolution}",
            requested_schema={
                "type": "object",
                "properties": {"close": {"type": "boolean", "title": "Close incident"}},
                "required": ["close"],
            },
        ))
        return InputRequiredResult(input_requests={"confirm": question})

    answer = answers["confirm"]
    if answer.action != "accept" or not answer.content["close"]:
        return {"status": "cancelled", "incident": incident}
    incident["status"] = "closed"
    incident["resolution"] = resolution
    return incident
```

The reference to `request_approval` in the docstring is no longer needed.

Try it out in Claude: *"Close incident 2, the VPN is working again."*

* What happens if you decline or cancel the dialog?
* Compare with exercise 6: where is the decision enforced in each case?

**Note:** In older versions of the MCP protocol (up to 2025-11-25) you wrote `await ctx.elicit(...)` instead.
Since protocol version 2026-07-28 this no longer works.
