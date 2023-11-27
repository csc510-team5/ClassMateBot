# Copyright (c) 2021 War-Keeper
import discord
import os
import asyncio
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import discord.ext.test as dpytest
from dotenv import load_dotenv
import pytest
from PyPDF2 import PdfReader
from discord.ext import commands
import vobject

import db


# ------------------------------------------------------------------------------------------------------
# Main file bot testing. Uses dpytest to test bot activity on a simulated server with simulated members
# ------------------------------------------------------------------------------------------------------


# -------------------
# Tests cogs/ping.py
# -------------------
@pytest.mark.asyncio
async def test_ping(bot):
    await dpytest.message("$ping")
    assert dpytest.verify().message().contains().content("Pong!")


# TODO Test user join messages


# ---------------------
# Tests cogs/groups.py
# ---------------------
@pytest.mark.asyncio
async def test_groupJoin(bot):
    # first leave all groups just in case in any
    await dpytest.message("$leave")
    dpytest.get_message()

    # Try to join a group
    await dpytest.message("$join 99")
    assert (
        dpytest.verify()
        .message()
        .content("You are now in Group 99! There are now 1/6 members.")
    )

    # try to join a different group
    await dpytest.message("$join 1")
    assert dpytest.verify().message().content("You are already in Group 99")

    # leave your group
    await dpytest.message("$leave")
    assert dpytest.verify().message().content("You have been removed from Group 99!")

    # leave with no group
    await dpytest.message("$leave")
    assert dpytest.verify().message().content("You are not in a group!")

    # Reset Groups
    await dpytest.message("$reset")
    print(dpytest.get_message())
    assert dpytest.verify().message().content("Roles deleted!")

    await dpytest.message("$startupgroups")
    print(dpytest.get_message())

    await dpytest.message("$connect")


# ------------------------------------
# Tests cogs/groups.py error handling
# ------------------------------------
@pytest.mark.asyncio
async def test_groupError(bot):
    # Try to join a group that doesn't exist
    await dpytest.message("$join -1")
    assert dpytest.verify().message().content("Not a valid group")
    assert (
        dpytest.verify()
        .message()
        .content(
            "To use the join command, do: $join <Num> where 0 <= <Num> <= 99 \n ( For example: $join 0 )"
        )
    )

    with pytest.raises(commands.MissingRequiredArgument):
        await dpytest.message("$join")
    assert (
        dpytest.verify()
        .message()
        .content("To use the join command, do: $join <Num> \n ( For example: $join 0 )")
    )


# ---------------------
# Tests cogs/assignments.py
# ---------------------
@pytest.mark.asyncio
async def test_assignments(bot):
    # create instuctor user
    user = dpytest.get_config().members[0]
    guild = dpytest.get_config().guilds[0]
    irole = await guild.create_role(name="Instructor")
    await irole.edit(permissions=discord.Permissions(8))
    role = discord.utils.get(guild.roles, name="Instructor")
    await dpytest.add_role(user, role)
    # Set up grade categories
    await dpytest.message("$addgradecategory Homework 0.3")
    assert (
        dpytest.verify()
        .message()
        .content("A grading category has been added for: Homework  with weight: 0.3 ")
    )
    await dpytest.message("$addgradecategory Project 0.7")
    assert (
        dpytest.verify()
        .message()
        .content("A grading category has been added for: Project  with weight: 0.7 ")
    )
    ##Adding Assignments
    # Test adding a valid assignment with new category
    await dpytest.message("$addassignment HW1 Homework 30")
    assert (
        dpytest.verify()
        .message()
        .content(
            "A grading assignment has been added for: HW1  with points: 30 and category: Homework"
        )
    )
    # Test adding into an existing category
    await dpytest.message("$addassignment HW2 Homework 30")
    assert (
        dpytest.verify()
        .message()
        .content(
            "A grading assignment has been added for: HW2  with points: 30 and category: Homework"
        )
    )
    ##Editing Assignments
    # Test editing an assignment points
    await dpytest.message("$editassignment HW2 Homework 20")
    assert (
        dpytest.verify()
        .message()
        .content(
            "HW2 assignment has been updated with points:20 and category: Homework"
        )
    )
    # Test editing an assignment category
    await dpytest.message("$editassignment HW1 Project 70")
    assert (
        dpytest.verify()
        .message()
        .content("HW1 assignment has been updated with points:70 and category: Project")
    )
    ##Deleting Assignments
    # Test deleting an assignment
    await dpytest.message("$deleteassignment HW1")
    assert dpytest.verify().message().content("HW1 assignment has been deleted ")


# ---------------------
# Tests cogs/assignments.py
# ---------------------
@pytest.mark.asyncio
async def test_assignments_error(bot):
    # create instuctor user
    user = dpytest.get_config().members[0]
    guild = dpytest.get_config().guilds[0]
    irole = await guild.create_role(name="Instructor")
    await irole.edit(permissions=discord.Permissions(8))
    role = discord.utils.get(guild.roles, name="Instructor")
    await dpytest.add_role(user, role)
    # Set up grade categories
    await dpytest.message("$addgradecategory Homework 0.3")
    assert (
        dpytest.verify()
        .message()
        .content("A grading category has been added for: Homework  with weight: 0.3 ")
    )
    await dpytest.message("$addgradecategory Project 0.7")
    assert (
        dpytest.verify()
        .message()
        .content("A grading category has been added for: Project  with weight: 0.7 ")
    )
    ##Adding Assignments
    # Test invalid points
    await dpytest.message("$addassignment HW2 Homework points")
    assert dpytest.verify().message().content("Points could not be parsed")
    await dpytest.message("$addassignment HW3 Homework -1")
    assert (
        dpytest.verify()
        .message()
        .content("Assignment points must be greater than or equal to zero")
    )
    # Test invalid parameters
    with pytest.raises(commands.MissingRequiredArgument):
        await dpytest.message("$addassignment HW1 Homework")
    assert (
        dpytest.verify()
        .message()
        .content(
            "To use the addassignment command, do: $addassignment <assignmentname> <categoryname> <points> \n ( For example: $addassignment test1 tests 100 )"
        )
    )
    # Test duplicate assignment
    await dpytest.message("$addassignment HW2 Homework 20")
    assert (
        dpytest.verify()
        .message()
        .content(
            "A grading assignment has been added for: HW2  with points: 20 and category: Homework"
        )
    )
    await dpytest.message("$addassignment HW2 Homework 20")
    assert (
        dpytest.verify().message().content("This assignment has already been added..!!")
    )
    ##Editing Assignments
    # Test invalid points
    await dpytest.message("$editassignment HW2 Homework points")
    assert dpytest.verify().message().content("Points could not be parsed")
    await dpytest.message("$editassignment HW2 Homework -1")
    assert (
        dpytest.verify()
        .message()
        .content("Assignment points must be greater than or equal to zero")
    )
    # Test assignment that does not exist
    await dpytest.message("$editassignment HW1 Homework 30")
    assert dpytest.verify().message().content("This assignment does not exist")
    # Test invalid parameters
    with pytest.raises(commands.MissingRequiredArgument):
        await dpytest.message("$editassignment HW2 Homework")
    assert (
        dpytest.verify()
        .message()
        .content(
            "To use the editassignment command, do: $editassignment <assignmentname> <categoryname> <points> \n ( For example: $editassignment test1 tests 95 )"
        )
    )
    ##Deleting Assignments
    # Test non existing assignment
    await dpytest.message("$deleteassignment HW1")
    assert dpytest.verify().message().content("This assignment does not exist")
    # Test invalid parameters
    with pytest.raises(commands.MissingRequiredArgument):
        await dpytest.message("$deleteassignment")
    assert (
        dpytest.verify()
        .message()
        .content(
            "To use the deleteassignment command, do: $deleteassignment <assignmentname>\n ( For example: $deleteassignment test1)"
        )
    )


