from datetime import datetime, timedelta, timezone
from discord.ext import tasks
from timezonefinder import TimezoneFinder
from geopy.geocoders import Nominatim
import discord
import pytz  # Import the pytz library
import geopy.geocoders
import certifi
import ssl

class ReminderManager:

    def __init__(self, bot):
        self.reminders = []
        self.bot = bot
        self.timezone = pytz.timezone('US/Pacific')  # Set the timezone to PST
        self.ssl_context = ssl._create_unverified_context(cafile=certifi.where())

    # Creates a reminder based on date and time
    async def create_reminder(self, ctx, date, time, name):
        try:
            # Convert the date and time strings to a datetime object
            today = datetime.today()

            # If only month and date is inputed
            if(len(date) == 5):
                date = str(today.year) + "-" + date
            
            # Converts date input to integers
            temp = date.split("-")
            input_date = [int(i) for i in temp]

            # Validates date input
            if (today.year > input_date[0]):
                await ctx.send(f"Check the year {input_date}")
            elif (today.month > input_date[1]):
                await ctx.send(f"Check the Month")
            elif(today.month == input_date[1]) and (today.day > input_date[2]):
                await ctx.send(f"Check the date")
            else:
                reminder_datetime = self.timezone.localize(datetime.strptime(f"{date} {time}", '%Y-%m-%d %H:%M'))
                self.reminders.append({'ctx': ctx, 'datetime': reminder_datetime, 'name': name, 'guild_id': ctx.guild.id})
                await ctx.send(f"Reminder '{name}' set for {reminder_datetime.strftime('%Y-%m-%d %H:%M')} PST!")

        except ValueError:
            await ctx.send(f"Invalid date or time format. Please use YYYY-MM-DD HH:MM format.")

    # Lists all reminders in order
    async def list_reminders(self, ctx):
        if not self.reminders:
            await ctx.send("No reminders set.")
            return
        
        # Sorts reminders based on date and time
        self.reminders.sort(key = lambda x: x['datetime'], reverse=False)
        
        reminder_list = "\n".join([f"'{r['name']}' on {r['datetime'].strftime('%B %d, %Y at %H:%M')} PST" for r in self.reminders])
        await ctx.send(f"Reminders:\n{reminder_list}")
    
    # Sets time zone according to user input (City, State, Country)
    async def set_timezone(self, ctx, location_name):
        # SSL certificate used in location api call
        geopy.geocoders.options.default_ssl_context = self.ssl_context
        geolocator = Nominatim(scheme="https", user_agent="reminderBot")

        # Gets Latitude and Longitude
        location = geolocator.geocode(location_name)

        if location:
            tf = TimezoneFinder()

            # Gets timezone from provided coordinates
            timezone_str = tf.timezone_at(lng= location.longitude, lat=location.latitude)

            if timezone_str:
                user_timezone = pytz.timezone(timezone_str)

                self.timezone = user_timezone

                # Sets time zone according to the utc
                local_time = datetime.now(self.timezone).strftime('%Y-%m-%d %H:%M')
                await ctx.send(f"New timezone set! Your current time is: {local_time}\nTimezone location: {timezone_str}")
            else:
                await ctx.send("Timezone information not found")
        else:
            await ctx.send("Location not found. Please check input")

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

