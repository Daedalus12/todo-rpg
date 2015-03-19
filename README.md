todo-rpg
========
Syncs task creation and completion between Todoist and HabitRPG

Installation
------------

Clone the repository:


    git clone https://github.com/Daedalus12/pyhabit.git
    cd pyhabit
    
Deploy a Heroku app:


    heroku create my-todo-rpg
    git push heroku master
   

Create a local file '.env' with login information:


    HABITRPG_USER_ID=55555555-5555-5555-5555-555555555555
    HABITRPG_API_TOKEN=55555555-5555-5555-5555-555555555555
    TODOIST_USERNAME=example@example.com
    TODOIST_PASSWORD=pa$$word


Add the login information to Heroku:


    python set_heroku_environment_variables.py
    
    
Run the script to make sure it works


    heroku run python runserver.py
    
    
Install an add-on to schedule running the script every 10 minutes


    heroku addons:add scheduler


Open the add-on configuration page and set up the recurring dyno:

- `heroku addons:open scheduler`
- Click 'Add Job...'
- Enter `python runserver.py` into the `$` field
- Set the frequency to 'Every 10 minutes' in the  dropdown menu
- Click 'Save'
    
That's it! You should be all set up.