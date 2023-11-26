# About $grade_report_assignment _(New Project 2 Command)_
 This command lets the instructor generate a report on the average, low, and high score on each assignment

## Changes

This command was introduced by [CSC510-Group-1](https://github.com/nfoster1492/ClassMateBot-1/).

# Location of Code
The code that implements the above mentioned functionality is located in `[cogs/grades.py](https://github.com/nfoster1492/ClassMateBot-1/tree/main/cogs/grades.py)`.

# Code Description
## Functions
grade_report_assignment(self, ctx): <br>
This function takes as arguments the values provided by the constructor through self and context in which the command was called

# How to run it? (Small Example)
You are in the server that has the Classmate Bot active and online. From the instructor commands channel, enter the command `$grade_report_assignment`

```
$grade_report_assignment
```
Successful execution of this command will send a DM to the instructor with the grading breakdown.

<img src="../../data/proj2media/gradeReportAssignmentHelp.PNG" width="500">

<img src="../../data/proj2media/gradeReportAssignment.PNG" width="500">

<img src="../../data/proj2media/gradeReportAssignmentDM.PNG" width="500">
