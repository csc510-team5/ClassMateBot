# About $add_grade_category _(New Project 2 Command)_
This command allows the instructor to add a new grade category with a designated weight
## Changes

This command was introduced by [CSC510-Group-1](https://github.com/nfoster1492/ClassMateBot-1/).

# Location of Code
The code that implements the above mentioned functionality is located in [cogs/grades.py](../../cogs/grades.py).

# Code Description
## Functions
add_grade_category(self, ctx, categoryname: str, weight: str): <br>
This function takes as arguments the values provided by the constructor through self, context in which the command was called, the name of the category being added, and the weight of the category being added.

# How to run it? (Small Example)
You are in the server that has the Classmate Bot active and online. You are an Instructor. From the instructor commands channel, enter the command `$add_grade_category <category_name> <weight>` with the desired category name and weight.

```
$add_grade_category CATEGORY_NAME, WEIGHT
$add_grade_category Tests .5
```
Successful execution of this command will add a grade category into the database with the desired weight. The bot will report on the success or failure of the command.

<img src="../../data/proj2media/addGradeCategoryHelp.PNG" width="500">

<img src="../../data/proj2media/addGradeCategory.PNG" width="500">