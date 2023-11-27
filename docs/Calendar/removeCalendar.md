# About $removeCalendar _(Modified Command in Project 2)_
This command allows the instructor to remove a specified user from the shared class Google Calendar.

# Location of Code
The code that implements the above mentioned gets functionality is located [here](../../cogs/calendar.py)

# Code Description
## Functions
removeCalendar(self, ctx, userEmail):: <br>
This function takes as arguments the values provided by the constructor through self, the context in which the command was called, and the user email that the instructor wishes to be removed.

# How to run it? (Small Example)
A basic application of this command would be if a student in the class decided to drop. The instructor can remove this user from the calendar using
```
$removeCalendar *email-to-remove*
```
Successful execution of this command will result in a Discord DM confirmation and the user being removed from the calendar.

