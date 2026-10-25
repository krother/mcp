"""
Incident server with an audit log of every tool call.
"""
import json
import logging

from fastmcp.server.middleware import Middleware

from incident_mcp import mcp

audit = logging.getLogger("audit")
audit.addHandler(logging.FileHandler("audit.log"))
audit.setLevel(logging.INFO)


class AuditMiddleware(Middleware):

    async def on_call_tool(self, context, call_next):
        entry = {
            "time": context.timestamp.isoformat(timespec="seconds"),
            "tool": context.message.name,
            "arguments": context.message.arguments,
        }
        try:
            result = await call_next(context)
            entry["status"] = "ok"
            return result
        except Exception as e:
            entry["status"] = f"error: {e}"
            raise
        finally:
            audit.info(json.dumps(entry))


mcp.add_middleware(AuditMiddleware())


if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=8000)