# -----------------------
# Tests cogs/grades.py
# -----------------------
@pytest.mark.asyncio
async def test_gradesStudent(bot):
    # create instuctor user
    user = dpytest.get_config().members[0]
    guild = dpytest.get_config().guilds[0]
    irole = await guild.create_role(name="Instructor")
    await irole.edit(permissions=discord.Permissions(8))
    role = discord.utils.get(guild.roles, name="Instructor")
    await dpytest.add_role(user, role)
    await dpytest.message("$addgradecategory Homework 0.3")
    assert (
        dpytest.verify()
        .message()
        .content("A grading category has been added for: Homework  with weight: 0.3 ")
    )
    await dpytest.message("$addassignment HW1 Homework 30")
    assert (
        dpytest.verify()
        .message()
        .content(
            "A grading assignment has been added for: HW1  with points: 30 and category: Homework"
        )
    )
    await guild.create_role(name="unverified")
    await guild.create_role(name="verified")
    role = discord.utils.get(guild.roles, name="unverified")
    await dpytest.add_role(user, role)
    channel = await guild.create_text_channel("general")
    await dpytest.message("$verify TestUser0", channel=channel)
    assert dpytest.verify().message().contains().content("Thank you for verifying!")
    # this is to clear the empty spot on the queue
    dpytest.get_message()
    await dpytest.message("$inputgrades HW1 TestingTrue ../test/data/grades.csv")
    assert dpytest.verify().message().contains().content("Entered grades for")
    await dpytest.message("$grade HW1")
    assert dpytest.verify().message().content("Grade for HW1: 25%, worth 30 points")
    await dpytest.message("$gradebycategory Homework")
    assert dpytest.verify().message().content("Grade for Homework: 25.00%")
    await dpytest.message("$gradeforclass")
    assert dpytest.verify().message().content("Grade for class: 7.50%")
    await dpytest.message("$graderequired Homework 50 30")
    assert (
        dpytest.verify()
        .message()
        .content("Grade on next assignment needed to keep 30% in Homework: 33.00%")
    )
    await dpytest.message("$graderequiredforclass Homework 50  60")
    assert (
        dpytest.verify()
        .message()
        .content("Grade on next assignment needed to keep 60%: 305.00%")
    )
    await dpytest.message("$categories")
    assert dpytest.verify().message().content("Category | Weight")
    assert dpytest.verify().message().content("================")
    assert dpytest.verify().message().content("Homework | 0.300")


# -----------------------
# Tests cogs/grades.py
# -----------------------
@pytest.mark.asyncio
async def test_gradesStudentError(bot):
    # create instuctor user
    user = dpytest.get_config().members[0]
    guild = dpytest.get_config().guilds[0]
    irole = await guild.create_role(name="Instructor")
    await irole.edit(permissions=discord.Permissions(8))
    role = discord.utils.get(guild.roles, name="Instructor")
    await dpytest.add_role(user, role)
    await dpytest.message("$addgradecategory Homework 0.3")
    assert (
        dpytest.verify()
        .message()
        .content("A grading category has been added for: Homework  with weight: 0.3 ")
    )
    await dpytest.message("$addassignment HW1 Homework 30")
    assert (
        dpytest.verify()
        .message()
        .content(
            "A grading assignment has been added for: HW1  with points: 30 and category: Homework"
        )
    )
    await guild.create_role(name="unverified")
    await guild.create_role(name="verified")
    role = discord.utils.get(guild.roles, name="unverified")
    await dpytest.add_role(user, role)
    channel = await guild.create_text_channel("general")
    await dpytest.message("$verify TestUser0", channel=channel)
    assert dpytest.verify().message().contains().content("Thank you for verifying!")
    # this is to clear the empty spot on the queue
    dpytest.get_message()
    await dpytest.message("$inputgrades HW1 TestingTrue ../test/data/grades.csv")
    assert dpytest.verify().message().contains().content("Entered grades for")
    with pytest.raises(commands.MissingRequiredArgument):
        await dpytest.message("$grade")
    assert (
        dpytest.verify()
        .message()
        .content(
            "To use the grade command, do: $grade <assignmentname>\n ( For example: $grade test1 )"
        )
    )
    await dpytest.message("$grade FakeHW")
    assert dpytest.verify().message().content("Grade for FakeHW does not exist")
    with pytest.raises(commands.MissingRequiredArgument):
        await dpytest.message("$gradebycategory")
    assert (
        dpytest.verify()
        .message()
        .content(
            "To use the gradebycategory command, do: $gradebycategory <categoryname>\n ( For example: $gradebycategory tests )"
        )
    )
    await dpytest.message("$gradebycategory FakeCat")
    assert dpytest.verify().message().content("Grades for FakeCat do not exist")
    with pytest.raises(commands.MissingRequiredArgument):
        await dpytest.message("$graderequired")
    assert (
        dpytest.verify()
        .message()
        .content(
            "To use the graderequired command, do: $graderequired <categoryname> <pointsvalue> <desiredgrade>\n ( For example: $graderequired tests 200 90 )"
        )
    )
    with pytest.raises(commands.MissingRequiredArgument):
        await dpytest.message("$graderequiredforclass")
    assert (
        dpytest.verify()
        .message()
        .content(
            "To use the graderequiredforclass command, do: $graderequiredforclass <categoryname> <pointsvalue> <desiredgrade>\n ( For example: $graderequiredforclass tests 200 90 )"
        )
    )
    await dpytest.message("$graderequiredforclass Testing33 50  60")
    assert dpytest.verify().message().content("Grades for Testing33 do not exist")


# -----------------------
# Tests cogs/grades.py
# -----------------------
@pytest.mark.asyncio
async def test_gradesInstructor(bot):
    # create instuctor user
    user = dpytest.get_config().members[0]
    guild = dpytest.get_config().guilds[0]
    irole = await guild.create_role(name="Instructor")
    await irole.edit(permissions=discord.Permissions(8))
    role = discord.utils.get(guild.roles, name="Instructor")
    await dpytest.add_role(user, role)
    await dpytest.message("$addgradecategory Homework 0.2")
    assert (
        dpytest.verify()
        .message()
        .content("A grading category has been added for: Homework  with weight: 0.2 ")
    )
    await dpytest.message("$editgradecategory Homework 0.3")
    assert (
        dpytest.verify()
        .message()
        .content("Homework category has been updated with weight:0.3 ")
    )
    await dpytest.message("$addgradecategory Exams 0.7")
    assert (
        dpytest.verify()
        .message()
        .content("A grading category has been added for: Exams  with weight: 0.7 ")
    )
    await dpytest.message("$addgradecategory Projects 0.5")
    assert (
        dpytest.verify()
        .message()
        .content("A grading category has been added for: Projects  with weight: 0.5 ")
    )
    await dpytest.message("$deletegradecategory Projects")
    assert dpytest.verify().message().content("Projects category has been deleted ")
    await dpytest.message("$addassignment Midterm1 Exams 100")
    assert (
        dpytest.verify()
        .message()
        .content(
            "A grading assignment has been added for: Midterm1  with points: 100 and category: Exams"
        )
    )
    await dpytest.message("$addassignment HW1 Homework 10")
    assert (
        dpytest.verify()
        .message()
        .content(
            "A grading assignment has been added for: HW1  with points: 10 and category: Homework"
        )
    )

    await dpytest.message("$categories")
    assert dpytest.verify().message().contains().content("Category | Weight")
    assert dpytest.verify().message().contains().content("================")
    assert dpytest.verify().message().contains().content("Exams | 0.700")
    assert dpytest.verify().message().contains().content("Homework | 0.300")

    # Create TestUser0
    await guild.create_role(name="unverified")
    await guild.create_role(name="verified")
    role = discord.utils.get(guild.roles, name="unverified")
    await dpytest.add_role(user, role)
    channel = await guild.create_text_channel("general")
    await dpytest.message("$verify TestUser0", channel=channel)
    assert dpytest.verify().message().contains().content("Thank you for verifying!")

    # this is to clear the empty spot on the queue
    dpytest.get_message()

    # Enters new grade and editing existing grade
    await dpytest.message("$inputgrades HW1 TestingTrue ../test/data/hwGrades.csv")
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("Entered grades for HW1, 1 new grades entered, 1 grades edited")
    )

    await dpytest.message(
        "$inputgrades Midterm1 TestingTrue ../test/data/examGrades.csv"
    )
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("Invalid grade value for student TestUser0, skipping entry")
    )
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("Invalid student name InvalidUser0, skipping entry")
    )
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("Entered grades for Midterm1, 1 new grades entered, 0 grades edited")
    )

    # await dpytest.message("$gradereportcategory")
    # assert dpytest.verify().message().contains().content("Grade Breakdown by Category")
    # assert dpytest.verify().message().contains().content("Exams | Average:")
    # assert dpytest.verify().message().contains().content("Homework | Average:")

    # await dpytest.message("$gradereportassignment")
    # assert (
    #     dpytest.verify().message().contains().content("Grade Breakdown by Assignment")
    # )
    # assert dpytest.verify().message().contains().content("HW1 | Average:")
    # assert dpytest.verify().message().contains().content("Midterm1 | Average:")


