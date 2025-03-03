import os
import logging
import ffmpeg
import zipfile
import rarfile
from pyrogram import Client, filters
from pyrogram.types import Message, Document, Video, Photo

# 🎯 Bot Configuration
API_ID = "your_api_id"
API_HASH = "your_api_hash"
BOT_TOKEN = "your_bot_token"

# 🚀 Initialize Bot
bot = Client("file_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# 📝 Logging Setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 📢 Command: Start
@bot.on_message(filters.command("start"))
def start(client, message: Message):
    message.reply_text(
        "👋 Hello! I am your Multi-Utility File Bot.

"
        "🔹 Use /convert to change video formats.
"
        "🔹 Use /rename to rename files.
"
        "🔹 Use /compress to zip files.
"
        "🔹 Use /extract to extract ZIP or RAR files.
"
        "🔹 Use /watermark to add watermark to images.
"
        "🔹 Use /metadata to get file metadata.
"
        "🔹 Use /thumbnail to generate video thumbnails.
"
        "🔹 Use /clear to free up space.

"
        "🔹 **Bot Developed by [Sagar Chauhan](https://github.com/sagarchauhansk)** 🎉"
    )

# ✏️ Command: Rename File
@bot.on_message(filters.command("rename"))
def rename(client, message: Message):
    message.reply_text("📂 Send me a file with the new filename in the caption.")

@bot.on_message(filters.document)
def handle_document(client, message: Message):
    if message.caption and message.caption.startswith("rename:"):
        new_name = message.caption.replace("rename:", "").strip()
        file_path = f"downloads/{new_name}"
        message.download(file_path)
        message.reply_document(file_path, caption=f"✅ Renamed to {new_name}")
        os.remove(file_path)

# 🎥 Command: Convert Video
@bot.on_message(filters.command("convert"))
def convert(client, message: Message):
    message.reply_text("🎥 Send me a video to convert to MP4 format.")

@bot.on_message(filters.video)
def handle_video(client, message: Message):
    input_path = message.download()
    output_path = input_path.replace(".mkv", ".mp4").replace(".avi", ".mp4")

    ffmpeg.input(input_path).output(output_path).run()
    message.reply_video(output_path, caption="✅ Converted to MP4!")
    os.remove(input_path)
    os.remove(output_path)

# 📦 Command: Compress Files
@bot.on_message(filters.command("compress"))
def compress(client, message: Message):
    message.reply_text("📦 Send me multiple files to compress into a ZIP.")

@bot.on_message(filters.command("extract"))
def extract(client, message: Message):
    message.reply_text("📂 Send me a ZIP or RAR file to extract.")

@bot.on_message(filters.command("clear"))
def clear(client, message: Message):
    folder = "downloads"
    if os.path.exists(folder):
        for file in os.listdir(folder):
            os.remove(os.path.join(folder, file))
    message.reply_text("🗑 Storage cleared successfully!")

# 🚀 Run Bot
bot.run()
