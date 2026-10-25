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
