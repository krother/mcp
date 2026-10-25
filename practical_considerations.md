
# Practical Considerations

To conclude, we take another look at software engineering: what does an MCP service need to work in everyday use?

## Exercise 1: Automated tests

A FastMCP server can be tested without a network and without an LLM by connecting the `Client` directly to the server object:

```bash
uv add --dev pytest pytest-asyncio
```

```python
import pytest
import pytest_asyncio
from fastmcp import Client

from incident_mcp import incidents, mcp

pytestmark = pytest.mark.asyncio


@pytest_asyncio.fixture
async def client():
    incidents.clear()
    async with Client(mcp) as c:
        yield c


async def test_create_incident(client):
    result = await client.call_tool(
        "create_incident",
        {"title": "printer on fire", "description": "smoke", "location": "B2-3"},
    )
    assert result.data["status"] == "open"
```

Run the test.

```bash
uv run pytest
```

----

## Discussion

1. How do I know that my LLM application **works**?
2. How do I know that it **does the right thing**?
3. How will my service **change in the future** – new models, new clients, new tools?
