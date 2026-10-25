"""
LangGraph workflow that uses the incident MCP server.

Run in a separate project (langchain-mcp-adapters needs mcp < 2):

    uv init workflow
    cd workflow
    uv add langgraph langchain-mcp-adapters langchain-ollama

Start incident_mcp.py first.
"""
import asyncio
from typing import Literal, TypedDict

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt
from pydantic import BaseModel, Field

TEAMS = {
    "hardware": "Facility Management",
    "software": "Application Support",
    "network": "Network Operations",
    "security": "Security Team",
}


class Classification(BaseModel):
    title: str = Field(description="short summary of the incident")
    location: str = Field(description="where it happened")
    category: Literal["hardware", "software", "network", "security"]


class State(TypedDict, total=False):
    message: str
    classification: dict
    priority: str
    team: str
    approved: bool
    incident: str


llm = ChatOllama(model="qwen3:0.6b", temperature=0)
mcp_client = MultiServerMCPClient(
    {"incidents": {"url": "http://localhost:8000/mcp", "transport": "streamable_http"}}
)


def classify(state: State) -> State:
    """use Ollama to extract location + category from the incident message"""
    classifier = llm.with_structured_output(Classification)
    result = classifier.invoke(f"Classify this incident report:\n\n{state['message']}")
    return {"classification": result.model_dump()}


def assign_priority(state: State) -> State:
    """deterministic step"""
    c = state["classification"]
    priority = "high" if c["category"] == "security" else "normal"
    return {"priority": priority, "team": TEAMS[c["category"]]}


def approve(state: State) -> State:
    """a human checks the classification before anything is recorded"""
    c = state["classification"]
    answer = interrupt(
        f"Record '{c['title']}' at location <{c['location']}> (category {c['category']}) "
        f"for {state['team']} with {state['priority']} priority? (y/n)"
    )
    return {"approved": answer.strip().lower() in ("y", "yes", "j", "ja")}


def route_approval(state: State) -> str:
    return "record" if state["approved"] else END


async def record(state: State) -> State:
    """Calls MCP to record the incident"""
    tools = {t.name: t for t in await mcp_client.get_tools()}
    c = state["classification"]
    result = await tools["create_incident"].ainvoke(
        {"title": c["title"], "description": state["message"], "location": c["location"]}
    )
    return {"incident": result[0]["text"]}


def notify(state: State) -> State:
    """Nachricht ans Team ausgeben"""
    print(f"📣 to {state['team']} ({state['priority']} priority):")
    print(f"   {state['incident']}")
    return {}


graph = StateGraph(State)
graph.add_node(classify)
graph.add_node(assign_priority)
graph.add_node(approve)
graph.add_node(record)
graph.add_node(notify)

graph.add_edge(START, "classify")
graph.add_edge("classify", "assign_priority")
graph.add_edge("assign_priority", "approve")
graph.add_conditional_edges("approve", route_approval, ["record", END])
graph.add_edge("record", "notify")
graph.add_edge("notify", END)
workflow = graph.compile(checkpointer=InMemorySaver())


async def main():
    # print(workflow.get_graph().draw_mermaid())
    config = {"configurable": {"thread_id": "1"}}
    message = input("describe the incident: ")
    state = await workflow.ainvoke({"message": message}, config)
    question = state["__interrupt__"][0].value
    answer = input(question + " ")
    state = await workflow.ainvoke(Command(resume=answer), config)
    if not state["approved"]:
        print("rejected, nothing recorded")


if __name__ == "__main__":
    asyncio.run(main())
