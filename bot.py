import os
import discord
from discord.ext import commands
from collections import defaultdict

TOKEN = os.getenv("DISCORD_TOKEN")  # Make sure this is set in your environment

# Set your control channel ID here
CONTROL_CHANNEL_ID = 1389276304544764054  # <-- replace with your channel ID

intents = discord.Intents.default()
intents.messages = True
intents.reactions = True
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='P', intents=intents)

# message_id: set(user_ids who reacted)
tracked_reactions = defaultdict(set)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    user_id = payload.user_id

    # Don't track bot reactions
    if user_id == bot.user.id:
        return

    tracked_reactions[message_id].add(user_id)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.channel.id != CONTROL_CHANNEL_ID:
        return

    if not message.content.startswith("P "):
        return

    # Parse message like: P <message_id>
    try:
        parts = message.content.strip().split()
        if len(parts) != 2:
            return

        msg_id = int(parts[1])
        if msg_id not in tracked_reactions:
            await message.channel.send(f"Message {msg_id} not tracked.")
            return

        control_channel = bot.get_channel(CONTROL_CHANNEL_ID)

        # Write P <user_id> for each user who reacted
        for user_id in tracked_reactions[msg_id]:
            await control_channel.send(f"P {user_id}")

        # Now write P <user_id> for every user who reacted to a user who reacted
        for uid in tracked_reactions[msg_id]:
            for other_uid in tracked_reactions[msg_id]:
                if uid != other_uid:
                    await control_channel.send(f"P {other_uid}")

    except Exception as e:
        await message.channel.send(f"Error: {e}")
