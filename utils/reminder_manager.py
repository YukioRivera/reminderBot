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

        now = datetime.now().time()
        now_plus_30_seconds = (datetime.combine(datetime.today(), now) + timedelta(seconds=30)).time()
        now_minus_30_seconds = (datetime.combine(datetime.today(), now) - timedelta(seconds=30)).time()

        for r in self.reminders:
            reminder_datetime_minus_2_hours = r['datetime'] - timedelta(hours=2)
            reminder_time_minus_2_hours = reminder_datetime_minus_2_hours.time()
            reminder_time_exact = r['datetime'].time()
                
            print(f"Reminder time minus 2 hours: {reminder_time_minus_2_hours}")  # Print the time object
            print(f"Current time: {now}")  # Print the time object

            if reminder_time_minus_2_hours == now:
                channel = discord.utils.find(lambda c: c.name=='general', self.bot.get_all_channels())
                if channel:
                    await channel.send(f"@everyone Reminder about '{r['name']}' in 2 hours!")
                else:
                    print("General channel not found!")
            elif now_minus_30_seconds <= reminder_time_exact <= now_plus_30_seconds:
                channel = discord.utils.find(lambda c: c.name=='general', self.bot.get_all_channels())
                if channel:
                    await channel.send(f"@everyone It's time for '{r['name']}'!")
                else:
                    print("General channel not found!")



    def start_loop(self):
        self.check_reminders.start()
