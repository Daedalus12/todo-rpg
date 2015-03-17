from pytodoist import todoist
from pyhabit.pyhabit.api import HabitAPI

from datetime import date, timedelta
import auth


def get_uncompleted_tasks_due_today(user):
    daily_tasks = user.search_tasks(todoist.Query.TODAY, todoist.Query.OVERDUE)
    return daily_tasks


def get_todoist_tasks_completed_in_last_week(user):
    d = date.today() - timedelta(days=2)
    return user.search_completed_tasks(from_date=d.strftime("%Y-%m-%dT:23:59"))


def check_if_habitrpg_task_exists(habitapi, task_id):
    response = habitapi.task(task_id)
    try:
        message = response['err']
        return False
    except KeyError:
        return True


if __name__ == "__main__":
    a = auth.Auth()
    todoist_user = todoist.login(a.todoist_username, a.todoist_password)

    habitapi = HabitAPI(a.hrpg_user_id, a.hrpg_token)

    print "TODOIST UNCOMPLETED TASKS:"
    tasks = get_uncompleted_tasks_due_today(todoist_user)
    for t in tasks:
        print "\t", t.id, t.content
        if check_if_habitrpg_task_exists(habitapi, t.id):
            print "\tHabitRPG task already exists; checking if complete"
            response = habitapi.task(t.id)
            if response['completed']:
                print "\t\tCompleting Todoist task"
                t.complete()
            else:
                print "\t\tTodoist task and HabitRPG task both incomplete"
        else:
            print "\tCreating newHabitRPG task"
            habitapi.create_task(habitapi.TYPE_TODO,
                                 t.content,
                                 t.id,
                                 completed=False)

    print "TODOIST COMPLETED TASKS:"
    tasks = get_todoist_tasks_completed_in_last_week(todoist_user)
    for t in tasks:
        print "\t", t.id, t.content
        if check_if_habitrpg_task_exists(habitapi, t.id):
            print "\tHabitRPG task already exists; checking if complete"
            response = habitapi.task(t.id)
            if not response['completed']:
                print "\t\tHabitRPG task uncompleted but Todoist task completed; completing HabitRPG task"
                habitapi.perform_task(t.id, 'up')
            else:
                print "\t\tHabitRPG task is also complete"
