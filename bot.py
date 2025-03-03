"""
📌 Multi-Utility File Bot with Metadata Editing
🔗 GitHub: https://github.com/sagarchauhansk/MetaRenameBot
🔹 Telegram: https://t.me/Pentasteradmin
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
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ChatMember

# 🎯 Bot Configuration
API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
FORCE_SUB_CHANNEL = os.environ.get("FORCE_SUB_CHANNEL")
WEB_SERVER_PORT = int(os.environ.get("PORT", 5000))  # Render assigns a dynamic port

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
        await message.reply_text("🚀 You must join our Telegram channel before using me!", reply_markup=join_button)
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

# 📊 Command: Get & Edit File Metadata
@bot.on_message(filters.command("metadata"))
async def metadata(client, message: Message):
    await message.reply_text("📁 Send me a file, and I'll provide a link to edit its metadata.")

@bot.on_message(filters.document | filters.video | filters.photo)
async def handle_metadata(client, message: Message):
    file_path = await message.download("downloads/")
    file_name = os.path.basename(file_path)

    try:
        metadata = ffmpeg.probe(file_path)
        metadata_json = json.dumps(metadata, indent=4)

        # Save metadata to a file
        metadata_file = f"downloads/{file_name}.json"
        with open(metadata_file, "w") as f:
            f.write(metadata_json)

        # Send user a link to edit metadata
        web_url = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}/edit_metadata/{file_name}"
        await message.reply_text(f"🔗 [Click here](<{web_url}>) to edit metadata.", disable_web_page_preview=True)
    except Exception as e:
        logging.error(f"Metadata Error: {str(e)}\n{traceback.format_exc()}")
        await message.reply_text("❌ Failed to extract metadata.")

# 🌐 Web UI for Metadata Editing
@app.route("/edit_metadata/<file_name>", methods=["GET"])
def edit_metadata(file_name):
    metadata_file = f"downloads/{file_name}.json"
    if not os.path.exists(metadata_file):
        return jsonify({"error": "Metadata file not found"}), 404

    with open(metadata_file, "r") as f:
        metadata = json.load(f)

    return render_template("edit_metadata.html", metadata=json.dumps(metadata, indent=4), file_name=file_name)

@app.route("/update_metadata/<file_name>", methods=["POST"])
def update_metadata(file_name):
    metadata_file = f"downloads/{file_name}.json"
    if not os.path.exists(metadata_file):
        return jsonify({"error": "Metadata file not found"}), 404

    new_metadata = request.json

    # Save updated metadata
    with open(metadata_file, "w") as f:
        json.dump(new_metadata, f, indent=4)

    return jsonify({"message": "Metadata updated successfully!"})

# 🚀 Start Flask Web Server on Render Assigned Port
def start_flask():
    app.run(host="0.0.0.0", port=WEB_SERVER_PORT, debug=True, use_reloader=False)

threading.Thread(target=start_flask, daemon=True).start()

# 🚀 Run Bot
bot.run()
