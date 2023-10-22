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
        todo.add_todo(title)
    redirect("/")


@route("/tasks/", method="PUT")
def set_task_status():
    all_tasks = todo.list_todos()
    done_task_ids = set(int(task_id) for task_id in request.forms.getall("task"))
    for task in all_tasks:
        new_status = task["id"] in done_task_ids
        todo.set_task_status(task["id"], new_status)
    redirect("/")


@route("/tasks/<task_id:int>", method="DELETE")
def delete(task_id):
    todo.delete_todo(task_id)
    redirect("/")


if __name__ == "__main__":
    debug(True)
    run(host="localhost", port=8080, reloader=True)
