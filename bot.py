#Importing Discord 
import discord
from discord.ext import commands

#Misc Imports
import json
import os

#Config File
with open('config.json') as config_file:
    config = json.load( config_file )

#MYSQL
import mysql.connector
db = mysql.connector.connect(
    host=config['mysqlip'],
    user=config['mysqluser'],
    passwd=config['mysqlpasswd'],
    database="careerbot",
    auth_plugin='mysql_native_password'
)

#Configure Bot
client = commands.Bot( command_prefix = '.')
serverid = config['serverid']

#Loading All Cogs
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

#Run Bot
token = config['token']
client.run(token)