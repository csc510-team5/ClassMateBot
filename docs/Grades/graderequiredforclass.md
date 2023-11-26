# About $graderequiredforclass _(New Project 2 Command)_
This command lets a student get the grade they need on the next assignment to keep a desired grade in the class.
## Changes

This command was introduced by [CSC510-Group-1](https://github.com/nfoster1492/ClassMateBot-1/).

# Location of Code
The code that implements the above mentioned functionality is located in `[cogs/grades.py](https://github.com/nfoster1492/ClassMateBot-1/tree/main/cogs/grades.py)`.

# Code Description
## Functions
graderequiredforclass(self, ctx, categoryName: str, pointValue: str, desiredGrade: str): <br>
This function takes as arguments the values provided by the constructor through self, context in which the command was called, the name of the category the assignment will be part of, the amount of points the next assignment will be worth, and the overall grade desired for the course.

# How to run it? (Small Example)
You are in the server that has the Classmate Bot active and online. You are a Student. From the general channel, enter the command `$graderequired <categoryName> <pointValue> <desiredGrade>`.

```
$graderequired CATEGORY_NAME POINT_VALUE DESIRED_GRADE
$graderequired tests 200 90
```
Successful execution of this command will DM the student the grade required on the next hypothetical assignment to keep a desired grade in the course.

<img src="../../data/proj2media/graderequiredforclassHelp.png" width="500">
