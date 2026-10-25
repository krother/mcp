
## Exercise 3: Match the terms

Cut out the cards and match each term with its description.

| Term |
|---------|
| Microservice |
| Docker |
| HTTP Transport |
| MCP Gateway |
| Proxy |
| central routing |
| authentication |
| tool filtering |

| Description |
|--------------|
| decides based on the tool name which server receives a request |
| a small, independently deployable service with exactly one task |
| hides tools that a particular client should not see or use |
| packages a server with all its dependencies into a container |
| a central entry point for many MCP servers, with auth, logging and filters |
| checks who makes a request, e.g. via an OAuth token |
| a server that passes requests on to another server unchanged |
| runs an MCP server as a web service that many clients can access |



## Exercise 2: Software engineering card set

Each group draws a card and discusses: *What does this mean for our MCP server?*

```{card} 12-Factor App
Twelve rules for web services, e.g.: configuration in environment variables, logs as a stream, stateless processes.
Our server stores incidents in memory – which rule does that violate?
```

```{card} Functional requirements
*What* should the system do? E.g. "An incident can be created, listed and closed."
Who decides which tools an LLM needs?
```

```{card} Non-functional requirements
*How well* should the system do it? Response time, cost per request, data protection, maintainability.
Which of these change when an LLM is involved?
```

```{card} The 4 requirements of software
**Availability** – the system is reachable.
**Reliability** – it delivers correct results.
**Security** – it is protected against attacks.
**Safety** – it does no harm.
```

```{card} Software entropy
Software that is changed becomes messier over time – unless someone actively cleans it up.
What happens to tool descriptions when the model behind them changes?
```