# -----------------------
# Tests cogs/grades.py
# -----------------------
@pytest.mark.asyncio
async def test_gradesInstructorError(bot):
    # pytest.set_trace()
    # create instuctor user
    user = dpytest.get_config().members[0]
    guild = dpytest.get_config().guilds[0]
    irole = await guild.create_role(name="Instructor")
    await irole.edit(permissions=discord.Permissions(8))
    role = discord.utils.get(guild.roles, name="Instructor")
    await dpytest.add_role(user, role)
    await dpytest.message("$addgradecategory Homework 0.2")
    assert (
        dpytest.verify()
        .message()
        .content("A grading category has been added for: Homework  with weight: 0.2 ")
    )
    await dpytest.message("$addgradecategory Homework asdf")
    assert dpytest.verify().message().content("Weight could not be parsed")
    await dpytest.message("$addgradecategory Homework -1")
    assert dpytest.verify().message().content("Weight must be greater than 0")
    await dpytest.message("$addgradecategory Homework 0.5")
    assert (
        dpytest.verify().message().content("This category has already been added..!!")
    )
    with pytest.raises(commands.MissingRequiredArgument):
        await dpytest.message("$addgradecategory")
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("To use the gradecategory command")
    )
    await dpytest.message("$editgradecategory Homework asdf")
    assert dpytest.verify().message().content("Weight could not be parsed")
    await dpytest.message("$editgradecategory Homework -1")
    assert dpytest.verify().message().content("Weight must be greater than 0")
    await dpytest.message("$editgradecategory Invalid 0.5")
    assert dpytest.verify().message().content("This category does not exist")
    with pytest.raises(commands.MissingRequiredArgument):
        await dpytest.message("$editgradecategory")
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("To use the editgradecategory command")
    )
    await dpytest.message("$deletegradecategory Invalid")
    assert dpytest.verify().message().content("This category does not exist")
    with pytest.raises(commands.MissingRequiredArgument):
        await dpytest.message("$deletegradecategory")
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("To use the deletegradecategory command")
    )
    with pytest.raises(commands.MissingRequiredArgument):
        await dpytest.message("$inputgrades")
    assert (
        dpytest.verify().message().contains().content("To use the inputgrades command")
    )


# -----------------------
# Tests cogs/deadline.py
# -----------------------
@pytest.mark.asyncio
async def test_deadline(bot):
    # create instuctor user
    user = dpytest.get_config().members[0]
    guild = dpytest.get_config().guilds[0]
    irole = await guild.create_role(name="Instructor")
    await irole.edit(permissions=discord.Permissions(8))
    role = discord.utils.get(guild.roles, name="Instructor")
    await dpytest.add_role(user, role)
    # Clear our reminders: Only if testing fails and leaves a reminders.JSON file with values behind
    # await dpytest.message("$clearreminders")
    # assert dpytest.verify().message().contains().content("All reminders have been cleared..!!")
    # Test reminders while none have been set
    await dpytest.message("$coursedue CSC505")
    assert (
        dpytest.verify()
        .message()
        .content("Rejoice..!! You have no pending reminders for CSC505..!!")
    )
    # Test setting 1 reminder
    await dpytest.message("$duedate CSC505 DANCE SEP 21 2050 10:00")
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content(
            "A date has been added for: CSC505 reminder named: DANCE which is due on: 2050-09-21 10:00:00"
        )
    )
    # Test setting a 2nd reminder
    await dpytest.message("$duedate CSC510 HW1 DEC 21 2050 19:59")
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content(
            "A date has been added for: CSC510 reminder named: HW1 which is due on: 2050-12-21 19:59:00"
        )
    )
    # Test deleting reminder
    await dpytest.message("$deletereminder CSC510 HW1")
    assert (
        dpytest.verify()
        .message()
        .content(
            "Following reminder has been deleted: Course: CSC510, reminder Name: HW1, Due Date: 2050-12-21 19:59:00"
        )
    )
    # Test re-adding a reminder
    await dpytest.message("$duedate CSC510 HW1 DEC 21 2050 19:59")
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content(
            "A date has been added for: CSC510 reminder named: HW1 which is due on: 2050-12-21 19:59:00"
        )
    )

    # Test adding an assignment twice
    await dpytest.message("$duedate CSC510 HW1 DEC 21 2050 19:59")
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("This reminder has already been added..!!")
    )

    # Clear reminders at the end of testing since we're using a local JSON file to store them
    await dpytest.message("$clearreminders")
    assert dpytest.verify().message().content("All reminders have been cleared..!!")


# --------------------------------
# Test listing multiple reminders
# --------------------------------
@pytest.mark.asyncio
async def test_listreminders(bot):
    # create instuctor user
    user = dpytest.get_config().members[0]
    guild = dpytest.get_config().guilds[0]
    irole = await guild.create_role(name="Instructor")
    await irole.edit(permissions=discord.Permissions(8))
    role = discord.utils.get(guild.roles, name="Instructor")
    await dpytest.add_role(user, role)
    # Test listing multiple reminders
    await dpytest.message("$duedate CSC505 DANCE SEP 21 2050 10:00")
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content(
            "A date has been added for: CSC505 reminder named: DANCE which is due on: 2050-09-21 10:00:00"
        )
    )
    # Test setting a 2nd reminder
    await dpytest.message("$duedate CSC510 HW1 DEC 21 2050 19:59")
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content(
            "A date has been added for: CSC510 reminder named: HW1 which is due on: "
        )
    )
    await dpytest.message("$listreminders")
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("CSC505 reminder named: DANCE which is due on:")
    )
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("CSC510 reminder named: HW1 which is due on:")
    )
    # Test $coursedue
    await dpytest.message("$coursedue CSC505")
    assert dpytest.verify().message().contains().content("DANCE is due at ")
    # Clear reminders at the end of testing since we're using a local JSON file to store them
    await dpytest.message("$clearreminders")
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("All reminders have been cleared..!!")
    )

    # Tests cogs/deadline.py


# ------------------------------
# Tests reminders due this week
# ------------------------------
@pytest.mark.asyncio
async def test_duethisweek(bot):
    # create instuctor user
    user = dpytest.get_config().members[0]
    guild = dpytest.get_config().guilds[0]
    irole = await guild.create_role(name="Instructor")
    await irole.edit(permissions=discord.Permissions(8))
    role = discord.utils.get(guild.roles, name="Instructor")
    await dpytest.add_role(user, role)
    # Try adding a reminder due in an hour
    now = datetime.now() + timedelta(hours=1)
    dt_string = now.strftime("%b %d %Y %H:%M")
    await dpytest.message(f"$duedate CSC600 HW0 {dt_string}")
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("A date has been added for: CSC600 reminder named: HW0")
    )
    # Check to see that the reminder is due this week
    await dpytest.message("$duethisweek")
    assert dpytest.verify().message().contains().content("CSC600 HW0 is due ")
    # Clear reminders at the end of testing since we're using a local JSON file to store them
    await dpytest.message("$clearreminders")
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("All reminders have been cleared..!!")
    )


# ------------------------------
# Tests reminders due today
# ------------------------------
@pytest.mark.asyncio
async def test_duetoday(bot):
    # create instuctor user
    user = dpytest.get_config().members[0]
    guild = dpytest.get_config().guilds[0]
    irole = await guild.create_role(name="Instructor")
    await irole.edit(permissions=discord.Permissions(8))
    role = discord.utils.get(guild.roles, name="Instructor")
    await dpytest.add_role(user, role)
    # Try adding a reminder due in an hour
    now = datetime.now() + timedelta(hours=6)
    dt_string = now.strftime("%b %d %Y %H:%M")
    await dpytest.message(f"$duedate CSC600 HW0 {dt_string}")
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("A date has been added for: CSC600 reminder named: HW0")
    )
    # Check to see that the reminder is due today
    await dpytest.message("$duetoday")
    assert dpytest.verify().message().contains().content("CSC600 HW0 is due ")
    # Clear reminders at the end of testing since we're using a local JSON file to store them
    await dpytest.message("$clearreminders")
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("All reminders have been cleared..!!")
    )


