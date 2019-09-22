#Discord Imports
import discord
from discord.ext import commands
from discord.utils import get

#MISC Imports
import asyncio
import sys
from datetime import date
from datetime import datetime

#Global Variables
database = None
cursor = None

def setup( client ):
    client.add_cog( functions(client) )
            
class functions( commands.Cog ):

    def __init__(self, client):
        self.client = client
        from bot import db
        global cursor
        global database
        database = db
        cursor = database.cursor(buffered=True)

    @commands.command( pass_context = True )
    async def init(self, ctx):
        tablename = str(ctx.message.author).replace('#','')
        embed=discord.Embed(color=0xabd8fc)
        try: #Create table if one doesnt exist for user
            cursor.execute(f'CREATE TABLE {tablename} (ID int NOT NULL AUTO_INCREMENT, Company varchar(255), Position varchar(255), Date varchar(255), URL varchar(255), PRIMARY KEY (ID) )')
            embed.add_field(name="THE SPEEDWAGON FOUNDATION", value=f'Table initialized for {ctx.message.author.mention}', inline=False)
        except:
            embed.add_field(name="THE SPEEDWAGON FOUNDATION", value=f'You have already initialized a table for {ctx.message.author.mention}.', inline=False)
        
        await ctx.send(embed=embed)
        
        database.commit()

    @commands.command( pass_context = True )
    async def apply(self, ctx):
        tablename = str(ctx.message.author).replace('#','')

        #Check if Table for User Exists
        try:
            cursor.execute(f'SELECT * FROM {tablename}')
        except:
            embed=discord.Embed(color=0xabd8fc)
            embed.add_field(name="TABLE NOT FOUND", value=f'**Please use \'.init\'**', inline=False)
            await ctx.send(embed=embed)
            return
        
        done = False
        while done is False:
            company = position = url = ""
            embed=discord.Embed(color=0xabd8fc)
            embed.add_field(name="NEW APPLICATION", value=f'**1) Company:** {company}\n**2) Position:** {position}\n**3) URL:** {url}\n\n *Please enter the name of the company:*', inline=False)
            await ctx.send(embed=embed)
            
            temp = await self.client.wait_for('message', check=lambda message: message.author == ctx.author)
            if temp.content.lower() == "quit" or temp.content.lower() == "q":
                embed=discord.Embed(color=0xabd8fc)
                embed.add_field(name="THE SPEEDWAGON FOUNDATION", value=f'**The Application has been aborted.**', inline=False)
                await ctx.send(embed=embed)
                return
            else:
                company = temp.content
                embed=discord.Embed(color=0xabd8fc)
                embed.add_field(name="NEW APPLICATION", value=f'**1) Company:** {company}\n**2) Position:** {position}\n**3) URL:** {url}\n\n *Please enter the name of the position:*', inline=False)
                await ctx.send(embed=embed)

                temp = await self.client.wait_for('message', check=lambda message: message.author == ctx.author)
                if temp.content.lower() == "quit" or temp.content.lower() == "q":
                    embed=discord.Embed(color=0xabd8fc)
                    embed.add_field(name="THE SPEEDWAGON FOUNDATION", value=f'**The Application has been aborted.**', inline=False)
                    await ctx.send(embed=embed)
                    return
                else:
                    position = temp.content
                    embed=discord.Embed(color=0xabd8fc)
                    embed.add_field(name="NEW APPLICATION", value=f'**1) Company:** {company}\n**2) Position:** {position}\n**3) URL:** {url}\n\n *Please enter the URL:*', inline=False)
                    await ctx.send(embed=embed)

                    temp = await self.client.wait_for('message', check=lambda message: message.author == ctx.author)
                    if temp.content.lower() == "quit" or temp.content.lower() == "q":
                        embed=discord.Embed(color=0xabd8fc)
                        embed.add_field(name="THE SPEEDWAGON FOUNDATION", value=f'**The Application has been aborted.**', inline=False)
                        await ctx.send(embed=embed)
                        return
                    else:
                        url = temp.content

                        response = False
                        while response is False:
                            embed=discord.Embed(color=0xabd8fc)
                            embed.add_field(name="NEW APPLICATION", value=f'**1) Company:** {company}\n**2) Position:** {position}\n**3) URL:** {url}\n\n *Is this Correct? (Y/N):*', inline=False)
                            await ctx.send(embed=embed)

                            temp = await self.client.wait_for('message', check=lambda message: message.author == ctx.author)
                            if temp.content.lower() == "quit" or temp.content.lower() == "q":
                                embed=discord.Embed(color=0xabd8fc)
                                embed.add_field(name="THE SPEEDWAGON FOUNDATION", value=f'**The Application has been aborted.**', inline=False)
                                await ctx.send(embed=embed)
                                return
                            elif temp.content.lower() == "y" or temp.content.lower() =="yes":
                                done = response = True
                            elif temp.content.lower() == "n" or temp.content.lower() =="no":
                                response = True
            
        today = date.today()
        d = today.strftime("%m/%d/%y")

        formula = (f'INSERT INTO {tablename} (Company, Position, Date, URL) VALUES (%s, %s, %s, %s)')
        tempRow = (company, position, d, url)
        cursor.execute( formula, tempRow )
        cursor.execute(f'ALTER TABLE {tablename} ORDER BY ID DESC')
        database.commit()

        embed=discord.Embed(color=0xabd8fc)
        embed.add_field(name="THE SPEEDWAGON FOUNDATION", value=f'**Your Application has been SUBMITTED.**', inline=False)
        await ctx.send(embed=embed)

    @commands.command( pass_context = True )
    async def stats(self, ctx):
        if len(ctx.message.mentions) == 0:
            username = ctx.message.author
        else:
            username = ctx.message.mentions[0]
        
        tablename = str(username).replace('#','')
        try:
            cursor.execute(f'SELECT * FROM {tablename} WHERE ID > 0')
        except:
            embed=discord.Embed(color=0xabd8fc)
            embed.add_field(name="TABLE NOT FOUND", value=f'**Please use \'.init\'**', inline=False)
            await ctx.send(embed=embed)
            return

        joblist = cursor.fetchall()
        database.commit()

        totalnum = 0
        date = firstdate = perday = "N/A"
        for item in joblist:
            date = item[3]
            if totalnum == 0:
                firstdate = item[3]
            totalnum += 1

        d_format = "%m/%d/%y"
        if totalnum == 0:
            perday = "N/A"
        elif (datetime.strptime( date, d_format ) - datetime.strptime( firstdate, d_format )).days == 0:
            perday = totalnum
        else:
            last = datetime.strptime( date, d_format )
            first = datetime.strptime( firstdate, d_format )
            perday = str( round( totalnum/( (last - first).days +1 ), 2 ) )

        embed=discord.Embed(color=0xabd8fc)
        embed.add_field(name="THE SPEEDWAGON FOUNDATION", value=f'**\nUSERNAME: {username.mention}**\nApplications Submitted: {totalnum}\nLast Submitted: {date}\nApps per Day: {perday}', inline=True)
        await ctx.send(embed=embed)
                            