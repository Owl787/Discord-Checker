import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.reactions = True
intents.message_content = True

bot = commands.Bot(command_prefix='P ', intents=intents)

# ✏️ Replace these with your actual IDs
CONTROL_CHANNEL_ID = 1388939559420559546  # Channel where you'll use the command
TARGET_MESSAGE_ID = 1389276304544764054   # The message you want to check

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command(name='', help="Usage: P <user_id> — checks the target message for reactions from that user.")
async def check_react(ctx, user_id: int):
    if ctx.channel.id != CONTROL_CHANNEL_ID:
        return  # Only respond in the control channel

    try:
        # Fetch the message from any text channel in the guild
        target_msg = None
        for channel in ctx.guild.text_channels:
            try:
                msg = await channel.fetch_message(TARGET_MESSAGE_ID)
                if msg:
                    target_msg = msg
                    break
            except discord.NotFound:
                continue

        if not target_msg:
            await ctx.send("❌ Couldn't find the target message.")
            return

        matches = []
        for reaction in target_msg.reactions:
            users = await reaction.users().flatten()
            if any(u.id == user_id for u in users):
                matches.append(str(reaction.emoji))

        if matches:
            emojis = ", ".join(matches)
            await ctx.send(f"✅ User <@{user_id}> reacted with: {emojis}")
        else:
            await ctx.send(f"❌ No reactions found from <@{user_id}> on that message.")

    except Exception as e:
        await ctx.send(f"⚠️ Error occurred: `{e}`")

# Startup
token = os.getenv("DISCORD_TOKEN")
if not token:
    raise RuntimeError("❗ DISCORD_TOKEN is not set in env variables.")
bot.run(token)
