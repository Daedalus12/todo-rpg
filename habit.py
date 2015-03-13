import hrpg.core
from datetime import datetime, date, timedelta
import auth
import sys, os

sys.path.append(os.path.join(".","pyhabit"))
from pyhabit.pyhabit.api import HabitAPI

a = auth.Auth()
h = HabitAPI(a.hrpg_user_id, a.hrpg_token)

for task in h.tasks2():
    print type(task)
    print type(task.json())