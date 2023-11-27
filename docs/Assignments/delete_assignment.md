# About $delete_assignment _(New Project 2 Command)_
This command lets the instructor delete an existing gradeable assignment
## Changes

This command was introduced by [CSC510-Group-1](https://github.com/nfoster1492/ClassMateBot-1/).

# Location of Code
The code that implements the above mentioned functionality is located in [cogs/assignments.py](../../cogs/assignments.py).

# Code Description
## Functions
delete_assignment(self, ctx, assignmentname: str): <br>
This function takes as arguments the values provided by the constructor through self, context in which the command was called, and the name of the assignment being deleted.
# How to run it? (Small Example)
You are in the server that has the Classmate Bot active and online. You are an Instructor. From the instructor commands channel, enter the command `$delete_assignment <assignment_name>` with the desired assignment name.

```
$delete_assignment ASSIGNMENT_NAME
$delete_assignment test1
```
Successful execution of this command will delete an assignment from the database. The bot will report on the success or failure of the command.

<img src="../../data/proj2media/deleteAssignmentHelp.PNG" width="500">

<img src="../../data/proj2media/deleteAssignment.PNG" width="500">