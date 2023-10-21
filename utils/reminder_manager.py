from datetime import datetime, timedelta, timezone
from discord.ext import tasks
from timezonefinder import TimezoneFinder
from geopy.geocoders import Nominatim
import discord
import json
import pytz  # Import the pytz library
import geopy.geocoders
import certifi
import ssl

with open("styles.json") as file:
    styles = json.load(file)
    
class ReminderManager:

    def __init__(self, bot):
        self.reminders = []
        self.bot = bot
        self.timezone = pytz.timezone('US/Pacific')  # Set the time zone to PST
        self.ssl_context = ssl._create_unverified_context(cafile=certifi.where())

    # Creates a reminder based on date and time
    async def create_reminder(self, ctx, date, time, name):
        try:
            # Convert the date and time strings to a datetime object
            today = datetime.today()

            # If only month and date is inputted
            if(len(date) == 5):
                date = str(today.year) + "-" + date
            
            # Converts date input to integers
            temp = date.split("-")
            input_date = [int(i) for i in temp]

            # Validates date input
            if (today.year > input_date[0]):
                embed = discord.Embed(title="Reminder", description = f"Check the year", color=int(styles['error']['color'], 16))
                await ctx.send(embed = embed)

            elif (today.month > input_date[1]):
                embed = discord.Embed(title="Reminder",description = f"Check the Month", color=int(styles['error']['color'], 16))
                await ctx.send(embed = embed)

            elif(today.month == input_date[1]) and (today.day > input_date[2]):
                embed = discord.Embed(title="Reminder",description = f"Check the date", color=int(styles['error']['color'], 16))
                await ctx.send(embed = embed)

            else:
                reminder_datetime = self.timezone.localize(datetime.strptime(f"{date} {time}", '%Y-%m-%d %H:%M'))
                self.reminders.append({'ctx': ctx, 'datetime': reminder_datetime, 'name': name, 'guild_id': ctx.guild.id})
                embed = discord.Embed(title="Reminder",description = f"Your reminder has been set for '{date}' at '{time}'", color=int(styles['success']['color'], 16))
                await ctx.send(embed = embed)

        except ValueError:
            embed = discord.Embed(title="Reminder", description =f"Invalid date or time format. Please use YYYY-MM-DD HH:MM format.", color=int(styles['error']['color'], 16))
            await ctx.send(embed=embed)

    # Lists all reminders in order
    async def list_reminders(self, ctx):
        if not self.reminders:
            embed = discord.Embed(title="List of Reminders", description="No reminders set.", color=int(styles['error']['color'], 16))
            await ctx.send(embed = embed)
            return
        
        # Sorts reminders based on date and time
        self.reminders.sort(key = lambda x: x['datetime'], reverse=False)
        
        reminder_list = "\n".join([f"'{r['name']}' on {r['datetime'].strftime('%B %d, %Y at %H:%M')} PST" for r in self.reminders])
        embed = discord.Embed(title="List of Reminders", description=f"\n{reminder_list}", color=int(styles['success']['color'], 16))
        await ctx.send(embed=embed)
    
    # Sets time zone according to user input (City, State, Country)
    async def set_timezone(self, ctx, location_name):
        # SSL certificate used in location api call
        geopy.geocoders.options.default_ssl_context = self.ssl_context
        geolocator = Nominatim(scheme="https", user_agent="reminderBot")

        # Gets Latitude and Longitude
        location = geolocator.geocode(location_name)

        if location:
            tf = TimezoneFinder()

            # Gets time zone from coordinates
            timezone_str = tf.timezone_at(lng= location.longitude, lat=location.latitude)

            if timezone_str:
                user_timezone = pytz.timezone(timezone_str)

                self.timezone = user_timezone

                # Sets time zone according to the utc
                local_time = datetime.now(self.timezone).strftime('%H:%M')
                embed = discord.Embed(title="Time zone", description=f"New time zone set! Your current time is: '{local_time}' \nTime zone location: {timezone_str}", color=int(styles['success']['color'], 16))
                await ctx.send(embed=embed)

            else:
                embed = discord.Embed(title="Time zone", description="Time zone information not found", color= int(styles['error']['color'], 16))
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Time zone", description="Location not found. Please check input", color=int(styles['error']['color'], 16))
            await ctx.send(embed=embed)

    # Used to remove a reminder in list
    async def delete(self, ctx, name):
        # If list is empty
        if not self.reminders:
            embed= discord.Embed(title="Delete", description="No reminders set.", color=int(styles['error']['color'],16))
            await ctx.send(embed=embed)
            return
        
        # Checks for multiple similarly named reminders
        reminderCount = [r for r in self.reminders if r['name'] == name]

        # removes reminder
        if len(reminderCount) == 1:
            self.reminders.remove(reminderCount[0])
            embed= discord.Embed(title="Delete", description=f"Reminder '{name}' removed!", color=int(styles['success']['color'], 16))
            await ctx.send(embed=embed)
            return
        
        # Array of all similarly named reminders
        reminder_list = "\n".join([f"{i+1}. '{r['name']}' on {r['datetime'].strftime('%B %d, %Y at %H:%M')} PST" for i, r in enumerate(reminderCount)])
        embed = discord.Embed(title="Delete", description= f"Multiple reminders found with the name '{name}'. Which one would you like to remove?\n{reminder_list}\nReply with the corresponding number.", color=int(styles['user_input']['color'],16))
        message = await ctx.send(embed=embed)
        
        # Checks the user input
        def check(message):
            return message.author == ctx.author and message.content.isdigit() and 1 <= int(message.content) <= len(reminderCount)
        
        try:
            reply = await self.bot.wait_for('message', timeout = 60.0, check = check)
        except TimeoutError:
            await ctx.send("Timed-out. Please try again")
            return
        
        # Deletes reminder
        index = int(reply.content) -1
        self.reminders.remove(reminderCount[index])

        embed= discord.Embed(title="Delete", description=f"Reminder '{name}' removed!", color=int(styles['success']['color'], 16))
        await ctx.send(embed=embed)

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