# ------------------------------
# Tests overdue reminders
# ------------------------------
@pytest.mark.asyncio
async def test_overdue(bot):
    # create instuctor user
    user = dpytest.get_config().members[0]
    guild = dpytest.get_config().guilds[0]
    irole = await guild.create_role(name="Instructor")
    await irole.edit(permissions=discord.Permissions(8))
    role = discord.utils.get(guild.roles, name="Instructor")
    await dpytest.add_role(user, role)
    # Try adding a reminder due in the past
    await dpytest.message("$duedate CSC600 HW0 SEP 21 2000 10:00")
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("A date has been added for: CSC600 reminder named: HW0")
    )
    # Check to see that the reminder is overdue
    await dpytest.message("$overdue")
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content(
            "CSC600 reminder named: HW0 which was due on: Sep 21 2000 10:00:00+0000"
        )
    )
    # Clear reminders at the end of testing since we're using a local JSON file to store them
    await dpytest.message("$clearoverdue")
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("All overdue reminders have been cleared..!!")
    )
    # Confirm overdue was removed
    await dpytest.message("$overdue")
    assert (
        dpytest.verify().message().contains().content("There are no overdue reminders")
    )


# ------------------------------
# Tests deadline errors
# ------------------------------
@pytest.mark.asyncio
async def test_deadline_errors(bot):
    # create instuctor user
    user = dpytest.get_config().members[0]
    guild = dpytest.get_config().guilds[0]
    irole = await guild.create_role(name="Instructor")
    await irole.edit(permissions=discord.Permissions(8))
    role = discord.utils.get(guild.roles, name="Instructor")
    await dpytest.add_role(user, role)

    # Tests timenow without an argument
    with pytest.raises(commands.MissingRequiredArgument):
        await dpytest.message("$timenow")
    assert (
        dpytest.verify()
        .message()
        .content(
            "To use the timenow command (with current time), do: "
            "$timenow MMM DD YYYY HH:MM ex. $timenow SEP 25 2024 17:02"
        )
    )

    # Test timenow with bad argument
    # with pytest.raises(commands.MissingRequiredArgument):
    await dpytest.message("$timenow blab")
    assert dpytest.verify().message().content("Due date could not be parsed")

    # Test duedate with bad argument
    # with pytest.raises(commands.MissingRequiredArgument):
    await dpytest.message("$duedate blab blab blab")
    assert dpytest.verify().message().content("Due date could not be parsed")
    # Tests duedate without an argument
    with pytest.raises(commands.MissingRequiredArgument):
        await dpytest.message("$duedate")
    assert (
        dpytest.verify()
        .message()
        .content(
            "To use the duedate command, do: $duedate CLASSNAME NAME MMM DD YYYY optional(HH:MM) optional(TIMEZONE)\n ( For example: $duedate CSC510 HW2 SEP 25 2024 17:02 EST )"
        )
    )

    # Tests deletereminder without an argument
    with pytest.raises(commands.MissingRequiredArgument):
        await dpytest.message("$deletereminder")
    assert (
        dpytest.verify()
        .message()
        .content(
            "To use the deletereminder command, do: $deletereminder CLASSNAME HW_NAME \n "
            "( For example: $deletereminder CSC510 HW2 )"
        )
    )

    # Tests changeduedate without an argument
    with pytest.raises(commands.MissingRequiredArgument):
        await dpytest.message("$changeduedate")
    assert (
        dpytest.verify()
        .message()
        .content(
            "To use the changeduedate command, do: $changeduedate CLASSNAME HW_NAME MMM DD YYYY optional(HH:MM) optional(TIMEZONE)\n"
            " ( For example: $changeduedate CSC510 HW2 SEP 25 2024 17:02 EST)"
        )
    )

    # Test changeduedate with bad argument
    # with pytest.raises(commands.MissingRequiredArgument):
    await dpytest.message("$changeduedate blab blab blab")
    assert dpytest.verify().message().content("Due date could not be parsed")

    # Tests coursedue without an argument
    with pytest.raises(commands.MissingRequiredArgument):
        await dpytest.message("$coursedue")
    assert (
        dpytest.verify()
        .message()
        .content(
            "To use the coursedue command, do: $coursedue CLASSNAME \n ( For example: $coursedue CSC510 )"
        )
    )


# --------------------
# Tests cogs/pinning
# --------------------
@pytest.mark.asyncio
async def test_pinning(bot):
    # Test pinning a message
    await dpytest.message("$pin TestMessage www.google.com this is a test")
    # print(dpytest.get_message().content)
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content(
            "A new message has been pinned with tag: TestMessage and description: www.google.com this is a test"
        )
    )
    await dpytest.message("$pin TestMessage www.discord.com this is also a test")
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content(
            "A new message has been pinned with tag: TestMessage and description: www.discord.com this is also a test"
        )
    )

    # clean up
    # await dpytest.message("$unpin TestMessage")


# ----------------
# Tests unpinning
# ----------------
@pytest.mark.asyncio
async def test_unpinning(bot):
    # Test pinning a message
    await dpytest.message("$pin TestMessage www.google.com this is a test")
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content(
            "A new message has been pinned with tag: TestMessage and description: www.google.com this is a test"
        )
    )
    await dpytest.message("$pin TestMessage www.discord.com this is also a test")
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content(
            "A new message has been pinned with tag: TestMessage and description: www.discord.com this is also a test"
        )
    )
    # Tests unpinning a message that doesn't exist
    await dpytest.message("$unpin None")
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("No message found with the combination of tagname: None, and author:")
    )
    # Tests unpinning messages that DO exist
    await dpytest.message("$unpin TestMessage")
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("2 pinned message(s) has been deleted with tag: TestMessage")
    )


# ---------------------
# Tests updating pins
# ---------------------
@pytest.mark.asyncio
async def test_updatepin(bot):
    # Tests adding another message to update pins
    await dpytest.message("$pin TestMessage2 www.discord.com test")
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content(
            "A new message has been pinned with tag: TestMessage2 and description: www.discord.com test"
        )
    )
    # Tests updatepin
    await dpytest.message("$updatepin TestMessage2 www.zoom.com test")
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("1 pinned message(s) has been deleted with tag: TestMessage2")
    )
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content(
            "A new message has been pinned with tag: TestMessage2 and description: www.zoom.com test"
        )
    )

    # Tests updating a non-existent pin
    await dpytest.message("$updatepin Tag Test")
    # Confirm no message exists
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("No message found with the combination of tagname: Tag, and author:")
    )
    # Ensure that a message is pinned.
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("A new message has been pinned with tag: Tag and description: Test")
    )


# ------------------------
# Tests pinnedmessages
# ------------------------
@pytest.mark.asyncio
async def test_pinnedmessages(bot):
    # Tests getting pins by tag: no pinned messages
    await dpytest.message("$pinnedmessages TestTag")
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("No messages found with the given tagname and author combination")
    )

    # pin and dequeue
    await dpytest.message("$pin Tag1 never gonna give you up")
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content(
            "A new message has been pinned with tag: Tag1 and description: never gonna give you up"
        )
    )
    # pin and dequeue
    await dpytest.message("$pin Tag1 never gonna let you down")
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content(
            "A new message has been pinned with tag: Tag1 and description: never gonna let you down"
        )
    )
    # pin and dequeue
    await dpytest.message("$pin Tag2 never gonna run around and desert you")
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content(
            "A new message has been pinned with tag: Tag2 and description: never gonna run around and desert you"
        )
    )

    # Tests getting pins by tag
    await dpytest.message("$pinnedmessages Tag1")
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("Tag: Tag1, Description: never gonna give you up")
    )
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("Tag: Tag1, Description: never gonna let you down")
    )

    # Tests getting all pins
    await dpytest.message("$pinnedmessages")
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("Tag: Tag1, Description: never gonna give you up")
    )
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("Tag: Tag1, Description: never gonna let you down")
    )
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("Tag: Tag2, Description: never gonna run around and desert you")
    )


