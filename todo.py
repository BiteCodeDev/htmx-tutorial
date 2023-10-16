from __future__ import unicode_literals

import sqlite3
import tempfile
from pathlib import Path

# This creates the database in a temporary directory
db_path = Path(tempfile.gettempdir()) / "bitecode_htmx_todo.db"
conn = sqlite3.connect(str(db_path))
conn.row_factory = sqlite3.Row
c = conn.cursor()
c.execute(
    "CREATE TABLE IF NOT EXISTS todos (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, done BOOL NOT NULL)"
)
conn.commit()


# From there, each function is an operation on the list of things to do
# The texts between """ tell you what each function does.
def add_todo(title):
    """Add a task to the things to do in the database and return it"""

    c.execute("INSERT INTO todos (title, done) VALUES (?, 0)", (title,))
    conn.commit()
    return {"id": c.lastrowid, "title": title, "done": False}


def set_task_status(task_id, done):
    """Set a task as done, or to be done, and return it partially"""

    c.execute("UPDATE todos SET done=? WHERE id=?", (done, task_id))
    conn.commit()
    return {"id": task_id, "done": done}


def delete_todo(task_id):
    """Delete a task completely"""

    c.execute("DELETE FROM todos WHERE id=?", (task_id,))
    conn.commit()


def list_todos():
    """Return all tasks"""

    return c.execute("SELECT * FROM todos ORDER BY id").fetchall()


def get_task(task_id):
    """Return one single task"""

    return c.execute("SELECT * FROM todos WHERE id=?", (task_id,)).fetchone()


def count_todos():
    """Return a count of all tasks and a count of the ones remaining to be done"""

    c.execute("SELECT COUNT(*) FROM todos")
    total = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM todos WHERE done")
    done = c.fetchone()[0]
    return {"done": done, "total": total}
