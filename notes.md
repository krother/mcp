
## TODO in class


## MCPInspector

https://github.com/modelcontextprotocol/inspector

npx @modelcontextprotocol/inspector

## Apps UI

- uv add fastmcp[apps]
- add imports + app example
- restart
- add pprint to client
- uv run fastmcp dev apps minimal_mcp.py

### InteractiveTools

server prepares it in one go, done
dashboards

Prefab components: https://prefab.prefect.io/docs/welcome
go to Reference for examples

### FastMCPApp

UI calls the server back

separates UI stuff from entry points cleanly
forms

## Day 2
- fastmcp[tasks]


## Error Handling

from fastmcp.exceptions import ToolError
        raise ToolError("Division by zero is not allowed.")
from fastmcp.exceptions import ResourceError

security: mcp = FastMCP(name="SecureServer", mask_error_details=True)

### stdout: print corrupts stdout

print("starting server", file=sys.stderr)

## Resources

@mcp.resource(
    uri="data://app-status",      # Explicit URI (required)
    name="ApplicationStatus",     # Custom name
    description="Provides the current status of the application.", # Custom description
    mime_type="application/json", # Explicit MIME type
    tags={"monitoring", "status"}, # Categorization tags
    meta={"version": "2.1", "team": "infrastructure"}  # Custom metadata
)

## Prompts

Examples: review, write a reply to a customer

Roles and messages: https://gofastmcp.com/servers/prompts#promptresult

## Other

- auth/OAuth2
- middleware
- pagination
- @mcp.tool(timeout=30.0)
- Context: https://gofastmcp.com/servers/context
- Providers: https://gofastmcp.com/servers/providers/overview
- Skills: https://gofastmcp.com/servers/providers/skills
