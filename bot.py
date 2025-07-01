import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f"Bot connected as {bot.user}")

@bot.event
async def on_raw_reaction_add(payload):
    if payload.user_id == bot.user.id:
        return
    if payload.channel_id != YOUR_WATCH_CHANNEL_ID:
        return
    target = bot.get_channel(YOUR_TARGET_CHANNEL_ID)
    if target:
        await target.send(f"#p {payload.user_id}")

token = os.getenv("DISCORD_TOKEN")
if not token:
    raise ValueError("DISCORD_TOKEN is not set")
bot.run(token)
