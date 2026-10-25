
# Your first MCP Server

## Exercise: Fibonacci MCP

In this exercise you build a simple MCP server that can calculate Fibonacci numbers.

### Step 1: Create a project

```bash
python -m pip install uv
mkdir mcp
cd mcp
uv init
uv add fastmcp
```

The last command should fail. Read the error message to find out why.
Find a suitable solution.

Check the result with:

```bash
uv run fastmcp version
```

### Step 2: Write a server

Create a file `fibonacci_mcp.py`:

```python
from fastmcp import FastMCP

mcp = FastMCP("Fibonacci")


@mcp.tool
def hello(name: str) -> str:
    return f"hello {name}"


if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=8000)
```

### Step 3: Add a tool

Add your function `fibonacci()` from the previous exercise.
Decorate it with `@mcp.tool` and add type hints.

### Step 4: Start the server

```bash
uv run fibonacci_mcp.py
```

Open [http://localhost:8000/mcp](http://localhost:8000/mcp) in the browser.
Unlike with FastAPI, you should see an error message – the server doesn't speak HTML, only JSON-RPC.

Stop the server with `Ctrl+C`. Start it again, this time with the terminal command `fastmcp` and auto-reload:

```bash
uv run fastmcp run fibonacci_mcp.py:mcp --transport http --port 8000 --reload
```

### Step 5: Call the server from Python

Create `client.py`:

```python
import asyncio
from pprint import pprint

from fastmcp import Client

client = Client("http://localhost:8000/mcp")


async def main():
    async with client:
        tools = await client.list_tools()
        pprint([t.name for t in tools])

        result = await client.call_tool("fibonacci", {"n": 10})
        pprint(result.data)


asyncio.run(main())
```

Run it in a second terminal:

```bash
uv run client.py
```

Alternatively, you can use the CLI:

```bash
uv run fastmcp list http://localhost:8000/mcp
uv run fastmcp call http://localhost:8000/mcp fibonacci n=10
```

### Step 6: Add a UI with Prefab

Install the extra:

```bash
uv add "fastmcp[apps]"
```

Add a tool that returns a visual card:

```python
from prefab_ui.app import PrefabApp
from prefab_ui.components import Badge, Column, Heading, Row, Text


@mcp.tool(app=True)
def fibonacci_card(n: int) -> PrefabApp:
    """Shows a Fibonacci number as a visual card."""
    with Column(gap=4, css_class="p-6") as view:
        Heading(f"Fibonacci #{n}")
        with Row(gap=2, align="center"):
            Text("Result")
            Badge(str(fibonacci(n)), variant="success")
    return PrefabApp(view=view)
```

Stop the server and start it in dev mode:

```bash
uv run fastmcp dev apps fibonacci_mcp.py
```

A browser window opens. Select `fibonacci_card` and run it.

### Sample solution:

Solution: [code/hello_mcp.py](code/hello_mcp.py), [code/fibonacci_mcp.py](code/fibonacci_mcp.py), [code/client.py](code/client.py)
