# Discord Reminder Bot

A Discord bot designed to set reminders for users in a server.

## Features

- Set reminders with the `!set [date] [time] [reminder name]` command.
- List all reminders with the `!list` command.
- Automatic notifications 2 hours before and at the exact set time.

## Prerequisites

- Python 3.9 or higher.
- A Discord account and a registered [Discord application](https://discord.com/developers/applications).
- `pytz` library for timezone handling.

## Installation

### With Docker:

1. **Clone the Repository**:
   ```bash
   git clone [Your Repository URL]
   cd [Your Repository Directory]
   ```

2. **Build the Docker Image**:
   ```bash
   docker build -t discord-reminder-bot .
   ```

3. **Run the Bot**:
   - Replace `YourActualBotToken` with your bot's token.
   ```bash
   docker run -p 8000:8000 -e DISCORD_BOT_TOKEN=YourActualBotToken discord-reminder-bot
   ```

### Without Docker:

1. **Clone the Repository**:
   ```bash
   git clone [Your Repository URL]
   cd [Your Repository Directory]
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Bot**:
   - Run the command. Replace `YourActualBotToken` with your bot's token.
   ```bash
   $env:DISCORD_BOT_TOKEN=YourActualBotToken
   ```
   - Then simply run the Bot with Python.
   ```bash
   python bot.py
   ```

## Inviting the Bot to Your Server

1. **Generate OAuth2 URL**:
   - Go to the [Discord Developer Portal](https://discord.com/developers/applications).
   - Click on your application, then navigate to the "OAuth2" tab.
   - Under "OAuth2 URL Generator", select the "bot" scope and any necessary permissions.
   - Copy the generated URL.

2. **Invite the Bot**:
   - Open the copied OAuth2 URL in your web browser.
   - Choose the server you want to invite the bot to and click "Authorize".

3. **Verify Bot's Presence**:
   - After authorizing, check your Discord server. The bot should now be a member of the server and ready to accept commands.

4. **Give Bot Permissions**:
   - Back in the Application menu, on the left select "Bot"
   - Enable the Presence Intent, Server Members Intent, and Message Content Intent radio buttons.
   - Scrolling down to Bot Permissions and enable relevant permissions (or Administrator to keep things simple).

## Secure Your Bot Token

- **Never Commit Your Token**: Your bot token is sensitive information. Never commit it directly in your code or push it to public repositories.
  
- **Use Environment Variables**: Store your bot token as an environment variable. This way, the token is not hardcoded in your application and can be easily changed if needed.

- **Check Your Repository**: Before pushing changes, always review your commits to ensure no sensitive information is being uploaded.

- **Token Leaks**: If you suspect your token has been leaked or exposed, [regenerate it immediately](https://discord.com/developers/applications/1145198699132235848/bot) and update your application to use the new token.

## Usage

1. **Set a Reminder**:
   ```bash
   !set [date in YYYY-MM-DD format] [time in HH:MM format] [reminder name]
   Example: !set 2023-10-12 16:00 Jira Meeting
   ```

2. **List All Reminders**:
   ```bash
   !list
   ```
