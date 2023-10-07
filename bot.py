# docker commands to stop and start the container again without create duplicates 
# docker stop discord-reminder-bot
# docker rm discord-reminder-bot
# docker build -t discord-reminder-bot-image .
# docker run --name discord-reminder-bot -p 8000:8000 -e "DISCORD_BOT_TOKEN=discord_token" discord-reminder-bot-image python -u bot.py

import os
import discord
from discord.ext import commands
from utils.reminder_manager import ReminderManager

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)


# Initialize ReminderManager 
reminder_manager = ReminderManager(bot)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    reminder_manager.start_loop()

@bot.command()
async def set(ctx, date, time):
    await reminder_manager.create_reminder(ctx, date, time)


@bot.command() 
async def list(ctx):
    await reminder_manager.list_reminders(ctx)
    
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing required argument.")
    else:
        print(f"Error: {error}")
        await ctx.send(f"An error occurred: {error}")



# Keep environment variable     
TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
if not TOKEN:
    raise ValueError("No token found!")   

bot.run(TOKEN)
