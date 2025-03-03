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
async def start(client, message):
    await message.reply_text(f"Hello {message.from_user.first_name}! I am a multi-utility bot. Use /help for commands.")

@bot.on_message(filters.command("help"))
async def help(client, message):
    await message.reply_text("""
Commands:
🔹 /rename - Rename files
🔹 /convert - Convert video format
🔹 /compress - Zip files
🔹 /extract - Extract ZIP/RAR files
🔹 /metadata - Get file metadata
🔹 /thumbnail - Extract video thumbnail
🔹 /clear - Cleanup storage
    """)

# Importing handlers correctly
import handlers.rename
import handlers.convert
import handlers.compress
import handlers.extract
import handlers.metadata
import handlers.thumbnail

if __name__ == "__main__":
    bot.run()