# ------------------------
# Tests pin-related errors
# ------------------------
@pytest.mark.asyncio
async def test_pinningErrors(bot):
    # Tests pinning without a message
    with pytest.raises(commands.MissingRequiredArgument):
        await dpytest.message("$pin")
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content(
            "To use the pin command, do: $pin TAGNAME DESCRIPTION \n ( For example: $pin HW8 https://"
            "discordapp.com/channels/139565116151562240/139565116151562240/890813190433292298 HW8 reminder )"
        )
    )

    # Tests unpinning without a message
    with pytest.raises(commands.MissingRequiredArgument):
        await dpytest.message("$unpin")
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content(
            "To use the unpin command, do: $unpin TAGNAME \n ( For example: $unpin HW8 )"
        )
    )

    # Tests updating a pin with invalid input
    with pytest.raises(commands.MissingRequiredArgument):
        await dpytest.message("$updatepin")
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content(
            "To use the updatepin command, do: $pin TAGNAME DESCRIPTION \n ( $updatepin HW8 https://discordapp"
            ".com/channels/139565116151562240/139565116151562240/890814489480531969 HW8 reminder )"
        )
    )

    # Tests using pinnedmessages with invalid input
    # with pytest.raises(commands.CommandError):
    # await dpytest.message("$pinnedmessages \" please fail omg")
    # assert dpytest.verify().message().contains().content(
    # "To use the pinnedmessages command, do: $pinnedmessages:"
    # " TAGNAME \n ( For example: $pinnedmessages HW8 )")

    # The above test requires the else statement below to be included
    # in pinning.py's retrieveMessages_error function.

    # @retrieveMessages.error
    # async def retrieveMessages_error(self, ctx, error):
    # if isinstance(error, commands.MissingRequiredArgument):
    # ...
    # else:
    # await ctx.send(
    # "To use the pinnedmessages command, do: $pinnedmessages:"
    # " TAGNAME \n ( For example: $pinnedmessages HW8 )")
    # print(error)


# --------------------
# Tests cogs/newComer
# --------------------


@pytest.mark.asyncio
async def test_verify(bot):
    user = dpytest.get_config().members[0]
    guild = dpytest.get_config().guilds[0]
    channel = await guild.create_text_channel("general")

    await dpytest.message("$verify Student Name", channel=channel)
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content(
            "Warning: Please make sure the verified and unverified roles exist in this server!"
        )
    )

    # Test self-verification - unverified role assigned
    await guild.create_role(name="unverified")
    await guild.create_role(name="verified")
    role = discord.utils.get(guild.roles, name="unverified")
    await dpytest.add_role(user, role)
    await dpytest.message("$verify Student Name", channel=channel)
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content(f"Thank you for verifying! You can start using {guild.name}!")
    )
    dpytest.get_message()


@pytest.mark.asyncio
async def test_verifyNoName(bot):
    guild = dpytest.get_config().guilds[0]
    await guild.create_role(name="unverified")
    await guild.create_role(name="verified")
    # Test verification without proper argument given
    await dpytest.message("$verify")
    # print(dpytest.get_message().content)
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content(
            "To use the verify command, do: $verify <FirstName LastName> \n ( For example: $verify Jane Doe )"
        )
    )


# We cannot currently test newComer.py in a meaningful way due to not having a way to DM the test bot directly,
# as well as inability to have dpytest add/remove roles to test specific cases


# --------------------
# Tests cogs/Voting
# --------------------
@pytest.mark.asyncio
async def test_voting(bot):
    # Test voting
    await dpytest.message(content="$vote 1")
    assert (
        dpytest.verify()
        .message()
        .content(
            "You are not in a group. You must join a group before voting on a project."
        )
    )
    await dpytest.message("$join 99")
    dpytest.get_message()
    await dpytest.message(content="$vote 1")
    assert dpytest.verify().message().content("Group 99 has voted for Project 1!")
    await dpytest.message(content="$vote 2")
    assert dpytest.verify().message().content("Group 99 removed vote for Project 1")
    assert dpytest.verify().message().content("Group 99 has voted for Project 2!")
    await dpytest.message(content="$vote 2")
    assert dpytest.verify().message().content("You already voted for Project 2")
    with pytest.raises(commands.UserInputError):
        await dpytest.message(content="$vote")
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content(
            "To join a project, use the join command, do: $vote <Num> \n( For example: $vote 0 )"
        )
    )
    await dpytest.message(content="$vote -1")
    assert dpytest.verify().message().content("A valid project number is 1-99.")


