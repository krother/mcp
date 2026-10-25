import sys
from datetime import datetime
from typing import Annotated, Literal

from fastmcp import FastMCP
from pydantic import BaseModel, Field, field_validator

mcp = FastMCP(
    "Incidents",
    instructions="Use this server to record, list and close IT incidents.",
)

incidents: dict[int, dict] = {}


class Incident(BaseModel):
    """An IT incident reported by a colleague."""

    title: str = Field(
        min_length=5, max_length=80, description="short summary, e.g. 'printer on fire'"
    )
    description: str = Field(description="what happened, in the words of the reporter")
    category: Literal["hardware", "software", "network", "security", "other"]
    severity: int = Field(ge=1, le=5, description="1 = cosmetic, 5 = business stopped")
    affected_users: int = Field(default=1, ge=1, le=10_000)
    location: str = Field(description="building and floor, e.g. 'B2-3'")

    @field_validator("location")
    @classmethod
    def check_location(cls, value: str) -> str:
        """Locations have the format <building>-<floor>, e.g. B2-3."""
        building, _, floor = value.partition("-")
        if not building or not floor.isdigit():
            raise ValueError("location must look like 'B2-3' (building-floor)")
        return value.upper()


@mcp.tool
def create_incident(incident: Incident) -> dict:
    """Records a new incident and returns it with its number."""
    incident_id = len(incidents) + 1
    incidents[incident_id] = {
        "id": incident_id,
        **incident.model_dump(),
        "status": "open",
        "created": datetime.now().isoformat(timespec="seconds"),
    }
    # pydantic models are easy to print or convert to JSON
    print(incident.model_dump(), file=sys.stderr)
    return incidents[incident_id]


@mcp.tool
def list_incidents(status: Literal["open", "closed"] = "open") -> list[dict]:
    """Lists all incidents with the given status."""
    return [i for i in incidents.values() if i["status"] == status]



@mcp.tool
def close_incident(
    incident_id: Annotated[int, Field(ge=1, description="number of the incident")],
    resolution: Annotated[str, Field(min_length=10, description="what was done to solve it")],
) -> dict:
    """Closes an incident."""
    incident = incidents[incident_id]
    incident["status"] = "closed"
    incident["resolution"] = resolution
    return incident


@mcp.resource("incident://{incident_id}")
def get_incident(incident_id: int) -> dict:
    """All details of a single incident."""
    return incidents[incident_id]


@mcp.prompt
def report_incident(text: str) -> str:
    """Turns a free-text message into a recorded incident."""
    return (
        "A colleague sent the following message:\n\n"
        f"{text}\n\n"
        "Extract title, description and location. "
        "Record the incident with the create_incident tool. "
        "Then confirm the incident number to the colleague."
    )


if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=8000)
