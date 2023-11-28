
  
# About $showResourceByTopic

Command that will enable everyone to get the list of resources for a specific topic. Rather than retrieving all the resources, the user can retrieve a list of resources in a particular topic.

## Changes

This command was introduced by [CSC510-Group-5](https://github.com/csc510-team5/ClassMateBot).

# Location of Code
The code that implements the above mentioned functionality is located in [resource.py](https://github.com/csc510-team5/ClassMateBot/blob/main/cogs/resource.py).

# Code Description
## Functions
showResourceByTopic(ctx, topic_name):: <br>
This function takes as arguments the context in which the command was called, the name of the topic for which  resources link will be retrieved.

# How to run it? (Small Example)
You are in the server that has the Classmate Bot active and online. You go to
 the channel and enter the command
  $showResourceByTopic topic_name
```
$showResourceByTopic Testing 
```
Successful execution of this command will add return the resources associated to the topics

<img src="https://github.com/csc510-team5/ClassMateBot/blob/main/data/media/show-resource-topic.png?raw=true" width="500">
