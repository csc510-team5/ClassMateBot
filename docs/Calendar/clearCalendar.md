# About $getiCalDownload _(Modified Command in Project 2)_
This command lets the instructor clear all events from the google calendar. 

# Location of Code
The code that implements the above mentioned gets functionality is located [here](../../cogs/calendar.py)

# Code Description
## Functions
clearCalendar(self, ctx):: <br>
This function takes as arguments the values provided by the constructor through self, and the context in which the command was called.

# How to run it? (Small Example)
Let's say that you are in the server that has the Classmate Bot active and online, and you are the instructor. All you have to do is 
enter the command 'clearCalendar': in the instructor commands channel and the bot will let you know the success or failure of your command
```
$clearCalendar
```
Successful execution of this command will result in the google calendar being cleared

![image](../../data/proj2media/clearCalendar.PNG)
