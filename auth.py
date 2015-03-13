import json

class Auth(object):

    def __init__(self):
        f = open("config.json", "r")
        d = json.load(f)[0]
        f.close()
        self.todoist_username = d["todoist"]["username"]
        self.todoist_password = d["todoist"]["password"]
        self.hrpg_user_id= d["habit-rpg"]["user-id"]
        self.hrpg_token = d["habit-rpg"]["api-token"]