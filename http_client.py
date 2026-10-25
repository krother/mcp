import asyncio
from fastmcp import Client
from pprint import pprint

client = Client("http://localhost:8000/mcp")

async def call_tool(name: str):
    async with client:
        result = await client.call_tool("greet", {"name": name})
        pprint(result.data)
        

asyncio.run(call_tool("Kristian"))
