import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
CONTROL_CHANNEL_ID = int(os.getenv("CONTROL_CHANNEL_ID"))  # Put your control channel ID here

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=None, self_bot=True, intents=intents)

processed_messages = set()
cooldown_seconds = 20

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")

@bot.event
async def on_message(message):
    if message.channel.id != CONTROL_CHANNEL_ID:
        return  # Ignore messages in other channels

    if message.id in processed_messages or message.author.id == bot.user.id:
        return

    await asyncio.sleep(cooldown_seconds)

    if message.reactions:
        user_ids = set()
        for reaction in message.reactions:
            users = await reaction.users().flatten()
            for user in users:
                if user != bot.user:
                    user_ids.add(user.id)

        for uid in user_ids:
            await message.channel.send(f"P {uid}")

    processed_messages.add(message.id)
