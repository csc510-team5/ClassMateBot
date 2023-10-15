from __future__ import print_function

import os.path
import datetime
import discord
import asyncio
from dotenv import load_dotenv
from discord.ext import commands, tasks

from google.auth.transport.requests import Request
from datetime import timedelta, datetime, date
from google.oauth2.credentials import Credentials
from urllib.request import urlopen
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pdfkit
import pandas as pd


class Calendar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.checkForEvents.start()

    def credsSetUp(self):
        # If modifying these scopes, delete the file token.json.
        SCOPES = ["https://www.googleapis.com/auth/calendar"]

        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        # If there are no (valid) credentials available, let the user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w", encoding="utf-8") as token:
                token.write(creds.to_json())
        return creds

    async def listCalendarEvents(self):
        creds = self.credsSetUp()
        try:
            service = build("calendar", "v3", credentials=creds)
            calendar = os.getenv("CALENDAR_ID")
            # Call the Calendar API
            now = datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
            print("Getting the upcoming 10 events")
            events_result = (
                service.events()
                .list(
                    calendarId=calendar,
                    timeMin=now,
                    maxResults=10,
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )
            events = events_result.get("items", [])

            if not events:
                print("No upcoming events found.")
                return
            return events

        except HttpError as error:
            print(f"An error occurred: {error}")

    @commands.command(name="addCalendarEvent")
    async def addCalendarEvent(self, ctx, name, location, description):
        creds = self.credsSetUp()
        try:
            calendar = os.getenv("CALENDAR_ID")
            service = build("calendar", "v3", credentials=creds)
            event = {
                "summary": name,
                "location": location,
                "description": description,
                "colorId": 4,
                "start": {
                    "dateTime": "2023-10-28T17:00:00-07:00",
                    "timeZone": "America/New_York",
                },
                "end": {
                    "dateTime": "2023-10-28T17:00:00-07:00",
                    "timeZone": "America/New_York",
                },
            }
            event = service.events().insert(calendarId=calendar, body=event).execute()

        except HttpError as error:
            print(f"An error occurred: {error}")

    # -----------------------------------------------------------------------------------------------------------------
    #    Function: getiCalDownload(self, ctx)
    #    Description: sends an ics file of the class calendar to the channel the command was issued in
    #    Inputs:
    #       - ctx: context of the command
    #    Outputs:
    #       - The ics file of the calendar
    # -----------------------------------------------------------------------------------------------------------------
    @commands.command(
        name="getiCalDownload",
        help="Enter the command to receive an ics"
        " file of the calendar$getiCalDownload",
    )
    async def getiCalDownload(self, ctx):
        # Get the calendar in ics format
        url = os.getenv("CALENDAR_ICS")
        text = urlopen(url).read().decode("iso-8859-1")
        # parse the received text to remove all \n characters
        newText = ""
        for character in text:
            if character != "\n":
                newText = newText + character
        # write to the ics file
        f = open(os.getenv("CALENDAR_PATH") + "ical.ics", "w", encoding="utf-8")
        f.write(newText)
        f.close()
        await ctx.send(file=discord.File(os.getenv("CALENDAR_PATH") + "ical.ics"))

    # -----------------------------------------------------------------------------------------------------------------
    #    Function: getPdfDownload(self, ctx)
    #    Description: sends an pdf file of the class calendar to the channel the command was issued in
    #    Inputs:
    #       - ctx: context of the command
    #    Outputs:
    #       - The pdf file of the calendar
    # -----------------------------------------------------------------------------------------------------------------
    @commands.command(
        name="getPdfDownload",
        help="Enter the command to receive an ics"
        " file of the calendar$getiCalDownload",
    )
    async def getPdfDownload(self, ctx):
        creds = self.credsSetUp()
        try:
            service = build("calendar", "v3", credentials=creds)
            # Call the Calendar API
            now = datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
            calendar = os.getenv("CALENDAR_ID")
            events_result = (
                service.events()
                .list(
                    calendarId=calendar,
                    timeMin=now,
                    maxResults=150,
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )
            events = events_result.get("items", [])

            if not events:
                print("No upcoming events found.")
                return
            calEvents = []
            for event in events:
                start = event["start"].get("dateTime", event["start"].get("date"))
                end = event["end"].get("dateTime", event["end"].get("date"))
                calEvent = {"Summary": event["summary"], "Start": start, "End": end}
                calEvents.append(calEvent)
            df = pd.DataFrame(calEvents)
            htmlCal = df.to_html()
            pdfkit.from_string(htmlCal, os.getenv("CALENDAR_PATH") + "calendar.pdf")
            await ctx.send(
                file=discord.File(os.getenv("CALENDAR_PATH") + "calendar.pdf")
            )

        except HttpError as error:
            print(f"An error occurred: {error}")

    # -----------------------------------------------------------------------------------------------------------------
    #    Function: checkForEvents(self)
    #    Description: Checks the calendar once per day for any events that are due the same day
    #    Outputs:
    #       - Message to the general chat where everyone is pinged of what events are due today
    # -----------------------------------------------------------------------------------------------------------------
    @tasks.loop(seconds=5)
    async def checkForEvents(self):
        creds = self.credsSetUp()
        try:
            service = build("calendar", "v3", credentials=creds)
            # Call the Calendar API
            now = datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
            calendar = os.getenv("CALENDAR_ID")
            events_result = (
                service.events()
                .list(
                    calendarId=calendar,
                    timeMin=now,
                    maxResults=150,
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )
            events = events_result.get("items", [])
            summary = ""
            for event in events:
                dt = datetime.strptime(
                    (event["start"]["dateTime"])[0:18], "%Y-%m-%dT%H:%M:%S"
                )
                if dt.day == date.today().day and dt.year == date.today().year:
                    summary = summary + event["summary"] + ","
            if len(summary) != 0:
                # If the bot is used in more than one server
                for guild in self.bot.guilds:
                    for channel in guild.text_channels:
                        # Find the general channel and ping
                        if channel.name == "general":
                            await channel.send("@everyone " + summary + "due TODAY!")
                            break
        except HttpError as error:
            print(f"An error occurred: {error}")

    # -----------------------------------------------------------------------------------------------------------------
    #    Function: checkForNewDay(self)
    #    Description: Keeps track of time before the calendar is checked each day
    # -----------------------------------------------------------------------------------------------------------------
    @checkForEvents.before_loop
    async def checkForNewDay(self):
        hour = 23
        minute = 23
        await self.bot.wait_until_ready()
        now = datetime.now()
        future = datetime(now.year, now.month, now.day, hour, minute)
        if now.hour >= hour and now.minute > minute:
            future += timedelta(days=1)
        await asyncio.sleep((future - now).seconds)

    # -----------------------------------------------------------------------------------------------------------------
    #    Function: subscribeCalendar(self, ctx, userEmail)
    #    Description: adds specified user to shared Google Calendar
    #    Inputs:
    #       - ctx: context of the command
    #       - target: calendar to modify
    #       - userEmail: user to add to target Google Calendar
    #    Outputs:
    #       - Confirmation string for successful add, error string for failure.
    # -----------------------------------------------------------------------------------------------------------------
    @commands.command(
        name="subscribeCalendar",
        help="Adds user to shared Google Calendar. Ex: subscribecalendar john.doe@gmail.com",
    )
    async def subscribecalendar(self, ctx, userEmail):
        creds = self.credsSetUp()
        try:
            service = build("calendar", "v3", credentials=creds)
            calendar = os.getenv("CALENDAR_ID")
            acl_rule = {
                "scope": {"type": "user", "value": userEmail},
                "role": "reader",  # Adjust the role as needed (e.g., reader, owner)
            }
            acl_rule = (
                service.acl().insert(calendarId=calendar, body=acl_rule).execute()
            )

            print(f"Added {userEmail} to the calendar.")
        except HttpError as e:
            print(f"Error adding user: {str(e)}")

    # -----------------------------------------------------------------------------------------------------------------
    #    Function: removeCalendar(self, ctx, userEmail)
    #    Description: removes specified user from shared Google Calendar
    #    Inputs:
    #       - ctx: context of the command
    #       - target: calendar to modify
    #       - userEmail: user to remove from target Google Calendar
    #    Outputs:
    #       - Confirmation string for successful removal, error string for failure.
    # -----------------------------------------------------------------------------------------------------------------
    @commands.has_role("Instructor")
    @commands.command(
        name="removeCalendar",
        help="Removes user from shared Google Calendar. Ex: removeCalendar john.doe@gmail.com",
    )
    async def removeCalendar(self, ctx, userEmail):
        creds = self.credsSetUp()
        try:
            service = build("calendar", "v3", credentials=creds)
            calendar = os.getenv("CALENDAR_ID")
            acl_rule_id = None
            # Get the list of ACL rules (permissions) for the calendar.
            acl_list = service.acl().list(calendarId=calendar).execute()
            for acl_rule in acl_list.get("items", []):
                if (
                    acl_rule["scope"]["type"] == "user"
                    and acl_rule["scope"]["value"] == userEmail
                ):
                    acl_rule_id = acl_rule["id"]
                    break
            if acl_rule_id:
                # Delete the ACL rule (permission) to remove the user from the calendar.
                service.acl().delete(calendarId=calendar, ruleId=acl_rule_id).execute()
                print(f"User '{userEmail}' has been removed from the calendar.")
            else:
                print(
                    f"User '{userEmail}' was not found in the calendar's permissions."
                )
        except HttpError as e:
            print(f"An error occurred: {str(e)}")


async def setup(bot):
    n = Calendar(bot)
    await bot.add_cog(n)
