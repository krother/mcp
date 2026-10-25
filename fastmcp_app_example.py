from prefab_ui.actions import SetState, ShowToast
from prefab_ui.actions.mcp import CallTool
from prefab_ui.app import PrefabApp
from prefab_ui.components import (
    Badge, Button, Column, ForEach, Form, Heading,
    Input, Row, Separator, Text,
)
from prefab_ui.rx import RESULT
from fastmcp import FastMCP, FastMCPApp

app = FastMCPApp("Notes")
notes_db: list[dict] = []


@app.tool()
def add_note(title: str, body: str) -> list[dict]:
    """Save a note and return all notes."""
    notes_db.append({"title": title, "body": body})
    return list(notes_db)


@app.ui()
def notes_app() -> PrefabApp:
    """Open the notes app."""
    with Column(gap=6, css_class="p-6") as view:
        Heading("Notes")

        with ForEach("notes") as note:
            with Row(gap=2, align="center"):
                Text(note.title, css_class="font-semibold")
                Badge(note.body)

        Separator()

        with Form(
            on_submit=CallTool(
                "add_note",
                on_success=[
                    SetState("notes", RESULT),
                    ShowToast("Note saved!", variant="success"),
                ],
                on_error=ShowToast("Failed to save", variant="error"),
            )
        ):
            Input(name="title", label="Title", required=True)
            Input(name="body", label="Body", required=True)
            Button("Add Note")

    return PrefabApp(view=view, state={"notes": list(notes_db)})


mcp = FastMCP("Notes Server", providers=[app])