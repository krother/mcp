from fastmcp import FastMCP
from fastmcp.exceptions import ToolError

mcp = FastMCP("Incidents", mask_error_details=True)

incidents: dict[int, dict] = {
    1: {"id": 1, "title": "printer on fire", "status": "open"},
    2: {"id": 2, "title": "VPN slow", "status": "open"},
}


@mcp.tool
def list_incidents() -> list[dict]:
    """Lists all incidents."""
    return list(incidents.values())


@mcp.tool(timeout=5.0)
def close_incident(incident_id: int, resolution: str) -> dict:
    """Closes an incident. Closing an already closed incident changes nothing."""
    if incident_id not in incidents:
        raise ToolError(
            f"Incident {incident_id} does not exist. "
            "Call list_incidents to find valid incident numbers."
        )
    incident = incidents[incident_id]
    if incident["status"] == "closed":
        return incident  # idempotent: a retry does no harm
    incident["status"] = "closed"
    incident["resolution"] = resolution
    return incident


if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=8000)
