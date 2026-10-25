# Logging and Debugging

With the **stdio** transport, `stdout` **is** the JSON-RPC channel.
Anything else written to `stdout` corrupts the messages:

```python
print("starting server")                  # breaks stdio servers
print("starting server", file=sys.stderr) # OK
```

Better: use logging, which writes to `stderr` by default:

```python
import logging

logging.basicConfig(level=logging.INFO)
logging.info("starting server")
```

Where to find the error messages:

- `uv run fastmcp run server.py --log-level DEBUG`
- MCP Inspector: panel **Server Notifications**
- Claude Code: `claude --debug`, or `/mcp` to see the server status
- ollmcp: `uv run ollmcp --debug`

----

## Exercise: Debugging

The server [code/broken_mcp.py](code/broken_mcp.py) is broken.
A colleague registered it in Claude Code with:

```bash
claude mcp add broken -- uv run --directory /home/alice/mcp_course broken_mcp.py
```

1. Register the server the same way in your Claude Code (or ollmcp) client.
2. Find out why the server doesn't connect. Fix the configuration.
3. Start Claude with `claude --debug` and type `/mcp`. Find out why the server reports errors. Fix them.
4. Call the tool directly. Find out why it fails. Fix it.

   ```bash
   uv run fastmcp call broken_mcp.py fibonacci n=20
   ```

<details>
<summary>Hints</summary>

- wrong `--directory` path in the configuration (`claude mcp remove broken`, then add it again)
- `print()` writes to `stdout`
- the parameter `n` has no type hint, so the schema accepts anything – including a string

</details>
