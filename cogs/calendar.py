# Copyright (c) 2023 nfoster1492
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

    # -----------------------------------------------------------------------------------------------------------------
    #    Function: credsSetUp(self)
    #    Description: Sets up the credentials for all calendar actions
    #    Outputs:
    #       - The credentials needed to access the google calendar api calls
    # -----------------------------------------------------------------------------------------------------------------
    def credsSetUp(self):
        """Set up Google Calendar with authentication"""
        # If modifying these scopes, delete the file token.json.
        SCOPES = ["https://www.googleapis.com/auth/calendar"]

        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        # If there are no (valid) credentials available, let the user log in.
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
            with open("cogs/token.json", "w", encoding="utf-8") as token:
                token.write(creds.to_json())
        return creds

    # -----------------------------------------------------------------------------------------------------------------
    #    Function: addCalendarEvent(self, ctx, name, description, eventTime)
    #    Description: adds an event to the Google Calendar specified in .env configuration
    #    Inputs:
    #       - ctx: context of the command
    #       - name: name of event
    #       - decription: description of event
    #       - eventTime: Time of event
    #    Outputs:
    #       - Event added to calendar
    # -----------------------------------------------------------------------------------------------------------------
    @commands.command(
        name="addCalendarEvent",
        help="Add an event to the course calendar using the format"
        ": $addCalendarEvent NAME DESCRIPTION DATE/TIME",
    )
    async def addCalendarEvent(self, ctx, name, description, eventTime):
        """Adds specified event to shared Google Calendar"""
        creds = self.credsSetUp()
        try:
            calendar = os.getenv("CALENDAR_ID")
            service = build("calendar", "v3", credentials=creds)
            event = {
                "summary": name,
                "description": description,
                "colorId": 4,
                "start": {"dateTime": str(eventTime), "timeZone": "UTC"},
                "end": {"dateTime": str(eventTime), "timeZone": "UTC"},
            }
            event = service.events().insert(calendarId=calendar, body=event).execute()
            await ctx.send(f"Event {name} added to calendar!")

        except HttpError as error:
            print(f"An error occurred: {error}")

    @commands.command(name="add_office_hours")
    # pylint: disable=too-many-arguments
    async def add_office_hours(
        self, ctx, ta_name, event_time, end_year, end_month, end_day
    ):
        creds = self.credsSetUp()
        try:
            calendar = os.getenv("CALENDAR_ID")
            service = build("calendar", "v3", credentials=creds)
            event = {
                "summary": f"{ta_name}'s office hours",
                "colorId": 2,
                "start": {"dateTime": str(event_time), "timeZone": "UTC"},
                "end": {"dateTime": str(event_time), "timeZone": "UTC"},
                "recurrence": [
                    f"RRULE:FREQ=WEEKLY;UNTIL={end_year}{end_month}{end_day}"
                ],
            }
            event = service.events().insert(calendarId=calendar, body=event).execute()
            await ctx.send(f"Office hours for {ta_name} added to calendar!")

        except HttpError as error:
            print(f"An error occurred: {error}")

    @commands.command(name="add_lectures")
    # pylint: disable=too-many-arguments
    async def add_lectures(
        self, ctx, class_name, address, event_time, end_year, end_month, end_day
    ):
        creds = self.credsSetUp()
        try:
            calendar = os.getenv("CALENDAR_ID")
            service = build("calendar", "v3", credentials=creds)
            event = {
                "summary": f"{class_name} lecture",
                "description": f"Address: {address}",
                "colorId": 2,
                "start": {"dateTime": str(event_time), "timeZone": "UTC"},
                "end": {"dateTime": str(event_time), "timeZone": "UTC"},
                "recurrence": [
                    f"RRULE:FREQ=WEEKLY;UNTIL={end_year}{end_month}{end_day}"
                ],
            }
            event = service.events().insert(calendarId=calendar, body=event).execute()
            await ctx.send(f"Lecture for {class_name} added to calendar!")

        except HttpError as error:
            print(f"An error occurred: {error}")

    # -----------------------------------------------------------------------------------------------------------------
    #    Function: clearCalendar(self, ctx)
    #    Description: clears all events from the google calendar
    #    Inputs:
    #       - ctx: context of the command
    #    Outputs:
    #       - Whether the command was a success or a failure
    # -----------------------------------------------------------------------------------------------------------------
    @commands.command(name="clearCalendar", help="Clear all events from calendar")
    async def clearCalendar(self, ctx):
        """Clears all events from shared Google Calendar"""
        creds = self.credsSetUp()
        try:
            page_token = None
            calendar = os.getenv("CALENDAR_ID")
            service = build("calendar", "v3", credentials=creds)
            calendar_events = []
            while True:
                events = (
                    service.events()
                    .list(calendarId=calendar, pageToken=page_token)
                    .execute()
                )
                for event in events["items"]:
                    calendar_events.append(event["id"])
                page_token = events.get("nextPageToken")
                if not page_token:
                    break

            for cid in calendar_events:
                service.events().delete(calendarId=calendar, eventId=cid).execute()
            await ctx.send("Calendar has been cleared")

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
        """Generates an ICAL file of the Google Calendar"""
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
        """Sends a pdf file of the class calendar to the Discord Channel"""
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
                await ctx.send("No upcoming events found.")
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
    @tasks.loop(hours=24)
    async def checkForEvents(self):
        """Checks calendar daily for the events due that day"""
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
        help="Adds user to shared Google Calendar. Ex: subscribeCalendar john.doe@gmail.com",
    )
    async def subscribeCalendar(self, ctx, userEmail):
        """Adds user to shared Google Calendar"""
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

            await ctx.author.send(f"Added {userEmail} to the calendar.")
        except HttpError as e:
            print(f"An error occurred: {e}")
            await ctx.author.send(
                f"Error adding user: {userEmail} is not a valid email."
            )

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
        """Removes user from shared Google Calendar"""
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
                await ctx.author.send(
                    f"User {userEmail} has been removed from the calendar."
                )
            else:
                await ctx.author.send(
                    f"User {userEmail} was not found in the calendar's permissions."
                )
        except HttpError as e:
            print(f"An error occurred: {e}")
            await ctx.author.send(
                f"Error removing user: {userEmail} is not a valid email."
            )


async def setup(bot):
    """Adds the file to the bot's cog system"""
    n = Calendar(bot)
    await bot.add_cog(n)
