from datetime import datetime, timedelta
from discord.ext import tasks
import discord

class ReminderManager:

    def __init__(self, bot):
        self.reminders = []
        self.bot = bot

    async def create_reminder(self, ctx, date, time, name):
        try:
            # Convert the date and time strings to a datetime object
            reminder_datetime = datetime.strptime(f"{date} {time}", '%Y-%m-%d %H:%M')
            self.reminders.append({'ctx': ctx, 'datetime': reminder_datetime, 'name': name})
            await ctx.send(f"Reminder '{name}' set for {reminder_datetime.strftime('%Y-%m-%d %H:%M')}!")
        except ValueError:
            await ctx.send("Invalid date or time format. Please use YYYY-MM-DD HH:MM format.")

    async def list_reminders(self, ctx):
        if not self.reminders:
            await ctx.send("No reminders set.")
            return
            
        reminder_list = "\n".join([f"'{r['name']}' on {r['datetime'].strftime('%B %d, %Y at %H:%M')}" for r in self.reminders])
        await ctx.send(f"Reminders:\n{reminder_list}")


    @tasks.loop(minutes=1)
    async def check_reminders(self):
        print("Checking reminders...")  # Debug print

        now = datetime.now()
        now_str = now.strftime('%H:%M')  # Convert current time to string format 'HH:MM'

        for r in self.reminders:
            reminder_datetime_minus_2_hours = r['datetime'] - timedelta(hours=2)
            reminder_time_minus_2_hours = reminder_datetime_minus_2_hours.time()
            reminder_str = reminder_time_minus_2_hours.strftime('%H:%M')  # Convert reminder time to string format 'HH:MM'
            
            print(f"Reminder time minus 2 hours: {reminder_str}")  # Print the string format
            print(f"Current time: {now_str}")  # Print the string format
            if str(reminder_str) == str(now_str):
                channel = discord.utils.find(lambda c: c.name=='general', self.bot.get_all_channels())
                if channel:
                    await channel.send(f"@everyone Reminder about '{r['name']}' in 2 hours!")
                else:
                    print("General channel not found!")

    def start_loop(self):
        self.check_reminders.start()