# -------------------
# Tests cogs/qanda
# --------------------
@pytest.mark.asyncio
async def test_qanda(bot):
    # Test q and a functionalities
    # create channel and get user
    user = dpytest.get_config().members[0]
    guild = dpytest.get_config().guilds[0]
    channel = await guild.create_text_channel("q-and-a")
    irole = await guild.create_role(name="Instructor")
    await irole.edit(permissions=discord.Permissions(8))
    role = discord.utils.get(guild.roles, name="Instructor")
    await dpytest.add_role(user, role)

    # Test asking a question anonymously
    await dpytest.message('$ask "What class is this?" anonymous', channel=channel)
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("Q1: What class is this? by anonymous")
    )

    # Test asking a question with name
    await dpytest.message('$ask "When is the last day of classes?"', channel=channel)
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("Q2: When is the last day of classes? by " + user.name)
    )

    # Tests getting answers: no answers
    await dpytest.message("$getAnswersFor 1", channel=channel)
    assert dpytest.verify().message().contains().content("No answers for Q1")

    # Test answering a question
    await dpytest.message('$answer 2 "TestA"', channel=channel)
    # Test answering a question anonymously
    await dpytest.message('$answer 2 "TestB" anonymous', channel=channel)

    # Tests getting answers: question has answers
    await dpytest.message("$getAnswersFor 2", channel=channel)
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content(
            "Q2: When is the last day of classes? by "
            + user.name
            + "\n"
            + user.name
            + " (Instructor) Ans: TestA\n"
            "anonymous (Instructor) Ans: TestB\n"
        )
    )

    # Tests channelGhost: not a ghost, has answers
    await dpytest.message("$channelGhost 2", channel=channel)
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("This question is not a ghost. Fetching anyway. . .")
    )
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content(
            "Q2: When is the last day of classes? by "
            + user.name
            + "\n"
            + user.name
            + " (Instructor) Ans: TestA\n"
            "anonymous (Instructor) Ans: TestB\n"
        )
    )

    # test deleting all answers for a question with none
    await dpytest.message("$DALLAF 1", channel=channel)
    assert dpytest.verify().message().contains().content("No answers exist for Q1")

    # test deleting all answers
    await dpytest.message("$DALLAF 2", channel=channel)
    assert dpytest.verify().message().contains().content("deleted 2 answers for Q2")

    # Test reviveGhost: non-existent question
    await dpytest.message("$reviveGhost 100", channel=channel)
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("No such question with the number: 100")
    )

    # Test channelGhost: non-existent question
    await dpytest.message("$channelGhost 100", channel=channel)
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("No such question with the number: 100")
    )

    # GHOST AND ZOMBIE TESTING

    # ask and dequeue
    await dpytest.message('$ask "Am I a zombie?" anon', channel=channel)
    assert (
        dpytest.verify().message().contains().content("Q3: Am I a zombie? by anonymous")
    )

    # hold on to q3
    q3_id = channel.last_message_id
    q3 = await channel.fetch_message(q3_id)

    # Tests channelGhost: not a ghost, no answers
    await dpytest.message("$channelGhost 3", channel=channel)
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("This question is not a ghost. Fetching anyway. . .")
    )
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("Q3: Am I a zombie? by anonymous\n" "No answers for Q3\n")
    )

    # Test spooky: no ghosts or zombies
    await dpytest.message("$spooky", channel=channel)
    assert dpytest.verify().message().contains().content("This channel isn't haunted.")

    # Test unearthZombies: no zombies
    await dpytest.message("$unearthZombies", channel=channel)
    assert dpytest.verify().message().contains().content("No zombies detected.")

    # zomb-ify Q3
    await q3.delete()

    # test answering a zombie
    await dpytest.message('$answer 3 "zombie test"', channel=channel)
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("Question 3 not found. It's a zombie!")
    )

    # test getting answers for a zombie
    await dpytest.message("$getAnswersFor 3", channel=channel)
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("Question 3 not found. It's a zombie!")
    )

    # ask and dequeue
    await dpytest.message('$ask "Am I a ghost?" anonymous', channel=channel)
    assert (
        dpytest.verify().message().contains().content("Q4: Am I a ghost? by anonymous")
    )
    # answer Q4
    await dpytest.message('$answer 4 "Yes" anon', channel=channel)

    # ask and dequeue
    await dpytest.message('$ask "Zombie" anonymous', channel=channel)
    assert dpytest.verify().message().contains().content("Q5: Zombie by anonymous")

    # hold on to q5
    q5_id = channel.last_message_id
    q5 = await channel.fetch_message(q5_id)

    # answer Q5; zombie with an answer
    await dpytest.message('$answer 5 "test" anonymous', channel=channel)

    # Test deleting a question
    await dpytest.message("$deleteQuestion 4", channel=channel)
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("Q4 is now a ghost. To restore it, use: $reviveGhost 4")
    )

    # Test deleting a ghost question
    await dpytest.message("$deleteQuestion 4", channel=channel)
    assert dpytest.verify().message().contains().content("Q4 is already a ghost!")

    # test answering a ghost
    await dpytest.message('$answer 4 "Ghost Test"', channel=channel)
    assert dpytest.verify().message().contains().content("You can't answer a ghost!")

    # Test channelGhost: answers
    await dpytest.message("$channelGhost 4", channel=channel)
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("Q4: Am I a ghost? by anonymous\nanonymous (Instructor) Ans: Yes\n")
    )

    # Tests getting answers for a ghost
    await dpytest.message("$getAnswersFor 4", channel=channel)
    assert dpytest.verify().message().contains().content("Q4 is a ghost!")

    # Test allChannelGhosts: answers
    await dpytest.message("$allChannelGhosts", channel=channel)
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("Q4: Am I a ghost? by anonymous\n" "anonymous (Instructor) Ans: Yes\n")
    )

    # test deleting all answers for ghost
    await dpytest.message("$DALLAF 4", channel=channel)
    assert dpytest.verify().message().contains().content("deleted 1 answers for Q4")
    assert dpytest.verify().message().contains().content("Q4 is a ghost!")

    # Test channelGhost: no answers
    await dpytest.message("$channelGhost 4", channel=channel)
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("Q4: Am I a ghost? by anonymous\n" "No answers for Q4\n")
    )

    # Test allChannelGhosts: no answers
    await dpytest.message("$allChannelGhosts", channel=channel)
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("Q4: Am I a ghost? by anonymous\n" "No answers for Q4\n")
    )

    # Test spooky: ghosts and zombies are present
    await dpytest.message("$spooky", channel=channel)
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("This channel is haunted by 1 ghosts and 1 zombies.")
    )

    # Test archiveQA: zombie, ghost, questions with and without answers
    await dpytest.message("$archiveQA", channel=channel)
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("Q1: What class is this? by anonymous\n" "No answers for Q1\n")
    )
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content(
            "Q2: When is the last day of classes? by " + user.name + "\n"
            "No answers for Q2\n"
        )
    )
    assert (
        dpytest.verify().message().contains().content("Q3 was deleted. It's a zombie!")
    )
    assert dpytest.verify().message().contains().content("Q4 is a ghost!")
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("Q5: Zombie by anonymous\n" "anonymous (Instructor) Ans: test\n")
    )

    # Test reviving a ghost (revive without answers)
    await dpytest.message("$reviveGhost 4", channel=channel)
    # no assert needed!

    # ghosts: 0, zombies: 1

    # Test deleting a zombie (ghosts + 1, zombies -1)
    await dpytest.message("$deleteQuestion 3", channel=channel)
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("Q3 was not found in channel. To restore it, use: $reviveGhost 3")
    )

    # ghosts: 1, zombies: 0

    # zomb-ify Q5
    await q5.delete()

    # ghosts: 1, zombies: 1

    # test reviving a zombie with answers
    await dpytest.message("$reviveGhost 5", channel=channel)
    # now we can assert because a message is actually posted this time.
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("Q5: Zombie by anonymous\n" "anonymous (Instructor) Ans: test\n")
    )

    # ghosts: 1, zombies: 0

    # create another zombie
    await dpytest.message('$ask "Zombie2" anonymous', channel=channel)
    assert dpytest.verify().message().contains().content("Q6: Zombie2 by anonymous")

    # hold on to q5
    q6_id = channel.last_message_id
    q6 = await channel.fetch_message(q6_id)
    await q6.delete()

    # test unearthZombies: zombies found
    await dpytest.message("$unearthZombies", channel=channel)
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content(
            "Found 1 zombies and assigned them ghost status.\n"
            "To view them, use: $allChannelGhosts\n"
            "To restore a question, use: $reviveGhost QUESTION_NUMBER"
        )
    )

    # ghosts: 2, zombies: 0

    # create final zombie
    await dpytest.message('$ask "Zombie3" anonymous', channel=channel)
    assert dpytest.verify().message().contains().content("Q7: Zombie3 by anonymous")
    # hold on to q7
    qz_id = channel.last_message_id
    qz = await channel.fetch_message(qz_id)

    await dpytest.message('$answer 7 "test" anonymous', channel=channel)

    # zomb-ify Q7
    await qz.delete()

    # ghosts: 2, zombies: 1

    # test deleting all answers for zombie
    await dpytest.message("$DALLAF 7", channel=channel)
    assert dpytest.verify().message().contains().content("deleted 1 answers for Q7")
    assert dpytest.verify().message().contains().content("Q7 is a zombie!")

    # test deleteAllQA: questions with and without answers, ghosts and zombies
    await dpytest.message("$deleteAllQA", channel=channel)
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content(
            "Deleted 7 questions from the database, including 1 zombies and 2 ghosts."
        )
    )


