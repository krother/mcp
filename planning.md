
# Connecing AI Applications with MCP

## Course Goals

- create a MCP-compatible web app
- define a CLI application that an LLM can use
- connect an existing LLM to an MCP service
- build a practical usage exampe, e.g. recording an incident

Below, six separate modules are described that can be delivered over 2 days.

## Day 1

### Module 1: Fundamentals

- ACTIVITY: once upon a time
- VISUAL: Architecture of a LLM 
- concept: from neurons to transformers – what a model actually computes (next-token prediction)
- TABLE: frontier models vs. open-weight models
- Q: have you used any of these already? How good were they?
- recent improvements, context as a scarce resource  
- VISUAL: pelicans
- ACTIVITY: text with gaps using words: dneural network, LLMs, context, tokens, prompt, user prompt, system prompt, temperature
- ACTIVITY: group discussion: current and future business scenarios?


### Module 2: Building MCP Servers

- Q: who attended the FastAPI course?
- Q: do we want to use pymcp or fastmcp? Check on pypi.org
- EXERCISE: implement a Fibonacci function, compare to ChatGPT
- VISUAL: MCP as an implementation of the Bridge Pattern
- concept: the N×M integration problem and how MCP standardizes it ("USB-C for AI")
- concept: architecture – host, client, server; JSON-RPC 2.0 messages
- concept: MCP vs. plain function calling vs. REST APIs

### 2.1 hello world
- EXERCISE: fibonacci mcp
  - set up project with uv
  - name bug by creating folder 'mcp'
  - install fastmcp
  - implement a hello world MCP service in Python with FastMCP
  - add fastmcp
  - run the MCP service as a HTTP service
  - add convenience app with Prefab to run in dev mode
  - visit the mcp in the browser

#### 2.2 information for the prompt

- EXERCISE: add instructions, docstring, parameter descriptions

### Module 3: MCP Clients

- VISUAL: The agent loop
  - concept: the agent loop – send tool schemas to the LLM, execute `tool_use` blocks, return results
- TABLE: stdio vs HTTP vs SSE: stdio for local, single-user processes; HTTP-based transports for remote, multi-client services, streaming-enabled; SSE obsoleted by Streamable HTTP in the current spec

#### 3.1 MCPInspector

- EXERCISE: install npm + MCPInspector
- EXERCISE: inspect the raw JSON-RPC traffic of an existing MCP server

#### 3.2 Ollama

- EXERCISE: run the smallest Qwen3 model via Ollama and llmcp

#### 3.3 Claude

- connect MCP to Claude in VSCode
- connect MCP to Claude in cli
- run prompt in both

## Tools, Resources and Prompts

- VISUAL: building blocks of MCPs: Tools, Resources and Prompts
- EXERCISE: extend the server to read resources
- EXERCISE: extend the server render prompt templates
- concept: logging and debugging – why `print()` breaks stdio servers, logging to stderr instead
- EXERCISE: broken code: debug a server with typical faults (wrong config path, missing type hints, stdout pollution) and fix them


## Day 2

## An MCP for incident reporting

- VISUAL: project structure
- EXERCISE: a step-by-step guide for implementing a MCP server for incident reporting
  goal: complete an incident-recording server with tools  `create_incident`, `list_incidents`, `close_incident`
  - project setup with uv, the `mcp` / `fastmcp` package
  - implement a first tool with `@mcp.tool()`
  - add type hints
  - add a docstring
  - add a resource (`@mcp.resource("incident://{id}")`)
  - add a prompt template

## Validation with pydantic

- EXAMPLE: pydantic type annotations in a MCP tools: Field, validation helper function, range limits
- EXERCISE: add pydantic model : improve a tool with vague parameters (`data: str`) into a well-typed pydantic interface and compare LLM behavior

## UI with Prefab

- the Prefab app interface
- EXAMPLE: working example code
- EXERCISE: run the example and see the UI
- EXERCISE: browse the catalog
- EXAMPLE: form example code that calls back to the server
- EXERCISE: build human-in-the loop step with Prefab

## LangGraph Workflows

- VISUAL: workflow
- concept: workflow automation in LangGraph
- concept: loading MCP tools into LangGraph via `langchain-mcp-adapters`
- EXERCISE: run a workflow "classify incident → assign priority → notify responsible team"
- EXERCISE: extend the workflow with a conditional branch (escalation for high priority)
- QUESTION: when a fixed workflow beats a free agent?
- Human-in-the-Loop: implementing explicit approval steps
  - QUESTION: which actions need approval (irreversible, outward-facing, costly)
  - concept: interrupts in LangGraph
  - code along: an approval step before `close_incident` is executed
  - exercise: execute a LangGraph interrupt that waits for a human decision


## Error recovery
- where to add retries, timeouts, idempotency, fallbacks?
- EXERCISE: debug a tool that fails silently and makes the LLM hallucinate a success. Add a meaningful error message

## Vectorized search
- relational and vector databases
  - VISUAL: TF Projector
  - concept: embeddings as vectors of meaning
  - concept vector-based search over documents
  - USE A DATABASE THAT IS pip-installable
  - EXERCISE: a `search_similar_incidents` tool backed by embeddings

## Multiple MCP servers

- VISUAL: MCP services, mounted service, gateway
- decoupling MCP servers from existing applications with FastMCP submodules, microservices and MCP Gateways
- concept: mounting/composing several FastMCP servers into one
- TABLE with short descriptions: Microservice, Docker, HTTP transport, MCP gateway, proxy, central routing, authentication, tool filtering
- EXERCISE: expose an existing FastAPI web app as an MCP service

MAKE CARD PAIRS TEXT + TITLE


## Data Protection and Security

- security and data protection risks when using AI
  - TABLE: lethal trifecta of security issues (Veit)
  - concept: prompt injection (direct and indirect), tool poisoning
  - concept: excessive agency and confused-deputy problems; OWASP Top 10 for LLM applications
  - data protection risks when using AI
  - concept: least privilege – read-only tools, scoped credentials, tool allowlists
- EXERCISE: add audit logging of every tool call

## MCP as a backend worker

- concept: long-running tasks, progress notifications and cancellation
- EXERCISE: create a Task with FastMCP
- EXERCISE: a batch script that imports a CSV of incidents via the MCP server
- QUESTION: when is MCP the right abstraction, and when is a plain REST API simpler?


## Practical Considerations when using MCPs

This module should provide food for thought for a generic discussion.

- EXERCISE: write pytest tests for the incident server
- SHORT TEXTS TO BE PRINTED ON CARDS: software engineering best practices
  - 12-factor app
  - functional requirements
  - non-functional requirements
  - 4 requirements of software: availability, reliability, security, safety
  - software entropy
- QUESTION: how do I know that my LLM application is working?
- QUESTION: how do I know that my LLM application is doing the right thing?
- QUESTION: how is my service going to change in the future?

- discussion: next steps, transfer to participants' projects
- feedback round
