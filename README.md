Of course! Here's the README with added instructions on how to invite the bot to a Discord server:

---

# Discord Reminder Bot

A Discord bot designed to set reminders for users in a server.

## Features

- Set reminders with the `set [time]` command.
- Check current reminders with the `check` command.
- Automatic notifications 24 hours and 2 hours before the set time.

## Prerequisites

- Python 3.8 or higher.
- A Discord account and a registered [Discord application](https://discord.com/developers/applications).

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
   - Replace `YourActualBotToken` with your bot's token.
   ```bash
   DISCORD_BOT_TOKEN=YourActualBotToken python bot.py
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

## Secure Your Bot Token

- **Never Commit Your Token**: Your bot token is sensitive information. Never commit it directly in your code or push it to public repositories.
  
- **Use Environment Variables**: Store your bot token as an environment variable. This way, the token is not hardcoded in your application and can be easily changed if needed.

- **Check Your Repository**: Before pushing changes, always review your commits to ensure no sensitive information is being uploaded.

- **Token Leaks**: If you suspect your token has been leaked or exposed, [regenerate it immediately](https://discord.com/developers/applications/1145198699132235848/bot) and update your application to use the new token.

## Usage

1. **Set a Reminder**:
   ```bash
   !set [time in HH:MM format]
   ```

2. **Check Current Reminders**:
   ```bash
   !check
   ```

## Contributing

If you'd like to contribute, please fork the repository and use a feature branch. Pull requests are warmly welcome.

## License

[Your chosen license, e.g., MIT]

---

This version of the README includes a new section on how to invite the bot to a Discord server, guiding users through the process step by step.
