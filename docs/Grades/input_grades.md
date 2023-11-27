# About $input_grades _(New Project 2 Command)_
This command allows the instructor to input grades into the system for a given assignment.

## Changes

This command was introduced by [CSC510-Group-1](https://github.com/nfoster1492/ClassMateBot-1/).

# Location of Code
The code that implements the above mentioned functionality is located in [cogs/grades.py](../../cogs/grades.py).

# Code Description
## Functions
input_grades(self, ctx, assignmentname: str): <br>
This function takes as arguments the values provided by the constructor through self, context in which the command was called, the assignment that the grades are being input for, and a csv file that is attached with a mappin gof the student names to the grades.

# How to run it? (Small Example)
You are in the server that has the Classmate Bot active and online. You are an Instructor. From the instructor commands channel, enter the command `$input_grades <assignment_name>` and attach a csv file with two columns, the first being student names and the second being the grades for the assignment

```
$inputgrades ASSIGNMENT_NAME
$inputgrades HW1
```
Successful execution of this command will update the grades in the database and report to the instructor the amount that were added, if any were skipped over, and the amount of grades that were edited.

<img src="../../data/proj2media/inputGradesHelp.PNG" width="500">

<img src="../../data/proj2media/inputGrades.PNG" width="500">