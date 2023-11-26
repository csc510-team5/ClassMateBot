# About $edit_assignment _(New Project 2 Command)_
This command lets the instructor edit a new gradeable assignment
## Changes

This command was introduced by [CSC510-Group-1](https://github.com/nfoster1492/ClassMateBot-1/).

# Location of Code
The code that implements the above mentioned functionality is located in `[cogs/grades.py](https://github.com/nfoster1492/ClassMateBot-1/tree/main/cogs/assignments.py)`.

# Code Description
## Functions
edit_assignment(self, ctx, assignmentname: str, categoryname: str, points: str): <br>
This function takes as arguments the values provided by the constructor through self, context in which the command was called, the name of the assignment being edited, the category it will now belong to, and the maximum amount of points now attainable on the assignment.

# How to run it? (Small Example)
You are in the server that has the Classmate Bot active and online. You are an Instructor. From the instructor commands channel, enter the command `$edit_assignment <assignment_name> <category_name> <points>` with the desired assignment name, category, and weight.

```
$edit_assignment ASSIGNMENT_NAME CATEGORY_NAME POINTS
$edit_assignment test1 tests 100
```
Successful execution of this command will edit an assignment in the database with the given name, with the desired category, and points. The bot will report on the success or failure of the command.

<img src="../../data/proj2media/editAssignmentHelp.PNG" width="500">

<img src="../../data/proj2media/editAssignment.PNG" width="500">