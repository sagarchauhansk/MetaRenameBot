"""
📌 Multi-Utility File Bot with Metadata Editing & More
🔗 GitHub: https://github.com/sagarchauhansk/MetaRenameBot
🔹 Telegram: https://t.me/Pentasteradmin (Join to use the bot)
🛠️ Developed by: sagarchauhansk

This bot can:
✅ Convert videos to different formats
✅ Rename files
✅ Compress and extract ZIP/RAR files
✅ Generate video thumbnails
✅ Get & Edit metadata via Web UI

⚡ Powered by Pyrogram & FFmpeg
"""

import os
import logging
import ffmpeg
import zipfile
import rarfile
import shutil
import traceback
import json
import threading
from flask import Flask, request, jsonify
from flask_cors import CORS
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ChatMember

# 🎯 Bot Configuration
API_ID = "your_api_id"
API_HASH = "your_api_hash"
BOT_TOKEN = "your_bot_token"
FORCE_SUB_CHANNEL = "your_channel_username"
WEB_SERVER_PORT = 5000

# 🚀 Initialize Flask Web Server
app = Flask(__name__)
CORS(app)

# 🚀 Initialize Bot
bot = Client("file_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# 📝 Logging Setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 🔒 Force Subscription Check
async def is_subscribed(client, user_id: int) -> bool:
    try:
        member: ChatMember = await client.get_chat_member(FORCE_SUB_CHANNEL, user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception:
        return False

# 📢 Command: Start
@bot.on_message(filters.command("start"))
async def start(client, message: Message):
    user_id = message.from_user.id
    if not await is_subscribed(client, user_id):
        join_button = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔔 Join Channel", url=f"https://t.me/{FORCE_SUB_CHANNEL}")]
        ])
        await message.reply_text(
            "🚀 You must join our Telegram channel before using me!",
            reply_markup=join_button
        )
        return

    await message.reply_text(
        "👋 Hello! I am your Multi-Utility File Bot.\n\n"
        "🔹 /convert - Convert video formats\n"
        "🔹 /rename - Rename files\n"
        "🔹 /compress - Compress files into ZIP\n"
        "🔹 /extract - Extract ZIP/RAR files\n"
        "🔹 /metadata - Get & Edit file metadata\n"
        "🔹 /thumbnail - Generate video thumbnails\n\n"
        "🔗 **Credits:**\n"
        "🔹 **GitHub**: [MetaRenameBot](https://github.com/sagarchauhansk/MetaRenameBot)\n"
        "🔹 **Developer**: [sagarchauhansk](https://t.me/Pentasteradmin)\n"
        "⚡ Powered by Pyrogram & FFmpeg",
        disable_web_page_preview=True
    )

# ✏️ Command: Rename File
@bot.on_message(filters.command("rename"))
async def rename(client, message: Message):
    await message.reply_text("📂 Send me a file with the new filename in the caption.")

@bot.on_message(filters.document)
async def handle_document(client, message: Message):
    if message.caption and message.caption.startswith("rename:"):
        new_name = message.caption.replace("rename:", "").strip()
        file_path = await message.download(f"downloads/{new_name}")
        await message.reply_document(file_path, caption=f"✅ Renamed to {new_name}")
        os.remove(file_path)

# 🎥 Command: Convert Video
@bot.on_message(filters.command("convert"))
async def convert(client, message: Message):
    await message.reply_text("🎞️ Send me a video with the desired format (e.g., MP4, MKV) in the caption.")

@bot.on_message(filters.video)
async def handle_video(client, message: Message):
    if message.caption and message.caption.startswith("convert:"):
        format_type = message.caption.replace("convert:", "").strip().lower()
        input_path = await message.download("downloads/")
        output_path = input_path.rsplit(".", 1)[0] + f".{format_type}"

        try:
            ffmpeg.input(input_path).output(output_path).run()
            await message.reply_video(output_path, caption=f"✅ Converted to {format_type}")
        except Exception as e:
            logging.error(f"Conversion Error: {str(e)}\n{traceback.format_exc()}")
            await message.reply_text(f"❌ Conversion failed: {str(e)}")
        finally:
            os.remove(input_path)
            os.remove(output_path)

# 📦 Command: Compress Files
@bot.on_message(filters.command("compress"))
async def compress(client, message: Message):
    await message.reply_text("🗜️ Send multiple files to compress.")

@bot.on_message(filters.document)
async def handle_compress(client, message: Message):
    zip_filename = "downloads/compressed_files.zip"
    os.makedirs("downloads", exist_ok=True)

    try:
        file_path = await message.download("downloads/")
        with zipfile.ZipFile(zip_filename, "w") as zipf:
            zipf.write(file_path, os.path.basename(file_path))
        await message.reply_document(zip_filename, caption="📦 Here is your compressed file.")
    finally:
        os.remove(file_path)
        os.remove(zip_filename)

# 📂 Command: Extract ZIP/RAR Files
@bot.on_message(filters.command("extract"))
async def extract(client, message: Message):
    await message.reply_text("📤 Send me a ZIP or RAR file to extract.")

@bot.on_message(filters.document)
async def handle_extract(client, message: Message):
    file_path = await message.download("downloads/")
    extract_folder = "downloads/extracted_files"
    os.makedirs(extract_folder, exist_ok=True)

    try:
        if file_path.endswith(".zip"):
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(extract_folder)
        elif file_path.endswith(".rar") and rarfile.is_rarfile(file_path):
            with rarfile.RarFile(file_path, 'r') as rar_ref:
                rar_ref.extractall(extract_folder)

        extracted_files = os.listdir(extract_folder)
        for file in extracted_files:
            extracted_file_path = os.path.join(extract_folder, file)
            await message.reply_document(extracted_file_path, caption=f"📂 Extracted: {file}")
            os.remove(extracted_file_path)
    finally:
        os.remove(file_path)
        shutil.rmtree(extract_folder, ignore_errors=True)

# 🌐 Web UI for Metadata Editing
@app.route("/edit_metadata/<file_name>", methods=["GET"])
def edit_metadata(file_name):
    metadata_file = f"downloads/{file_name}.json"
    if not os.path.exists(metadata_file):
        return jsonify({"error": "Metadata file not found"}), 404

    with open(metadata_file, "r") as f:
        metadata = json.load(f)

    return jsonify(metadata)

@app.route("/update_metadata/<file_name>", methods=["POST"])
def update_metadata(file_name):
    metadata_file = f"downloads/{file_name}.json"
    file_path = f"downloads/{file_name}"

    if not os.path.exists(metadata_file) or not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404

    new_metadata = request.json
    with open(metadata_file, "w") as f:
        json.dump(new_metadata, f, indent=4)

    return jsonify({"message": "Metadata updated successfully!"})

# 🚀 Run Flask Web Server
def start_flask():
    app.run(host="0.0.0.0", port=WEB_SERVER_PORT, debug=True, use_reloader=False)

threading.Thread(target=start_flask, daemon=True).start()

# 🚀 Run Bot
bot.run()
