from pytodoist import todoist
from datetime import datetime, date, timedelta
import auth


def getTodoistTasksNext24():
    a = auth.Auth()
    user = todoist.login(a.todoist_username, a.todoist_password )
    tasks = user.get_uncompleted_tasks()
    now = datetime.now()
    filtered_tasks = []
    threshold = timedelta(hours=24)
    for task in tasks:
        if task.due_date is not None:
            duedate = datetime.strptime(task.due_date, "%a %d %b %Y %H:%M:%S")
            if (duedate - now) < threshold:
                filtered_tasks.append(task)
                print task.content

    return filtered_tasks

getTodoistTasksNext24()

