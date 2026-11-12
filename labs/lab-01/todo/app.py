"""A simple to-do list app built with Streamlit, using a JSON file as the database."""

import json
import uuid
from pathlib import Path

import streamlit as st

# The "database": a JSON file stored next to this script.
DB_FILE = Path(__file__).parent / "todos.json"


# ---------- Data layer: reading and writing the JSON file ----------

def load_todos() -> list[dict]:
    """Read all tasks from the JSON file. Returns an empty list if the file doesn't exist yet."""
    if not DB_FILE.exists():
        return []
    try:
        return json.loads(DB_FILE.read_text())
    except json.JSONDecodeError:
        st.error("todos.json is damaged and couldn't be read. Starting with an empty list.")
        return []


def save_todos(todos: list[dict]) -> None:
    """Write all tasks back to the JSON file."""
    DB_FILE.write_text(json.dumps(todos, indent=2))


# ---------- Presentation layer: what the user sees ----------

st.title("✅ To-Do List")

todos = load_todos()

# Form to add a new task. clear_on_submit empties the text box after adding.
with st.form("add_task", clear_on_submit=True):
    new_task = st.text_input("New task", placeholder="What do you need to do?")
    if st.form_submit_button("Add") and new_task.strip():
        todos.append({"id": str(uuid.uuid4()), "text": new_task.strip(), "done": False})
        save_todos(todos)
        st.rerun()

if not todos:
    st.info("No tasks yet. Add one above!")

# Show each task with a checkbox (done / not done) and a delete button.
for todo in todos:
    col_check, col_delete = st.columns([6, 1])
    with col_check:
        done = st.checkbox(todo["text"], value=todo["done"], key=f"done_{todo['id']}")
        if done != todo["done"]:
            todo["done"] = done
            save_todos(todos)
            st.rerun()
    with col_delete:
        if st.button("🗑️", key=f"delete_{todo['id']}", help="Delete task"):
            todos = [t for t in todos if t["id"] != todo["id"]]
            save_todos(todos)
            st.rerun()

if todos:
    remaining = sum(not t["done"] for t in todos)
    st.caption(f"{remaining} of {len(todos)} tasks left")
