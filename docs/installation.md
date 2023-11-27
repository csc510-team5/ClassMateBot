# Setup/Installation Guide

**NOTE: DO NOT UPLOAD YOUR** `.env` **FILE TO YOUR REPO**.

To set up and run the ClassMate Bot:
1. Ensure you have the following installed:
    * [Python 3](https://www.python.org/downloads/) 
    * [pip](https://pip.pypa.io/en/stable/installation/)
2. Clone this repo onto your local machine
    ```
    git clone https://github.com/csc510-team5/ClassMateBot.git
    cd ClassMateBot
    ```
3. In the repository directory, run `pip install -r requirements.txt`
4. Create a `.env` file in your project's root directory (we will put things into it later)
5. Create a Discord bot and get its token:
   1. Create a [Discord Account](https://discord.com/login)
   2. Create a Discord server for the bot to run in
   3. Create a Discord bot in the [Developer Portal](https://discord.com/developers/applications) by [following instructions here](https://realpython.com/how-to-make-a-discord-bot-python/). Copy the bot's token into the `.env` file:
      ```
      # .env
      TOKEN={your-bot-token}
      ```
6. **Set up the database.** ClassMate Bot currently uses [Heroku](https://www.heroku.com/) as a cloud platform for running the bot, and uses a PostgreSQL database hooked up to the Heroku application that runs the bot.
   1. [Create a Heroku account](https://signup.heroku.com/login).
   2. Sign in to Heroku and create a new Heroku application.
   3. Add the Heroku Postgres extension (in the `Resources` tab of the Heroku application web UI).
   4. Acquire the PostgreSQL database connection URL (In the web UI inside the Heroku app, navigate to `Resources > Heroku Postgres > Settings > View Credentials...` and note the URI). Copy this URI into the `.env` file; your `.env` file should now look like this:
      ```
      # .env
      TOKEN={your-bot-token}
      DATABASE_URL={your-database-url}
      ```
7. TO COMPLETELY SET UP THE DATABASE, SEE THE SECTIONS BELOW. Under the **Heroku** section, follow the **Installation** and **Database Setup** guides. DO THIS BEFORE CONTINUING ON TO THE NEXT STEP.
8. Create a Google Cloud Project ([Follow instructions here](https://developers.google.com/calendar/api/quickstart/python))
9. Start the bot. From the project root directory, run `python3 bot` (or `python bot.py` on Windows)
10. Invite the bot to your server ([Follow instructions here](https://realpython.com/how-to-make-a-discord-bot-python/)) (**Please ensure the bot is running and that the database is set up in order for server initialization to happen properly**)
    * NOTE:  When using the OAuth2 URL Generator, make sure you check the box which gives your bot Administrative permissions
11. You should now be able to input commands and get responses from the bot as appropriate.

## Heroku

## Working with the Heroku PostgreSQL database
Working directly with the PostgreSQL database can be done through the PostgreSQL command line interface `psql`.

### Installation:

1. [Install PostgreSQL on your system](https://www.postgresql.org/download/) (details differ depending on OS) and ensure you can access the `psql` program through a terminal.
2. Set up the heroku command line tool:
   1. [Install the heroku command line tool](https://devcenter.heroku.com/articles/heroku-cli)
   2. Authenticate to the Heroku CLI: `heroku login`
   3. Connect the Heroku CLI to your Heroku app: from your project's root directory run `heroku git:remote -a <name-of-your-app>`

You should now be able to connect to the Heroku PostgreSQL database through the `psql` client by running `heroku pg:psql` (if this step fails you may have not installed PostgreSQL correctly/installed the wrong version.) 

Documentation for `psql` can be found [here](https://www.postgresql.org/docs/13/app-psql.html)

Ensure that your PostgreSQL version matches the version (PG version) displayed when you enter `heroku pg:info`. (This may or may not be an issue.)  

If you are using Windows, be sure to add PostgreSQL to your PATH environment variable: `C:\Program Files\PostgreSQL\<VERSION>\bin`

### Database setup:

This should only be done **ONCE** per Heroku app.

If you used the PostgreSQL installer, you should have a program called pgAdmin4. If not, download it [here](https://www.pgadmin.org/download/).

1. Login to Heroku and select your app. Navigate to `Resources` and select Heroku Postgres. Go to Settings and click View Credentials.
2. Launch pgAdmin4. Right click on `Servers` and then click `Create > Server`.
3. Under the `general` tab, choose any name you want.
4. Under the `connection` tab:
   From your Heroku credentials:
   1. Copy and paste the **Host** credential into pgAdmin's **Host name/address** field.
   2. Copy and paste port into pgAdmin's port.
   3. Copy and paste the **Database** credential into pgAdmin's **Maintenance database** field. (This is NOT your database's name!)
   4. Copy and paste the **User** credential into pgAdmin's **Username** field.
   5. Copy and paste the **Password** credential into pgAdmin's **Password** field. For sanity's sake, tick the "save password" box.
   6. **DO NOT PRESS SAVE YET.**
5. Go to the `SSL` tab in pgAdmin. Under **SSL Mode**, select **Require**.
6. Go to the `Advanced` tab. Inside the **DB Restriction** field, enter your Heroku **Database** credential. (This is the same string you entered into **Maintenance Database**.) DO NOT SKIP THIS STEP.
7. _Now_ you can press save.
8. Inside your newly created server, open up the `Databases > Schemas > Public` drop down lists. Right click on `Tables` and select the `Query Tool`.
9. Inside the query tool, click on `Query Editor.` Copy and paste the contents of [this SQL file](../init.sql) into the editor and then click on the execute button (looks like a play button).
10. Right click on `Tables` and select `refresh`.

Congratulations! You now have your tables set up.

## Google Calendar setup:

1. Create a Calendar category on your Google Calendar that will be used for the shared bot calendar
2. Find the Calendar ID of this calendar in the Google Calendar settings under "Integrate calendar" and add it to your .env file
    ```
      # .env
      TOKEN={your-bot-token}
      DATABASE_URL={your-database-url}
      CALENDAR_ID={your-calendar-id}
      ```
3. In the same settings menu, find the secret address of this calendar and add it to your .env file
    ```
      # .env
      TOKEN={your-bot-token}
      DATABASE_URL={your-database-url}
      CALENDAR_ID={your-calendar-id}
      CALENDAR_ICS={your-secret-address}
      ```
4. In your directory of choice create two files, calendar.pdf and ical.ics
5. Copy the path to this directory and add it to your .env file
   ```
      # .env
      TOKEN={your-bot-token}
      DATABASE_URL={your-database-url}
      CALENDAR_ID={your-calendar-id}
      CALENDAR_ICS={your-secret-address}
      CALENDAR_PATH={path-to-files}
      ```
6. Download wkhtmltopdf ([Download here](https://wkhtmltopdf.org/downloads.html)) Note: If you are on Windows add the path of the downloaded file to your PATH environment variable 

#### Resolving calendar issues

Until the Google Cloud App is pushed to production, the user that is managing the bot will need to generate a new token every seven days:
1. Delete the `token.json` file from the project root directory.
2. Run one of the calendar commands specified in /docs/Calendar: this will open a browser window allowing you to reauthenticate the application and generate a new `token.json`

## Running the bot locally

This is recommended if you plan on testing your changes before pushing them to github. Be sure to turn off any Heroku dynos that may be active!  

1. From the project root directory, run `python3 bot` (or `python bot.py` on Windows).  
2. Test your changes in your Discord server.
3. If you want to reload the bot, hit `ctrl+c` in the terminal and run the bot again.

Easy! 

Every member of your group can have their own private Discord server and bot. Each bot should be connected to its own Heroku app and database, however. To setup your bot, simply follow this guide from the beginning for each bot!

## Running the bot through Heroku

NOTE: You do NOT need to follow this step for the database to work properly!

In order to run the bot through Heroku, first ensure that the bot is connected to, and deployed from, your GitHub repo. To do this, navigate to `Deploy > GitHub` in the Heroku web UI for your app and connect the app to your ClassMateBot fork. After the app is deployed, navigate to `Resources` and click the pencil icon, flip the switch to on, and click confirm, within the `worker` dyno.

Be sure to add your bot token to your Heroku config vars!

Go to `Settings > Reveal Config Vars` and add TOKEN as you did for your .env file.

If you run out of dyno hours, it's still possible to run the bot. From the project root directory, run `python3 bot` (or `python bot.py` on Windows)

## Running Tests
This bot is tested using pytest and [dpytest](https://dpytest.readthedocs.io/en/latest/index.html). To run tests on the ClassMate Bot, run `pytest` in the root directory.

## Repository Workflows

### Configuration files

Configuration files for coverage and pylint are available in the project's root directory. You can (and should!) edit them as you please.

Coverage configuration: `.coveragerc`

Pylint configuration: `.pylintrc`

### Running workflows

To get the workflows to properly run, add the tokens in your .env file to your repository secrets. (**DO NOT UPLOAD .ENV** !!!)

<img src="../data/proj3media/cmbotsecrets.png" width="800">
