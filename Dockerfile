# Use official Python image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the bot files into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV API_ID=""
ENV API_HASH=""
ENV BOT_TOKEN=""
ENV FORCE_SUB_CHANNEL=""

# Run the bot
CMD ["python", "bot.py"]
