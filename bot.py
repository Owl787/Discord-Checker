import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.messages = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Replace with your channel IDs
WATCHED_CHANNEL_ID = 1388939559420559546  # where reactions happen
TARGET_CHANNEL_ID = 1389308377909166110  # where "#p <user_id>" is sent

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} - {bot.user.id}')

@bot.event
async def on_raw_reaction_add(payload):
    if payload.channel_id != WATCHED_CHANNEL_ID:
        return

    user_id = payload.user_id
    if user_id == bot.user.id:
        return  # ignore bot reactions

    target_channel = bot.get_channel(TARGET_CHANNEL_ID)
    if target_channel:
        await target_channel.send(f"#p {user_id}")

# Run the bot
import os
bot.run(os.getenv("DISCORD_TOKEN"))
