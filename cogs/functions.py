#Discord Imports
import discord
from discord.ext import commands
from discord.utils import get

#MISC Imports
import asyncio
import sys


def setup( client ):
    client.add_cog( functions(client) )


class functions( commands.Cog ):

    def __init__(self, client):
        self.client = client
    