# -------------------------
# Tests cogs/qanda: error testing
# -------------------------
@pytest.mark.asyncio
async def test_qanda_errors(bot):
    # Test q and a functionalities
    # create channel and get user
    user = dpytest.get_config().members[0]
    guild = dpytest.get_config().guilds[0]
    channel = await guild.create_text_channel("q-and-a")
    gen_channel = await guild.create_text_channel("general")
    irole = await guild.create_role(name="Instructor")
    await irole.edit(permissions=discord.Permissions(8))
    role = discord.utils.get(guild.roles, name="Instructor")
    await dpytest.add_role(user, role)

    # Test asking a question in the wrong channel
    msg = await dpytest.message(
        '$ask "Is this the right channel?"', channel=gen_channel
    )
    with pytest.raises(discord.NotFound):
        await gen_channel.fetch_message(msg.id)
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("Please send questions to the #q-and-a channel.")
    )

    # Tests unknown anonymous input (question)
    await dpytest.message('$ask "Who am I?" wronganon', channel=channel)
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content(
            "Unknown input for *anonymous* option. Please type **anonymous**, **anon**, or leave blank."
        )
    )

    # Tests incorrect use of ask command: missing args
    with pytest.raises(commands.MissingRequiredArgument):
        await dpytest.message("$ask", channel=channel)
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content(
            'To use the ask command, do: $ask "QUESTION" anonymous*<optional>* \n '
            '(For example: $ask "What class is this?" anonymous)'
        )
    )

    # Test answering a question in the wrong channel
    msga = await dpytest.message('$answer 1 "Test"', channel=gen_channel)
    with pytest.raises(discord.NotFound):
        await gen_channel.fetch_message(msga.id)
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("Please send answers to the #q-and-a channel.")
    )

    # Tests unknown anonymous input (answer)
    await dpytest.message('$answer 1 "A Thing" wronganon', channel=channel)
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content(
            "Unknown input for *anonymous* option. Please type **anonymous**, **anon**, or leave blank."
        )
    )

    # Tests answering a nonexistent question (answer)
    await dpytest.message('$answer 100 "nope"', channel=channel)
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("No such question with the number: 100")
    )

    # placeholder test for empty input (answer)
    # await dpytest.message("$answer 100 \"\" ", channel=channel)
    # assert dpytest.verify().message().contains().content('STRING GOES HERE')

    # Tests incorrect use of answer command: no args
    with pytest.raises(commands.MissingRequiredArgument):
        await dpytest.message("$answer", channel=channel)
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content(
            'To use the answer command, do: $answer QUESTION_NUMBER "ANSWER" anonymous*<optional>*\n '
            '(For example: $answer 2 "Yes")'
        )
    )

    # Tests answering with bad input (answer)
    await dpytest.message('$answer "nope" lol', channel=channel)
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content(
            'Please include a valid question number. EX: $answer 1 /"Oct 12/" anonymous'
        )
    )

    # Test getAnswersFor in wrong channel
    msg = await dpytest.message("$getAnswersFor 1", channel=gen_channel)
    with pytest.raises(discord.NotFound):
        await gen_channel.fetch_message(msg.id)
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("Please use this command inside the #q-and-a channel.")
    )

    # Tests getting answers for nonexistent question
    await dpytest.message("$getAnswersFor 100", channel=channel)
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("No such question with the number: 100")
    )

    # Tests getAnswersFor with bad input: no arg
    with pytest.raises(commands.MissingRequiredArgument):
        await dpytest.message("$getAnswersFor", channel=channel)
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content(
            "To use the getAnswersFor command, do: $getAnswersFor QUESTION_NUMBER\n "
            "(Example: $getAnswersFor 1)"
        )
    )

    # Tests getting answers with bad input
    await dpytest.message("$getAnswersFor abc", channel=channel)
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("Please include a valid question number. EX: $getAnswersFor 1")
    )

    # Test that deleting answers does not work outside of QA
    msg = await dpytest.message("$DALLAF 1", channel=gen_channel)
    with pytest.raises(discord.NotFound):
        await gen_channel.fetch_message(msg.id)
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("Please use this command inside the #q-and-a channel.")
    )

    # test deleting all answers with bad input: no args
    with pytest.raises(commands.MissingRequiredArgument):
        await dpytest.message("$DALLAF", channel=channel)
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content(
            "To use the deleteAllAnswersFor command, do: $DALLAF QUESTION_NUMBER\n "
            "(Example: $DALLAF 1)"
        )
    )

    # test deleting all answers with bad input
    await dpytest.message("$DALLAF abc", channel=channel)
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("Please include a valid question number. EX: $DALLAF 1")
    )

    # test deleting all answers for a non-existent question
    await dpytest.message("$DALLAF 100", channel=channel)
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("No such question with the number: 100")
    )

    # Test that deleting questions does not work outside of QA
    msg = await dpytest.message("$deleteQuestion 1", channel=gen_channel)
    with pytest.raises(discord.NotFound):
        await gen_channel.fetch_message(msg.id)
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("Please use this command inside the #q-and-a channel.")
    )

    # test deleting questions with bad input: no args
    with pytest.raises(commands.MissingRequiredArgument):
        await dpytest.message("$deleteQuestion", channel=channel)
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content(
            "To use the deleteQuestion command, do: $deleteQuestion QUESTION_NUMBER\n "
            "(Example: $deleteQuestion 1"
        )
    )

    # test deleting question with bad input
    await dpytest.message("$deleteQuestion abc", channel=channel)
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("Please include a valid question number. EX: $deleteQuestion 1")
    )

    # test deleting a non-existent question
    await dpytest.message("$deleteQuestion 100", channel=channel)
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("Question number not in database: 100")
    )

    # Test that deleting all QAs does not work outside of QA
    await dpytest.message("$deleteAllQA", channel=gen_channel)
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("Please use this command inside the #q-and-a channel.")
    )

    # Test deleting all QAs without any questions
    await dpytest.message("$deleteAllQA", channel=channel)
    assert (
        dpytest.verify().message().contains().content("No questions found in database.")
    )

    # Test archiveQA: empty database
    await dpytest.message("$archiveQA", channel=channel)
    assert (
        dpytest.verify().message().contains().content("No questions found in database.")
    )

    # Test that archiveQA does not work outside of QA
    await dpytest.message("$archiveQA", channel=gen_channel)
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("Please use this command inside the #q-and-a channel.")
    )

    # Test channelGhost in the wrong channel
    await dpytest.message("$channelGhost 1", channel=gen_channel)
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("Please use this command inside the #q-and-a channel.")
    )

    # Tests channelGhost: missing args
    with pytest.raises(commands.MissingRequiredArgument):
        await dpytest.message("$channelGhost", channel=channel)
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content(
            "To use the channelGhost command, do: $channelGhost QUESTION_NUMBER\n "
            "(Example: $channelGhost 1)"
        )
    )

    # Tests channelGhost: invalid arg
    await dpytest.message("$channelGhost blah", channel=channel)
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("Please include a valid question number. EX: $channelGhost 1")
    )

    # Tests channelGhost: empty database
    await dpytest.message("$channelGhost 1", channel=channel)
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("No such question with the number: 1")
    )

    # Test allChannelGhosts in the wrong channel
    await dpytest.message("$allChannelGhosts", channel=gen_channel)
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("Please use this command inside the #q-and-a channel.")
    )

    # allChannelGhosts without any ghosts
    await dpytest.message("$allChannelGhosts", channel=channel)
    assert dpytest.verify().message().contains().content("No ghosts found in database.")

    # Test spooky in the wrong channel
    await dpytest.message("$spooky", channel=gen_channel)
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("Please use this command inside the #q-and-a channel.")
    )

    # Test spooky: empty database
    await dpytest.message("$spooky", channel=channel)
    assert dpytest.verify().message().contains().content("This channel isn't haunted.")

    # Test unearthZombies in the wrong channel
    await dpytest.message("$unearthZombies", channel=gen_channel)
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("Please use this command inside the #q-and-a channel.")
    )

    # Test unearthZombies: empty database
    await dpytest.message("$unearthZombies", channel=channel)
    assert dpytest.verify().message().contains().content("No zombies detected.")

    # Test reviveGhost in the wrong channel
    await dpytest.message("$reviveGhost 1", channel=gen_channel)
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("Please use this command inside the #q-and-a channel.")
    )

    # Tests reviveGhost: missing args
    with pytest.raises(commands.MissingRequiredArgument):
        await dpytest.message("$reviveGhost", channel=channel)
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content(
            "To use the reviveGhost command, do: $reviveGhost QUESTION_NUMBER\n "
            "(Example: $reviveGhost 1)"
        )
    )

    # Tests reviveGhost: invalid arg
    await dpytest.message("$reviveGhost blah", channel=channel)
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("Please include a valid question number. EX: $reviveGhost 1")
    )

    # Test reviveGhost: empty database
    await dpytest.message("$reviveGhost 1", channel=channel)
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("No such question with the number: 1")
    )

    # Test ask: empty question
    await dpytest.message('$ask ""', channel=channel)
    assert (
        dpytest.verify().message().contains().content("Please enter a valid question.")
    )

    # Test ask: whitepaces only
    await dpytest.message('$ask "   "', channel=channel)
    assert (
        dpytest.verify().message().contains().content("Please enter a valid question.")
    )

    # Test ask: one char question
    await dpytest.message('$ask "A"', channel=channel)
    assert dpytest.verify().message().contains().content("Question too short.")

    # Test answer: empty answer
    await dpytest.message('$answer 1 ""', channel=channel)
    assert dpytest.verify().message().contains().content("Please enter a valid answer.")

    # Test answer: whitespaces only
    await dpytest.message('$answer 1 "    "', channel=channel)
    assert dpytest.verify().message().contains().content("Please enter a valid answer.")


# --------------------
# Tests cogs/reviewQs
# --------------------
@pytest.mark.asyncio
async def test_review_qs(bot):
    # Test review question functionalities
    # create roles and get user
    user = dpytest.get_config().members[0]
    guild = dpytest.get_config().guilds[0]
    await guild.create_role(name="Instructor")
    role = discord.utils.get(guild.roles, name="Instructor")
    await dpytest.add_role(user, role)

    # Test adding a question
    await dpytest.message('$addQuestion "What class is this?" "CSC510"', member=user)
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content(
            "A new review question has been added! Question: What class is this? and Answer: CSC510."
        )
    )

    # Test getting a question
    await dpytest.message("$getQuestion", member=user)
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("What class is this? \n ||CSC510||")
    )

    # Test error
    with pytest.raises(Exception):
        await dpytest.message('$addQuestion "Is this a test question?"', member=user)
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content(
            'To use the addQuestion command, do: $addQuestion "Question" "Answer" \n'
            '(For example: $addQuestion "What class is this?" "CSC510")'
        )
    )


