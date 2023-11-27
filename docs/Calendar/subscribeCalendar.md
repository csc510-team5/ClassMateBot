# About $subscribeCalendar _(Modified Command in Project 2)_
This command allows a user to subscribe to the shared class Google Calendar.

# Location of Code
The code that implements the above mentioned gets functionality is located [here](../../cogs/calendar.py)

# Code Description
## Functions
subscribeCalendar(self, ctx, userEmail):: <br>
This function takes as arguments the values provided by the constructor through self, the context in which the command was called, and the user email to be added to the calendar.

# How to run it? (Small Example)
A basic application of this command would be if a student wanted to add themselves to the shared class calendar. Another possibility would be for the instructor to enroll students on their behalf. This is accomplished using
```
$subscribeCalendar *email-to-add*
```
Successful execution of this command will result in a Discord DM confirmation and the user being added the calendar.

![image](../../data/proj2media/subscribeCalendar1.png)

![image](../../data/proj2media/subscribeCalendar2.png)

