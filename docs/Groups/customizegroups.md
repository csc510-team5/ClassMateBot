# About $customizegroups
This command lets the user customize the total number of groups to create as well as the maximum members for each group.

# Location of Code
The code that implements the above-mentioned gits functionality is located [here](https://github.com/csc510-team5/ClassMateBot/blob/main/cogs/groups.py).

# Code Description
## Functions
def customizegroups(self, ctx, total_groups: int, max_members: int): <br>
This function takes as arguments the values provided by the constructor through self and context in which the command was called. The two remaining arguments include the total number of groups to create and the maximum members per group.

# How to run it?
In any channel of the server, you can customize group settings  by typing `customizegroups <total_groups> <maximum_members>`.
```
$customizegroups TOTAL_GROUPS MAXIMUM_MEMBERS
$customizegroups 10 6
```
Successful execution of this command will return a message indicating the group settings.