# --------------------------------
# Test polling: poll
# --------------------------------
@pytest.mark.asyncio
async def test_poll(bot):
    user = dpytest.get_config().members[0]
    guild = dpytest.get_config().guilds[0]
    channel = await guild.create_text_channel("polls")

    # Test poll: no input
    await dpytest.message("$poll", channel=channel)
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("Please enter a question for your poll.")
    )

    # Test poll: whitespace
    await dpytest.message("$poll    ", channel=channel)
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("Please enter a question for your poll.")
    )

    # Test poll: question too short
    await dpytest.message("$poll ab", channel=channel)
    assert dpytest.verify().message().contains().content("Poll question too short.")

    # Test poll: student
    await dpytest.message("$poll abc", channel=channel)
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("**POLL by Student**\n\nabc\n** **")
    )

    await guild.create_role(name="Instructor")
    role = discord.utils.get(guild.roles, name="Instructor")
    await dpytest.add_role(user, role)

    # Test poll: instructor
    await dpytest.message("$poll abc", channel=channel)
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("**POLL by Instructor**\n\nabc\n** **")
    )

    # Test poll: reactions
    msgid = channel.last_message_id
    msg = await channel.fetch_message(msgid)

    # should have three reactions, but this is a known bug.
    # From dpytest: This is d.py/discord's fault, the message object from send isn't
    # the same as the one in the state
    assert len(msg.reactions) == 1


# --------------------------------
# Test polling: quizpoll
# --------------------------------
@pytest.mark.asyncio
async def test_quizpoll(bot):
    # user = dpytest.get_config().members[0]
    # guild = dpytest.get_config().guilds[0]
    # channel = await guild.create_text_channel('polls')

    # Test quizpoll: no input
    with pytest.raises(commands.MissingRequiredArgument):
        await dpytest.message("$quizpoll")
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content(
            'To use the quizpoll command, do: $quizpoll "TITLE" [option1] [option2] ... [option6]\n '
            "Be sure to enclose title with quotes and options with brackets!\n"
            'EX: $quizpoll "I am a poll" [Vote for me!] [I am option 2]'
        )
    )

    # Test quizpoll: title is whitespace
    await dpytest.message('$quizpoll "  " [a] [b] [c] [d] [e] [f]')
    assert dpytest.verify().message().contains().content("Please enter a valid title.")

    # Test quizpoll: title is too short
    await dpytest.message('$quizpoll "a" [a] [b] [c] [d] [e] [f]')
    assert dpytest.verify().message().contains().content("Title too short.")

    # Test quizpoll: too few options
    await dpytest.message('$quizpoll "TITLE" [a]')
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("Polls need at least two options.")
    )

    # Test quizpoll: too many options
    await dpytest.message('$quizpoll "TITLE" [a] [b] [c] [d] [e] [f] [g]')
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("Polls cannot have more than six options.")
    )

    # Test quizpoll: option is empty
    await dpytest.message('$quizpoll "TITLE" [] [b] [c]')
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("Options cannot be blank or whitespace only.")
    )

    e = discord.Embed(
        title="**TITLE**",
        description="\n\n🇦     a\n\n🇧     b\n\n🇨     c",
        colour=0x83BAE3,
    )

    # Test quizpoll embed
    await dpytest.message('$quizpoll "TITLE" [a] [b] [c]')
    assert dpytest.verify().message().embed(e)


# --------------------------------
# Test calendar: subscribe and remove
# --------------------------------
@pytest.mark.asyncio
async def test_calendar(bot):
    user = dpytest.get_config().members[0]
    guild = dpytest.get_config().guilds[0]
    irole = await guild.create_role(name="Instructor")
    await irole.edit(permissions=discord.Permissions(8))
    role = discord.utils.get(guild.roles, name="Instructor")
    await dpytest.add_role(user, role)

    # Test subscribeCalendar success
    await dpytest.message("$subscribeCalendar johndoe@gmail.com")
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("Added johndoe@gmail.com to the calendar.")
    )

    # Test subscribeCalendar failure
    await dpytest.message("$subscribeCalendar johndoe")
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("Error adding user: johndoe is not a valid email.")
    )

    # Test removeCalendar failure
    await dpytest.message("$removeCalendar johndoe")
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("User johndoe was not found in the calendar's permissions.")
    )

    # Test removeCalendar failure
    await dpytest.message("$removeCalendar johndoe@gmail.com")
    assert (
        dpytest.verify()
        .message()
        .contains()
        .content("User johndoe@gmail.com has been removed from the calendar.")
    )


@pytest.mark.asyncio
async def test_get_calendar_downloads(bot):
    await dpytest.message("$clearCalendar")
    assert dpytest.verify().message().contains().content("Calendar has been cleared")
    await dpytest.message("$getPdfDownload")
    assert dpytest.verify().message().contains().content("No upcoming events found.")
    date = datetime.now(ZoneInfo("America/New_York")) + timedelta(days=1)
    caldate = date.astimezone(ZoneInfo("UTC"))
    dateiso = date.isoformat(timespec="seconds")
    caldateiso = caldate.isoformat(timespec="seconds")[:-6]
    await dpytest.message(f"$addCalendarEvent HW3 CSC510 {caldateiso}Z")
    assert dpytest.verify().message().contains().content("Event HW3 added to calendar!")

    await dpytest.message("$getPdfDownload")
    calendar_path = os.getenv("CALENDAR_PATH")

    reader = PdfReader(f"{calendar_path}calendar.pdf")

    page = reader.pages[0]

    text = page.extract_text()
    text = text.split("\n")

    assert len(text) == 7
    assert text[0] == "Summary"
    assert text[1] == "Start"
    assert text[2] == "End"
    assert text[3] == "0"
    assert text[4] == "HW3"
    assert text[5][:10] == dateiso[:10]
    assert text[5][10:16] == dateiso[10:16]

    await dpytest.message("$getiCalDownload")

    # referenced https://stackoverflow.com/questions/3408097/parsing-files-ics-icalendar-using-python

    caldata = open(f"{calendar_path}ical.ics").read()

    for cal in vobject.readComponents(caldata):
        for component in cal.components():
            if component.name == "VEVENT":
                assert component.description.valueRepr() == "CSC510"
                assert component.summary.valueRepr() == "HW3"
                assert component.dtstart.valueRepr().month == caldate.month
                assert component.dtstart.valueRepr().year == caldate.year
                assert component.dtstart.valueRepr().day == caldate.day
                assert component.dtstart.valueRepr().hour == caldate.hour


# @pytest.mark.asyncio
# async def test_get_resource_by_topic(bot):
#     # create instuctor user
#     user = dpytest.get_config().members[0]
#     guild = dpytest.get_config().guilds[0]
#     irole = await guild.create_role(name="Instructor")
#     await irole.edit(permissions=discord.Permissions(8))
#     role = discord.utils.get(guild.roles, name="Instructor")
#     await dpytest.add_role(user, role)

#      ##Testing add resource

# +   await dpytest.message(
# +       "$addResource Testing https://github.com/txt/se23/blob/main/docs/testing1.md"
# +   )
# +   assert (
# +       dpytest.verify()
#         .message()
# +       .contains()
# +       .content("Resource successfully added to the Testing")
# +   )
 
#      ##Testing delete Resource

# -   await dpytest.message("$deleteResource Testing https://github.com/txt/se23/blob/main/docs/testing1.md")
# -   assert dpytest.verify().message().contains().content("The Resource has been deleted successfully.")
# +   await dpytest.message(
# +       "$deleteResource  Testing https://github.com/txt/se23/blob/main/docs/testing1.md"
# +   )
# +   assert (
# +       dpytest.verify()
# +       .message()
#         .contains()
# +       .content("The Resource has been deleted successfully.")
# +   )
 
#      ##Test missing argument topic
#     await dpytest.message("$showResourceByTopic")
# -   assert dpytest.verify().message().contains().content("To use the showResourceByTopic command, do: $showResourceByTopic <Topic Name>")
# +   assert (
# +        dpytest.verify()
# +        .message()
# +        .contains()
# +        .content(
# +            "To use the showResourceByTopic command, do: $showResourceByTopic <Topic Name>"
# +        )
# +    )