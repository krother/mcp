"""
Tests for the incident server.

    uv add --dev pytest pytest-asyncio
    uv run pytest
"""
import pytest
import pytest_asyncio
from fastmcp import Client

from incident_mcp import incidents, mcp

pytestmark = pytest.mark.asyncio

PRINTER = {"title": "printer on fire", "description": "smoke", "location": "B2-3"}


@pytest_asyncio.fixture
async def client():
    incidents.clear()
    async with Client(mcp) as c:
        yield c


async def test_tools_are_listed(client):
    tools = {t.name for t in await client.list_tools()}
    assert tools == {"create_incident", "list_incidents", "close_incident"}


async def test_tools_have_descriptions(client):
    for tool in await client.list_tools():
        assert tool.description, f"{tool.name} has no docstring"


async def test_create_incident(client):
    result = await client.call_tool("create_incident", PRINTER)
    assert result.data["id"] == 1
    assert result.data["status"] == "open"


async def test_close_incident(client):
    await client.call_tool("create_incident", PRINTER)
    await client.call_tool("close_incident", {"incident_id": 1, "resolution": "water"})
    result = await client.call_tool("list_incidents", {"status": "open"})
    assert result.data == []


async def test_close_unknown_incident(client):
    result = await client.call_tool(
        "close_incident", {"incident_id": 99, "resolution": "?"}, raise_on_error=False
    )
    assert result.is_error
