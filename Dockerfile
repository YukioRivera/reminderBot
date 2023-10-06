FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the bot script and requirements file
COPY bot.py .
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Run the bot script
CMD ["python", "./bot.py"]
