#Discord Imports
import discord
from discord.ext import commands
from discord.utils import get

#MISC Imports
import asyncio
import sys


def setup( client ):
    client.add_cog( initial(client) )


class initial( commands.Cog ):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('BOT is running.')

    #Cog Commands
    @commands.command()
    async def load(self, ctx, extension):
        self.client.load_extension( f'cogs.{extension}')
        print(f'Loading {extension}')

    @commands.command()
    async def unload(self, ctx, extension):
        self.client.unload_extension( f'cogs.{extension}')
        print(f'Unloading {extension}')

    #Close Script 
    @commands.command()
    async def quit(self, ctx):
        voice = get( self.client.voice_clients, guild=ctx.guild )
        if voice and voice.is_connected():
            await voice.disconnect()
        sys.exit()