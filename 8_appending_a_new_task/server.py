import sys
from pathlib import Path

### BOILERPLATE TO MINIMIZE DEMO SETUP FOR YOU, IGNORE ###
CUR_DIR = Path(__file__).resolve().parent
sys.path.append(str(CUR_DIR.parent))

import todo
from bottle import TEMPLATE_PATH, debug, redirect, request, route, run, template

TEMPLATE_PATH.append(str(CUR_DIR))
### END BOILER PLATE ###


@route("/")
def index():
    tasks = todo.list_todos()
    counts = todo.count_todos()
    return template("index", tasks=tasks, counts=counts)


@route("/tasks/", method="POST")
def add():
    title = request.forms.get("title")
    if title:
        new_task = todo.add_todo(title)
        return template("_task", task=new_task)
    return ""


@route("/tasks/<task_id:int>", method="PUT")
def toggle_task(task_id):
    status = request.forms.get("task")
    todo.set_task_status(task_id, bool(status))
    return template("_task", task=todo.get_task(task_id))


@route("/tasks/<task_id:int>", method="DELETE")
def delete(task_id):
    todo.delete_todo(task_id)
    return ""


if __name__ == "__main__":
    debug(True)
    run(host="localhost", port=8080, reloader=True)
