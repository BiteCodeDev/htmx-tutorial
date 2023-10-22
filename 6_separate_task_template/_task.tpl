<li >
    <input type="checkbox" id="task{{task['id']}}"
           name="task"
           value="{{task['id']}}"
           % if task['done']:
           checked
           % end
    >
    <label for="task{{task['id']}}">{{task['title']}}</label>
    <a
    hx-delete="/tasks/{{task['id']}}"
    hx-swap="outerHTML"
    hx-target="body"
    >X</a>
</li>
