
# About $addResource

Command that lets the instructor add the resource link of course materials. Instructor only.

## Changes

This command was introduced by [CSC510-Group-5](https://github.com/csc510-team5/ClassMateBot).

# Location of Code
The code that implements the above mentioned functionality is located in [resource.py](https://github.com/csc510-team5/ClassMateBot/blob/main/cogs/resource.py).

# Code Description
## Functions
addResource(ctx, topic, resource_link):: <br>
This function takes as arguments the context in which the command was called, the name of the topic for which a resource link will be added, and the resource_link itself.

# How to run it? (Small Example)
You are in the server that has the Classmate Bot active and online. You go to
 the #instructor-commands channel and enter the command
  $addResource topic_name resource_link.
```
$addResource Testing "https://github.com/txt/se23/blob/main/docs/testing1.md"
$addResource "License in SE" "https://github.com/txt/se23/blob/main/docs/licenses.md"
```
Successful execution of this command will add two resource in the resource list.

<img src="https://github.com/csc510-team5/ClassMateBot/blob/main/data/media/add-resource.png?raw=true" width="500">

This can be verified by the command $showAllResource to check if the resources have been added. 

<img src="https://github.com/csc510-team5/ClassMateBot/blob/main/data/media/show-resource.png?raw=true" width="500">
