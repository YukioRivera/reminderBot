from datetime import datetime, timedelta
from discord.ext import tasks
import discord
import pytz  # Import the pytz library

class ReminderManager:

    def __init__(self, bot):
        self.reminders = []
        self.bot = bot
        self.timezone = pytz.timezone('US/Pacific')  # Set the timezone to PST

    async def create_reminder(self, ctx, date, time, name):
        try:
            # Convert the date and time strings to a datetime object in PST
            reminder_datetime = self.timezone.localize(datetime.strptime(f"{date} {time}", '%Y-%m-%d %H:%M'))
            self.reminders.append({'ctx': ctx, 'datetime': reminder_datetime, 'name': name, 'guild_id': ctx.guild.id})
            await ctx.send(f"Reminder '{name}' set for {reminder_datetime.strftime('%Y-%m-%d %H:%M')} PST!")
        except ValueError:
            await ctx.send("Invalid date or time format. Please use YYYY-MM-DD HH:MM format.")

    async def list_reminders(self, ctx):
        if not self.reminders:
            await ctx.send("No reminders set.")
            return
            
        reminder_list = "\n".join([f"'{r['name']}' on {r['datetime'].strftime('%B %d, %Y at %H:%M')} PST" for r in self.reminders])
        await ctx.send(f"Reminders:\n{reminder_list}")

    @tasks.loop(minutes=1)
    async def check_reminders(self):
        print("Checking reminders...")  # Debug print

        now = datetime.now(self.timezone).replace(second=0, microsecond=0)  # Get the current time in PST and set seconds and microseconds to 0
        print(f"Current time: {now.strftime('%H:%M')}")  # Debug print

        reminders_to_remove = []

        for r in self.reminders[:]:  # Iterate over a copy of the list
            reminder_datetime_minus_2_hours = r['datetime'] - timedelta(hours=2)
            reminder_time_minus_2_hours = reminder_datetime_minus_2_hours.time()
            reminder_time_exact = r['datetime'].time()
            
            print(f"Reminder time minus 2 hours: {reminder_time_minus_2_hours.strftime('%H:%M')}")  # Debug print
            print(f"Exact Reminder time: {reminder_time_exact.strftime('%H:%M')}")  # Debug print
            
            guild = self.bot.get_guild(r['guild_id'])
            print("guild: ", guild)
            if guild:
                channel = discord.utils.get(guild.channels, name='general')
                print("channel: ", channel)
                if channel:
                    try:
                        if reminder_time_minus_2_hours == now.time():
                            await channel.send(f"@everyone Reminder about '{r['name']}' in 2 hours!")
                        elif reminder_time_exact == now.time():
                            await channel.send(f"@everyone It's time for '{r['name']}'!")
                            reminders_to_remove.append(r)
                    except Exception as e:
                        print(f"Error sending reminder: {e}")
                else:
                    print("General channel not found!")
            else:
                print(f"Guild with ID {r['guild_id']} not found!")

        # Remove the reminders that have been triggered
        for r in reminders_to_remove:
            self.reminders.remove(r)

    def start_loop(self):
        self.check_reminders.start()

