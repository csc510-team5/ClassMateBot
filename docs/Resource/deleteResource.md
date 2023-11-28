
  
# About $deleteResource

Command that lets the instructor delete a resource link of course materials. Instructor only.

## Changes

This command was introduced by [CSC510-Group-5](https://github.com/csc510-team5/ClassMateBot).

# Location of Code
The code that implements the above mentioned functionality is located in [resource.py](https://github.com/csc510-team5/ClassMateBot/blob/main/cogs/resource.py).

# Code Description
## Functions
deleteResource(ctx, topic, resource_link):: <br>
This function takes as arguments the context in which the command was called, the name of the topic and the resource_link that needs to be discarded.

# How to run it? (Small Example)
You are in the server that has the Classmate Bot active and online. You go to
 the #instructor-commands channel and enter the command
  $deleteResource topic_name resource_link.
```
$deleteResource "Testing" "https://github.com/txt/se23/blob/main/docs/testing1.md"
```
Successful execution of this command will delete the resource in the resource list.

<img src="https://github.com/csc510-team5/ClassMateBot/blob/main/data/media/delete-resource.png?raw=true" width="500">

This can be verified by the command $showAllResource to check if the resource have been deleted. 

