import os
import discord
import asyncpraw

from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

# REDDIT
reddit = asyncpraw.Reddit(
    client_id=os.getenv('ID'),
    client_secret=os.getenv('SECRET'),
    user_agent=f'Hello',
    username=os.getenv('ACCOUNT_USERNAME'),
    password=os.getenv('ACCOUNT_PASSWORD'),
    redirect_uri='http://localhost:8080',
)
reddit.validate_on_submit = True

# DISCORD
discord_client = commands.Bot(command_prefix=commands.when_mentioned, help_command=None)

@discord_client.event
async def on_ready():
    print('Connected with Discord as', discord_client.user)

@discord_client.event
async def on_message(message):
    if 'reddix:' in message.channel.topic:
        await message.add_reaction('✅')
        sub = await reddit.subreddit(message.channel.topic.split('reddix:"')[1].split('"')[0]) # get subreddit
        post = await sub.submit(title='Discord Auto-News', selftext=message.clean_content) # post
        await post.reply(f'Hey, Ich bin der **Reddix Bot** und dieser Post wurde automatisiert erstellt.\n\n\nServer: **{message.guild.name}**\n\nKanal: **#{message.channel.name}**\n\nAutor: **@{message.author}** ') # reply with info

discord_client.run(os.getenv('DISCORD'))