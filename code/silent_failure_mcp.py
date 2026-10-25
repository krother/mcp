"""
This server has a tool that fails silently.
Ask an LLM to close incident 7 and watch what it reports.
"""
from fastmcp import FastMCP

mcp = FastMCP("Incidents")

# example database
incidents: dict[int, dict] = {
    1: {"id": 1, "title": "printer on fire", "status": "open"},
    2: {"id": 2, "title": "VPN slow", "status": "open"},
}


@mcp.tool
def list_incidents() -> list[dict]:
    """Lists all incidents."""
    return list(incidents.values())


@mcp.tool
def close_incident(incident_id: int, resolution: str) -> str:
    """Closes an incident."""
    try:
        incident = incidents[incident_id]
        incident["status"] = "closed"
        incident["resolution"] = resolution
    except Exception:
        pass
    return "OK"


if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=8000)
