# About $getpdfDownload _(Modified Command in Project 2)_
This command lets students download a pdf so that they can import the class calendar into their calendar software of choice. 

# Location of Code
The code that implements the above mentioned gets functionality is located [here](../../cogs/calendar.py)

# Code Description
## Functions
getpdfDownload(self, ctx):: <br>
This function takes as arguments the values provided by the constructor through self, and the context in which the command was called.

# How to run it? (Small Example)
Let's say that you are in the server that has the Classmate Bot active and online, and the instructor has been updating the calendar with events. All you have to do is 
enter the command 'getPdfDownload': and the bot will return a file that the student can download
```
$getPdfDownload
```
Successful execution of this command will result in a pdf being sent in the same channel

![image](../../data/proj2media/getPdfDownload.JPG)
