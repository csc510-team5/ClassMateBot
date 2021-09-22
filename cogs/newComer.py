# TODO intro message from bot to new students with important messages and links

import discord
from discord.ext import commands
import os
import csv


class Helper(commands.Cog):
    GUILD = os.getenv("GUILD")
    UNVERIFIED_ROLE_NAME = os.getenv("UNVERIFIED_ROLE_NAME")
    VERIFIED_MEMBER_ROLE = os.getenv("VERIFIED_MEMBER_ROLE")

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="helpful00", help="purely a test function")
    async def helpful00(self, ctx):
        await ctx.send(f"Pong! My ping currently is {round(self.bot.latency * 1000)}ms")

    @commands.dm_only()
    @commands.command(
        name="verify",
        pass_context=True,
        help="Request the bot to verify the user to get access to channels",
    )
    async def verify(self, ctx, *, name: str = None):
        guild = None
        for g in self.bot.guilds:
            if g.name == self.GUILD:
                guild = g
        member = guild.get_member(ctx.message.author.id)
        unverified = discord.utils.get(
            guild.roles, name=self.UNVERIFIED_ROLE_NAME
        )  # finds the unverified role in the guild
        if (
            unverified in member.roles
        ):  # checks if the user running the command has the unveirifed role
            if name == None:
                await ctx.send(
                    "Please enter $verify your_full_name to get access to channels"
                )
            else:
                verified = discord.utils.get(
                    guild.roles, name=self.VERIFIED_MEMBER_ROLE
                )  # finds the verified role in the guild
                with open(
                    "data/server_data/name_mapping.csv", mode="a", newline=""
                ) as outfile:  # storing discord name and actual name in name_mapping.csv
                    writer = csv.writer(outfile)
                    writer.writerow([member.name, name])
                await member.add_roles(verified)  # adding verfied role
                await member.remove_roles(unverified)  # removed verfied role
                await ctx.send("Thank you for verifying")
        else:  # user has verified role
            await ctx.send("You are already verified!")


def setup(bot):
    bot.add_cog(Helper(bot))
