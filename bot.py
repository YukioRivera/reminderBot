import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

reminders = []

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    check_reminders.start()

@bot.command()
async def set(ctx, time: str):
    # Assuming time is in the format "HH:MM"
    reminder_time = datetime.strptime(time, '%H:%M')
    reminders.append(reminder_time)
    await ctx.send(f'Reminder set for {time}!')

@bot.command()
async def check(ctx):
    if not reminders:
        await ctx.send("No reminders set!")
        return
    message = "Current reminders:\n"
    for reminder in reminders:
        message += f"- {reminder.strftime('%H:%M')}\n"
    await ctx.send(message)

@tasks.loop(minutes=1)
async def check_reminders():
    now = datetime.now().time()
    for reminder in reminders:
        if (reminder - timedelta(hours=24)).time() == now:
            channel = bot.get_channel(YOUR_CHANNEL_ID)  # Replace with your channel ID
            await channel.send("@everyone Reminder! Event in 24 hours!")
        elif (reminder - timedelta(hours=2)).time() == now:
            channel = bot.get_channel(YOUR_CHANNEL_ID)  # Replace with your channel ID
            await channel.send("@everyone Reminder! Event in 2 hours!")

bot.run('MTE0NTE5ODY5OTEzMjIzNTg0OA.GqC7WJ.O7Rt8TKBiAMQES_lMbcaiE5CfgG4dgv3-UHUQU')  # Replace with your bot token
