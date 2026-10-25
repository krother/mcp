"""
An existing REST API for the hardware inventory.

    uv add fastapi uvicorn
    uv run uvicorn inventory_api:app --port 8001
"""
from fastapi import FastAPI, HTTPException

app = FastAPI(title="Inventory")

devices = {
    "PR-17": {"id": "PR-17", "type": "printer", "location": "B2-3", "owner": "Facility"},
    "SW-02": {"id": "SW-02", "type": "network switch", "location": "B0-1", "owner": "Network"},
    "NB-88": {"id": "NB-88", "type": "notebook", "location": "remote", "owner": "Alice"},
}


@app.get("/devices", operation_id="list_devices")
def list_devices(location: str | None = None) -> list[dict]:
    """Lists all devices, optionally filtered by location."""
    return [d for d in devices.values() if location in (None, d["location"])]


@app.get("/devices/{device_id}", operation_id="get_device")
def get_device(device_id: str) -> dict:
    """Returns one device by its inventory number."""
    if device_id not in devices:
        raise HTTPException(status_code=404, detail="device not found")
    return devices[device_id]


@app.delete("/devices/{device_id}", operation_id="delete_device")
def delete_device(device_id: str) -> dict:
    """Removes a device from the inventory."""
    return devices.pop(device_id)
