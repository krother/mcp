

## Tools

Tools are the core building blocks that allow your LLM to interact with external systems, execute code and access data that is not in its training data. In FastMCP, tools are Python functions that are exposed to LLMs via the MCP protocol. Tools in FastMCP turn ordinary Python functions into capabilities that LLMs can call during a conversation. When an LLM decides to use a tool:

1. It sends a request with parameters based on the tool's schema.
2. FastMCP validates these parameters against your function's signature.
3. Your function is executed with the validated inputs.
4. The result is returned to the LLM, which can use it in its response.

This allows LLMs to perform tasks such as querying databases, calling APIs, doing calculations or accessing files – extending their capabilities beyond what is in their training data.

## Resources

Resources represent data or files that an MCP client can read. Resource templates extend this concept by allowing clients to request dynamically generated resources, depending on parameters in the URI.

FastMCP simplifies defining static and dynamic resources, primarily with the decorator @mcp.resource.

## Prompts

Prompts are reusable message templates that help LLMs generate structured, purposeful responses. FastMCP simplifies defining these templates, primarily with the decorator @mcp.prompt.

What are prompts?
Prompts provide parameterized message templates for LLMs. When a client requests a prompt:

1. FastMCP finds the matching prompt definition.
2. If it has parameters, they are validated against your function signature.
3. Your function is executed with the validated inputs.
4. The generated message(s) are returned to the LLM to guide its response.

This lets you define consistent, reusable templates that LLMs can use across different clients and contexts.
