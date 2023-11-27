# About $grade _(New Project 2 Command)_
This command lets a student get their grade for a certain assignment
## Changes

This command was introduced by [CSC510-Group-1](https://github.com/nfoster1492/ClassMateBot-1/).

# Location of Code
The code that implements the above mentioned functionality is located in [cogs/grades.py](../../cogs/grades.py).

# Code Description
## Functions
grade(self, ctx, assignmentName: str): <br>
This function takes as arguments the values provided by the constructor through self, context in which the command was called, and the name of the assignment whose grade is desired.

# How to run it? (Small Example)
You are in the server that has the Classmate Bot active and online. You are a Student. From the general channel, enter the command `$grade <assignmentName>` with the desired assignment name.

```
$grade ASSIGNMENT_NAME
$grade hw1
```
Successful execution of this command will DM the student their grade for that specific assignment.

<img src="https://github.com/nfoster1492/ClassMateBot-1/blob/c8e9fdaf0560a8c93743aaba67ceccb8b94bd845/data/proj2media/gradeHelp.png" width="500">
