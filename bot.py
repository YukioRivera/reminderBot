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

class CustomHelpCommand(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        channel = self.get_destination()
        help_embed = discord.Embed(title="ReminderBot Help", color=discord.Color.blue())
        
        for command in self.context.bot.commands:
            if command.name == "set":
                help_embed.add_field(name=f"!{command.name}", value=f"{command.brief}\nUsage: !set YYYY-MM-DD HH:MM 'Name of the reminder'", inline=False)
            elif command.name == "list":
                help_embed.add_field(name=f"!{command.name}", value=f"{command.brief}\nUsage: !list", inline=False)
            elif command.name == "set_timezone":
                help_embed.add_field(name=f"!{command.name}", value=f"{command.brief}\nUsage: !set_timezone City, State, Country(optional)", inline=False)
            else:
                help_embed.add_field(name=f"!{command.name}", value=command.brief, inline=False)
        
        await channel.send(embed=help_embed)


bot.help_command = CustomHelpCommand()

# Initialize ReminderManager 
reminder_manager = ReminderManager(bot)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    reminder_manager.start_loop()

@bot.command(brief="Set a new reminder.")
async def set(ctx, date, time, name):
    await reminder_manager.create_reminder(ctx, date, time, name)

@bot.command(brief="List all reminders.")
async def list(ctx):
    await reminder_manager.list_reminders(ctx)

@bot.command(brief="Updates timezone")
async def set_timezone(ctx, location_name):
    await reminder_manager.set_timezone(ctx, location_name)

@bot.command(brief="Removes reminder from the list")
async def remove(ctx, name):
    await reminder_manager.remove(ctx, name)
    
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
