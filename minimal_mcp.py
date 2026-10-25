from fastmcp import FastMCP
from prefab_ui.app import PrefabApp
from prefab_ui.components import Column, Heading, Text, Badge, Row
from fastmcp import Context, FastMCP
from mcp.server.request_state import RequestStateSecurity
from mcp.types import ElicitRequest, ElicitRequestFormParams, InputRequiredResult
import os


key = "12345678901234567890123456789012"

mcp = FastMCP("Demo 🚀",
    instructions="...",
    request_state_security=RequestStateSecurity(
        keys=[key.encode()]
    )
)

@mcp.tool
def hello(name: str) -> str:
    """Greets the user"""
    return f"hello {name}"


@mcp.tool(app=True)
def greet(name: str) -> PrefabApp:
    """Greet someone with a visual card."""
    with Column(gap=4, css_class="p-6") as view:
        Heading(f"Hello, {name}!")
        with Row(gap=2, align="center"):
            Text("Status")
            Badge("Greeted", variant="success")

    return PrefabApp(view=view)


@mcp.tool()
async def book_flight(ctx: Context) -> str | InputRequiredResult:
    answers = ctx.input_responses
    if answers is None:
        params = ElicitRequestFormParams(
            message="Where would you like to fly?",
            requested_schema={
                "type": "object",
                "properties": {"destination": {"type": "string"}},
                "required": ["destination"],
            },
        )
        return InputRequiredResult(
            result_type="input_required",
            input_requests={
                "destination": ElicitRequest(
                    method="elicitation/create",
                    params=params,
                )
            },
        )

    response = answers["destination"]
    if response.action != "accept" or response.content is None:
        return "Booking cancelled."

    destination = response.content["destination"]
    return f"Booked a flight to {destination}."

@mcp.tool(description="...")
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool
def fibonacci(n: int) -> int:
    """calculates a number from the Fibonacci Series"""
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a
    # TODO enforce n to be positive
    # TODO: return str because of JSON encoding

if __name__ == "__main__":
    #mcp.run()
    mcp.run(transport="http", host="127.0.0.1", port=8000)