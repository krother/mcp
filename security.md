
# Data Protection and Security

An MCP server gives an LLM power to perform real-world actions. This also means it can cause damage.

## Lethal Trifecta

It becomes dangerous when a system has three properties at the same time

| Property | Example in the incident server |
|-------------|-----------------------------|
| **access to private data** | incidents with names, locations, password hints |
| **exposure to untrusted content** | the description of an incident comes from anyone |
| **a way out** | a tool that sends e-mails or fetches URLs |

An attacker writes instructions into an incident – the LLM reads them and sends the data out by e-mail.
**Remove at least one of the three properties.**

### Sources:

- [Linux Magazin](https://www.cusy.io/de/blog/securing-llm-agents.html)
- [Simon Willison](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/)


## Attacks

| Attack | Description |
|---------|-------------|
| **direct prompt injection** | the user themselves writes *"Ignore all rules and …"* |
| **indirect prompt injection** | instructions are hidden in data the LLM reads: incidents, web pages, e-mails |
| **Tool Poisoning** | a third-party MCP server hides instructions in its tool descriptions |
| **Excessive Agency** | a tool can do more than necessary, e.g. `run_sql(query: str)` instead of `list_incidents()` |
| **Confused Deputy** | the LLM acts with the permissions of the server, not with those of the user |

More on this: [OWASP Top 10 for LLM Applications](https://genai.owasp.org/llm-top-10/)

## Data protection

- everything a tool returns ends up in the context – and therefore with the LLM provider
- only return personal data when it is needed
- consider local models (Ollama) for sensitive data
- logs contain tool arguments – they are personal data, too

## Least Privilege

- **read-only tools** wherever possible
- **restricted credentials**: the server only gets the database permissions it needs
- **tool allowlists**: only offer the tools a client needs (see [Multiple MCP Servers](multiple_servers.md))
- **approvals** for everything that cannot be undone (see [Human-in-the-Loop](langgraph_workflows.md))

----

## Exercise: Audit log

Every tool call should be traceable: who, when, what, with which result.
A **middleware** sees every call before it reaches the tool:

```python
import json
import logging

from fastmcp.server.middleware import Middleware

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
        result = await call_next(context)
        audit.info(json.dumps(entry))
        return result


mcp.add_middleware(AuditMiddleware())
```

1. Add the middleware to your incident server.
2. Let an LLM create and close a few incidents. Look at `audit.log`.
3. Also log failed calls (`try` / `except` / `finally`).
4. Which fields in the log are personal data? How long are you allowed to keep them?

Solution: [code/audit_mcp.py](code/audit_mcp.py)
