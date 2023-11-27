# About $add_assignment _(New Project 2 Command)_
This command lets the instructor add a new gradeable assignment
## Changes

This command was introduced by [CSC510-Group-1](https://github.com/nfoster1492/ClassMateBot-1/).

# Location of Code
The code that implements the above mentioned functionality is located in [cogs/assignments.py](../../cogs/assignments.py).

# Code Description
## Functions
add_assignment(self, ctx, assignmentname: str, categoryname: str, points: str): <br>
This function takes as arguments the values provided by the constructor through self, context in which the command was called, the name of the assignment being added, the category it belongs to, and the maximum amount of points attainable on the assignment.

# How to run it? (Small Example)
You are in the server that has the Classmate Bot active and online. You are an Instructor. From the instructor commands channel, enter the command `$add_assignment <assignment_name> <category_name> <points>` with the desired assignment name, category, and weight.

```
$add_assignment ASSIGNMENT_NAME CATEGORY_NAME POINTS
$add_assignment test1 tests 100
```
Successful execution of this command will add an assignment into the database with the desired name, category, and points. The bot will report on the success or failure of the command.

<img src="../../data/proj2media/addAssignmentHelp.PNG" width="500">

<img src="../../data/proj2media/addAssignment.PNG" width="500">