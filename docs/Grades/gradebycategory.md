# About $gradebycategory _(New Project 2 Command)_
 This command lets a student get their average grade for a certain category.

## Changes

This command was introduced by [CSC510-Group-1](https://github.com/nfoster1492/ClassMateBot-1/).

# Location of Code
The code that implements the above mentioned functionality is located in [cogs/grades.py](../../cogs/grades.py).

# Code Description
## Functions
gradebycateogory(self, ctx, categoryName: str): <br>
This function takes as arguments the values provided by the constructor through self, context in which the command was called, and the name of the category whose average grade is desired.

# How to run it? (Small Example)
You are in the server that has the Classmate Bot active and online. From the general channel, enter the command `$gradebycategory categoryName`

```
$gradebycategory CATEGORY_NAME
$gradebycategory projects
```
Successful execution of this command will send a DM to the student with their average grade for the given category.

<img src="https://github.com/nfoster1492/ClassMateBot-1/blob/1453b81e4ad9fdc99b744fb35c859f2b0829e8b9/data/proj2media/gradebycategoryHelp.png" width="500">
