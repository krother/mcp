
# MCP Clients

**Goal: In this chapter you connect different LLMs to your MCP server.**

We will try out as many of them as possible:

- MCP Inspector (a Node-based client program, not an LLM)
- Qwen3 0.6, a small local Ollama model
- Claude
- Copilot (not documented here)

----

## Transport modes

| Transport | How it works | Use case |
|-----------|-----|---------|
| **stdio** | the host starts the server as a subprocess and communicates via stdin/stdout | local, single user |
| **Streamable HTTP** | the server runs as a web service under `/mcp` and supports streaming | remote, many clients |
| **SSE** | older HTTP variant | deprecated, replaced by Streamable HTTP |

Switch the transport in your server as needed:

```python
mcp.run()                                       # stdio (default)
mcp.run(transport="http", host="127.0.0.1", port=8000)   # HTTP
```

----

## Exercise: MCP Inspector

### Step 1: Install Node.js

Check whether `npx` is available:

```bash
npx --version
```

If not, install Node.js from [nodejs.org](https://nodejs.org/).

### Step 2: Start the Inspector

```bash
npx @modelcontextprotocol/inspector
```

A browser window should open.

### Step 3: Connect to your server

Start your Fibonacci server via HTTP (see [hello_mcp.md](hello_mcp.md)). In the Inspector:

1. Transport Type: **Streamable HTTP**
2. URL: `http://localhost:8000/mcp`
3. click **Connect**
4. go to **Tools** → **List Tools** → select `fibonacci` → **Run Tool**

### Step 4: Examine the raw traffic

Open the **History** panel at the bottom.
Click on each entry and find:

- the `initialize` request and the server's capabilities
- the `tools/list` response with your docstrings
- the `tools/call` request and the corresponding response

**Tip:** FastMCP can start the Inspector together with your server:

```bash
uv run fastmcp dev inspector fibonacci_mcp.py
```

----

## Exercise: Local LLM with Ollama

### Step 1: Install Ollama

Download and install from [ollama.com/download](https://ollama.com/download).

### Step 2: Run a small model

```bash
ollama run qwen3:0.6b
```

Try out a few prompts, e.g. *"What is the 30th Fibonacci number?"*. Exit with `/bye`.

### Step 3: Install an MCP client for Ollama

```bash
uv add ollmcp
```

### Step 4: Connect the model to your server

Start your Fibonacci server via HTTP. In a second terminal:

```bash
uv run ollmcp -m qwen3:0.6b -u http://localhost:8000/mcp
```

Ask again: *"What is the 30th Fibonacci number?"*
Observe whether the model calls the tool.

If the model ignores the tool, try a larger one: `qwen3:1.7b` or `qwen3:4b`.

----

## Exercise: Claude

### Step 1: Register the server in Claude Code (CLI)

While the server is running via HTTP:

```bash
claude mcp add --transport http fibonacci http://localhost:8000/mcp
claude mcp list
```

Alternatively via stdio – Claude then starts the server itself:

```bash
claude mcp add fibonacci-stdio -- uv run --directory /full/path/to/your/project fibonacci_mcp.py
```

For stdio, the server must call `mcp.run()` without `transport="http"`.

### Step 2: Run a prompt in the CLI

```bash
claude
```

Type `/mcp` to see the connected servers. Then ask:

> Which Fibonacci numbers are at positions 50 to 60?

Claude asks for permission before calling the tool.

### Step 3: Run the same prompt in VS Code

1. open your project folder in VS Code
2. open the Claude Code panel
3. type `/mcp` and check whether `fibonacci` is connected (VS Code uses the same configuration as the CLI)
4. run the same prompt

### Step 4: Compare

- Did all clients (Ollama, Claude CLI, VS Code) call the tool?
- Which tool did they choose: `fibonacci` or `fibonacci_series`?
