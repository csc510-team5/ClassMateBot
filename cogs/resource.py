import os
import sys

import discord
from discord.ext import commands
from discord.utils import get

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import db


# -----------------------------------------------------------
# This File contains commands for Managing Resources, Adding Deleting and Retriving Resource,
# -----------------------------------------------------------
class Resource(commands.Cog):
    # -----------------------------------------------------------
    # initialize
    # -----------------------------------------------------------
    def __init__(self, bot):
        self.bot = bot

    # -------------------------------------------------------------------------------------------------------
    #    Function: addResource(self, ctx, topic, resource_link):
    #    Description: This function is used to add the topic and the link the of resource of this topic
    #    Inputs:
    #    - self: used to access parameters passed to the class through the constructor
    #    - ctx: used to access the values passed through the current context
    #    - topic : used to provide the name of a topic
    #    - resource_link : used to provide the topic's resource link
    #    Outputs: It will add a new rosource in the list of course material resource
    # -------------------------------------------------------------------------------------------------------
    @commands.has_role("Instructor")
    @commands.command(
        name="addResource",
        help="To use the addResource command, do: $addResource <topic_name> <resource_link>  \n \
        ( For example: $addResource Ethical_Software_Engineering, https://github.com/txt/se23/blob/main/docs/ethics.md  )"
    )
    async def addResource(self, ctx, topic, resource_link):
        db.query(
            "INSERT INTO resources (guild_id, topic_name, resource_link) VALUES (%s, %s, %s)",
            (ctx.guild.id,  topic, resource_link),
        )
        await ctx.send(f"Resource successfully added to the topic {topic}")
        return
    @addResource.error
    async def addResource_error(self, ctx, error):
        """Error handling for resource add"""
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("To use the addResource command, do: $addResource <topic_name> <resource_link>  \n \
            ( For example: $addResource Ethical_Software_Engineering, https://github.com/txt/se23/blob/main/docs/ethics.md  )"
            )


    # -------------------------------------------------------------------------------------------------------
    #    Function: showAllResource(self, ctx):
    #    Description: This function is used to get the resources
    #    Inputs:
    #    - self: used to access parameters passed to the class through the constructor
    #    - ctx: used to access the values passed through the current context
    #    Outputs: Return the list of resources
    # -------------------------------------------------------------------------------------------------------
    @commands.command(
        name="showAllResource",
        help="To use the showAllResource command, do: $showAllResource"
    )
    async def showAllResource(self, ctx):
        result = db.query("SELECT * FROM resources")

        if not result:
            await ctx.send("No resources found.")
            return
        embed = discord.Embed(title="List of Resources", color=0x00ff00)

        for row in result:
            topic = row[1]
            resource_link = row[2]
            embed.add_field(name=f"Topic: {topic}", value=f"Resource Link: {resource_link}", inline=False)
        await ctx.send(embed=embed)
        return

    @showAllResource.error
    async def showAllResource_error(self, ctx, error):
        """Error handling for getting resource"""
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send0("To use the showAllResource command, do: $showAllResource")

    # -------------------------------------------------------------------------------------------------------
    #    Function: showResourceByTopic(self, ctx, topic_name):
    #    Description: This function is used to get the resources of a sprcific topic
    #    Inputs:
    #    - self: used to access parameters passed to the class through the constructor
    #    - ctx: used to access the values passed through the current context
    #    Outputs: Return the list of resources of a specific Topic
    # -------------------------------------------------------------------------------------------------------
    @commands.command(
        name="showResourceByTopic",
        help="To use the showResourceByTopic command, do: $showResourceByTopic <Topic Name> \n \
        To see the Topic List, use $showTopicList"
    )
    async def showResourceByTopic(self, ctx, topic_name):
        result = db.query("SELECT * FROM resources WHERE topic_name = %s", (topic_name,))

        if not result:
            await ctx.send("No resources found.")
            return

        embed = discord.Embed(title=f"List of Resources for topic {topic_name}", color=0x00ff00)

        for row in result:
            topic = row[1]
            resource_link = row[2]
            embed.add_field(name="", value=f"Resource: {resource_link}", inline=False)

        await ctx.send(embed=embed)
        return

    @showResourceByTopic.error
    async def showResourceByTopic_error(self, ctx, error):
        """Error handling for getting resource"""
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("To use the showResourceByTopic command, do: $showResourceByTopic <Topic Name> \n \
            To see the Topic List, use $showTopicList")
        else:
            print(error)
    # -------------------------------------------------------------------------------------------------------
    #    Function: deleteResource(self, ctx, topic, resource_link):
    #    Description: This function will delete a resource from the resource list
    #    Inputs:
    #    - self: used to access parameters passed to the class through the constructor
    #    - ctx: used to access the values passed through the current context
    #    - topic : used to provide the name of a topic
    #    - resource_link : used to provide the resource topic's link
    #    Outputs: It will add a new rosource under a topic
    # -------------------------------------------------------------------------------------------------------
    @commands.has_role("Instructor")
    @commands.command(
        name="deleteResource",
        help="To use the deleteResource command, do: $deleteResource <topic_name> <resource_link>  \n \
        ( For example: $deleteResource Ethical_Software_Engineering, https://github.com/txt/se23/blob/main/docs/ethics.md  ) \n \
        To see all the resource use $showAllResource"
        )
    async def deleteResource(self, ctx, topic, resource_link):
        result = db.query("SELECT * FROM resources WHERE guild_id = %s AND topic_name = %s AND resource_link = %s",
                    (ctx.guild.id, topic, resource_link))

        if not result:
            await ctx.send("No matching element found.To see all the resouce use $showAllResource")
            return
        db.query("DELETE FROM resources WHERE topic_name = %s AND resource_link = %s",
        (topic, resource_link))
        await ctx.send("The Resource has been deleted successfully.")
        return
    @deleteResource.error
    async def deleteResource_error(self, ctx, error):
        """Error handling for resource add"""
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("To use the deleteResource command, do: $deleteResource <topic_name> <resource_link>  \n \
            ( For example: $DeleteResource Ethical_Software_Engineering, https://github.com/txt/se23/blob/main/docs/ethics.md  ) \n \
            To see all the resource use $showAllResource"
            )


    # -------------------------------------------------------------------------------------------------------
    #    Function: showTopicList(self, ctx):
    #    Description: This function is used to get the resources
    #    Inputs:
    #    - self: used to access parameters passed to the class through the constructor
    #    - ctx: used to access the values passed through the current context
    #    Outputs: Return the list of topics
    # -------------------------------------------------------------------------------------------------------
    @commands.command(
        name="showTopicList",
        help="To use the showTopicList command, do: $showTopicList"
    )
    async def showTopicList(self, ctx):
        result = db.query("SELECT DISTINCT topic_name FROM resources")

        if not result:
            await ctx.send("No topic has been created yet.")
            return

        topic_list = [row[0] for row in result]

        formatted_topic_list = "\n".join(topic_list)

        await ctx.send(f"List of Topics:\n{formatted_topic_list}")
        return

    @showTopicList.error
    async def showTopicList_error(self, ctx, error):
        """Error handling for getting resource"""
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("To use the showTopicList command, do: $showTopicList")


async def setup(bot):
    """Adds the file to the bot's cog system"""
    await bot.add_cog(Resource(bot))