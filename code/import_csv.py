"""
Imports incidents from a CSV file. No LLM involved.

Start incident_worker.py first.
"""
import asyncio
import csv

from fastmcp import Client

client = Client("http://localhost:8000/mcp")


async def main():
    async with client:
        with open("incidents.csv") as f:
            for row in csv.DictReader(f):
                result = await client.call_tool("create_incident", row)
                print(result)


asyncio.run(main())
