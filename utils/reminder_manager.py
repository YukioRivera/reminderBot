from datetime import datetime, timedelta
from discord.ext import tasks
import discord


class ReminderManager:

    def __init__(self, bot):
        self.reminders = []
        self.bot = bot

    async def create_reminder(self, ctx, time):
        try:
            # Convert the time string to a datetime object
            reminder_time = datetime.strptime(time, '%H:%M').time()
            self.reminders.append({'ctx': ctx, 'time': reminder_time})
            await ctx.send(f"Reminder set for {time}!")
        except ValueError:
            await ctx.send("Invalid time format. Please use HH:MM format.")



    async def list_reminders(self, ctx):
        if not self.reminders:
            # ctx.send("No reminders set.")
            await ctx.send("No reminders set.")
            return
        
        reminder_list = "\n".join([f"{r['time'].strftime('%H:%M')} for {r['ctx'].author.name}" for r in self.reminders])
        # ctx.send(f"Reminders:\n{reminder_list}")
        await ctx.send(f"Reminders:\n{reminder_list}")


    @tasks.loop(minutes=1)
    async def check_reminders(self):
        print("Checking reminders...")  # Debug print

        now = datetime.now().time()
        now_str = now.strftime('%H:%M')  # Convert current time to string format 'HH:MM'

        for r in self.reminders:
            reminder_time_minus_2_hours = (datetime.combine(datetime.today(), r['time']) - timedelta(hours=2)).time()
            reminder_str = reminder_time_minus_2_hours.strftime('%H:%M')  # Convert reminder time to string format 'HH:MM'
            
            print(f"Reminder time minus 2 hours: {reminder_str}")  # Print the string format
            print(f"Current time: {now_str}")  # Print the string format
            
            if str(reminder_str) == str(now_str):
                channel = discord.utils.find(lambda c: c.name=='general', self.bot.get_all_channels())
                if channel:
                    await channel.send(f"Reminder for {r['ctx'].author.mention} in 2 hours!")
                else:
                    print("General channel not found!")

    def start_loop(self):
        self.check_reminders.start()
