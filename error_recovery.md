
# Error Handling

An LLM only sees what a tool returns. If a tool doesn't report an error, the LLM assumes that everything worked –
and tells the user so.

## Where to start?

| Pattern | Problem | Implementation |
|--------|---------|-----------|
| **meaningful errors** | the LLM guesses what went wrong | `raise ToolError("...")` with a hint on how to do it right |
| **Retry** | an external service is briefly unavailable | try again, in the client or in the tool |
| **Timeout** | a tool hangs and blocks the agent loop | `@mcp.tool(timeout=5.0)` |
| **Idempotency** | a retry creates an incident twice | a second identical call changes nothing |
| **Fallback** | a service is down permanently | alternative route, e.g. ticket by e-mail instead of via API |

```python
from fastmcp.exceptions import ToolError

if incident_id not in incidents:
    raise ToolError(
        f"Incident {incident_id} does not exist. "
        "Call list_incidents to find valid incident numbers."
    )
```

With `FastMCP("Incidents", mask_error_details=True)` the LLM only sees messages from `ToolError`.
Other exceptions (with stack traces, paths, passwords …) are hidden.

----

## Exercise: A tool that fails silently

The server [code/silent_failure_mcp.py](code/silent_failure_mcp.py) contains two incidents.

1. Connect it to an LLM.
2. Ask the LLM: *"Close incident 7, the problem is solved."*
3. What does the LLM answer? What is really in `list_incidents`?
4. Find the cause in the code.
5. Replace the silent failure with a `ToolError` with a helpful message.
6. Repeat the prompt. Does the LLM now call `list_incidents` on its own?
7. Make `close_incident` idempotent: an incident that is already closed is not changed again.

Solution: [code/error_recovery_mcp.py](code/error_recovery_mcp.py)
