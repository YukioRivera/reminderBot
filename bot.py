# docker commands to stop and start the container again without create duplicates 
# docker stop discord-reminder-bot
# docker rm discord-reminder-bot
# docker build -t discord-reminder-bot-image .
# docker run --name discord-reminder-bot -p 8000:8000 -e "DISCORD_BOT_TOKEN=MTE0NTE5ODY5OTEzMjIzNTg0OA.GDQAim.5GI1g9jbAUVoLLieazD7ZkJV6ks_mJc6pbbpho" discord-reminder-bot-image python -u bot.py


import os
import re
import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta

# Reminder class
class Reminder:
    def __init__(self, time):
        self.time = time

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

reminders = []

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print(f"Server time: {datetime.now()}")
    if not check_reminders.is_running() and not check_reminders.is_being_cancelled():
        check_reminders.start()

@bot.command()
async def set(ctx, time):
    # Validate time format
    if not re.match(r'\d{2}:\d{2}', time):
        await ctx.send("Invalid time format! Use HH:MM")
        return
        
    reminder = Reminder(datetime.strptime(time, '%H:%M'))
    reminders.append(reminder)
    
    await ctx.send(f'Reminder set for {time}!')

@bot.command()  
async def list(ctx):
    if not reminders:
        await ctx.send("No reminders set!")
        return
    
    message = "Current reminders:\n"
    for r in reminders:
        message += f"- {r.time.strftime('%H:%M')}\n"
    
    await ctx.send(message)

@tasks.loop(minutes=1)
async def check_reminders():
    print("Checking reminders...")  # Debug print

    now = datetime.now().time()
    now_str = now.strftime('%H:%M')  # Convert current time to string format 'HH:MM'

    for r in reminders:
        reminder_time_minus_2_hours = (r.time - timedelta(hours=2)).time()
        reminder_str = reminder_time_minus_2_hours.strftime('%H:%M')  # Convert reminder time to string format 'HH:MM'
        print(type(reminder_time_minus_2_hours))
        print(type(reminder_str))
        
        print(f"Reminder time minus 2 hours: {reminder_str}")  # Print the string format
        print(f"Current time: {now_str}")  # Print the string format
        
        reminder_str = reminder_time_minus_2_hours.strftime('%H:%M')
        now_str = now.strftime('%H:%M')

        if str(reminder_str) == str(now_str):
            channel = discord.utils.find(lambda c: c.name=='general', bot.get_all_channels())
            if channel:
                await channel.send("Reminder in 2 hours!")
            else:
                print("General channel not found!")


# Keep environment variable     
TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
if not TOKEN:
    raise ValueError("No token found!")   

bot.run(TOKEN)
