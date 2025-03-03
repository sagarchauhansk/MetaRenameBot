from pyrogram import Client, filters
import os
from config import API_ID, API_HASH, BOT_TOKEN

bot = Client(
    "MultiUtilityBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@bot.on_message(filters.command("start"))
def start(client, message):
    message.reply_text(f"Hello {message.from_user.first_name}! I am a multi-utility bot. Use /help for commands.")

@bot.on_message(filters.command("help"))
def help(client, message):
    message.reply_text("""
Commands:
🔹 /rename - Rename files
🔹 /convert - Convert video format
🔹 /compress - Zip files
🔹 /extract - Extract ZIP/RAR files
🔹 /watermark - Add watermark to images
🔹 /metadata - Get file metadata
🔹 /thumbnail - Extract video thumbnail
🔹 /clear - Cleanup storage
    """)

# Importing all handlers
from handlers import rename, convert, compress, extract, watermark, metadata, thumbnail

if __name__ == "__main__":
    bot.run()
