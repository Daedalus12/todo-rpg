import os, sys
sys.path.append(os.path.join(".", "pyhabit"))
sys.path.append(os.path.join(".", "pytodoist"))

from pytodoist import todoist
from pyhabit.api import HabitAPI

from datetime import date, timedelta
import os


def get_uncompleted_tasks_due_today(user):
    daily_tasks = user.search_tasks(todoist.Query.TODAY, todoist.Query.OVERDUE)
    return daily_tasks


def get_todoist_tasks_completed_in_last_week(user):
    d = date.today() - timedelta(days=2)
    return user.search_completed_tasks(from_date=d.strftime("%Y-%m-%dT:23:59"))


def check_if_habitrpg_task_exists(habit_api, task_id):
    resp = habit_api.task(task_id)
    if 'err' in resp:
        return False
    else:
        return True



def sync():
    todoist_user = todoist.login(os.environ.get('TODOIST_USERNAME'),
                                 os.environ.get('TODOIST_PASSWORD'))

    habit_api = HabitAPI(os.environ.get('HABITRPG_USER_ID'),
                        os.environ.get('HABITRPG_API_TOKEN'))

    print "TODOIST UNCOMPLETED TASKS:"
    tasks = get_uncompleted_tasks_due_today(todoist_user)
    for t in tasks:
        print "\t", t.id, t.content
        if check_if_habitrpg_task_exists(habit_api, t.id):
            print "\tHabitRPG task already exists; checking if complete"
            resp  = habit_api.task(t.id)
            if resp['completed']:
                print "\t\tCompleting Todoist task"
                t.complete()
            else:
                print "\t\tTodoist task and HabitRPG task both incomplete"
        else:
            print "\tCreating newHabitRPG task"
            habit_api.create_task(habit_api.TYPE_TODO,
                                 t.content,
                                 t.id,
                                 completed=False)

    print "TODOIST COMPLETED TASKS:"
    tasks = get_todoist_tasks_completed_in_last_week(todoist_user)
    for t in tasks:
        print "\t", t.id, t.content
        if check_if_habitrpg_task_exists(habit_api, t.id):
            print "\tHabitRPG task already exists; checking if complete"
            response = habit_api.task(t.id)
            if not response['completed']:
                print "\t\tHabitRPG task uncompleted but Todoist task " \
                      "completed; completing HabitRPG task"
                habit_api.perform_task(t.id, 'up')
            else:
                print "\t\tHabitRPG task is also complete"