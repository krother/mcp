from typing import Any

import httpx
from fastmcp import FastMCP

BASE_URL = "https://v6.bvg.transport.rest"

mcp = FastMCP("BVG-Bot")


def find_station(name: str) -> dict[str, Any]:
    """returns the best matching stop for a station name"""
    response = httpx.get(
        f"{BASE_URL}/locations",
        params={
            "query": name,
            "results": 1,
            "stops": "true",
            "addresses": "false",
            "poi": "false",
        },
        timeout=10,
    )
    response.raise_for_status()
    results = response.json()
    if not results:
        raise ValueError(f"Station not found: {name}")
    return results[0]


@mcp.tool
def fahrplan_anfrage(station_from: str, station_to: str) -> list[Any]:
    """
    sends a request to the BVG Transport API, finds two station and
    returns a list of departure times, bus/train lines and destinations
    """
    origin = find_station(station_from)
    destination = find_station(station_to)

    response = httpx.get(
        f"{BASE_URL}/journeys",
        params={"from": origin["id"], "to": destination["id"], "results": 3},
        timeout=10,
    )
    response.raise_for_status()

    journeys = []
    for journey in response.json()["journeys"]:
        legs = []
        for leg in journey["legs"]:
            legs.append(
                {
                    "from": leg["origin"]["name"],
                    "departure": leg["departure"],
                    "line": "Fußweg" if leg.get("walking") else leg["line"]["name"],
                    "direction": leg.get("direction"),
                    "to": leg["destination"]["name"],
                    "arrival": leg["arrival"],
                }
            )
        journeys.append(legs)
    return journeys


if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=8010)
