import os
import logging
import ffmpeg
import zipfile
import rarfile
from pyrogram import Client, filters
from pyrogram.types import Message, Document, Video
from PIL import Image, ImageDraw, ImageFont
import shutil

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
    message.reply_text("👋 Hello! I am your Multi-Utility File Bot.\n\n"
                        "🔹 Use /convert to change video formats.\n"
                        "🔹 Use /rename to rename files.\n"
                        "🔹 Use /compress to zip files.\n"
                        "🔹 Use /extract to extract ZIP or RAR files.\n"
                        "🔹 Use /watermark to add watermark to images.\n"
                        "🔹 Use /metadata to get file metadata.\n"
                        "🔹 Use /thumbnail to generate video thumbnails.\n"
                        "🔹 Use /clear to free up space.")

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
    message.reply_text("🎞️ Send me a video with the desired format (e.g., MP4, MKV) in the caption.")

@bot.on_message(filters.video)
def handle_video(client, message: Message):
    if message.caption and message.caption.startswith("convert:"):
        format_type = message.caption.replace("convert:", "").strip().lower()
        input_path = message.download()
        output_path = input_path.rsplit(".", 1)[0] + f".{format_type}"

        ffmpeg.input(input_path).output(output_path).run()
        message.reply_video(output_path, caption=f"✅ Converted to {format_type}")
        os.remove(input_path)
        os.remove(output_path)

# 🖼️ Command: Generate Thumbnail
@bot.on_message(filters.command("thumbnail"))
def thumbnail(client, message: Message):
    message.reply_text("📸 Send me a video, and I'll generate a thumbnail from it.")

@bot.on_message(filters.video)
def handle_thumbnail(client, message: Message):
    input_path = message.download()
    output_path = input_path.rsplit(".", 1)[0] + "_thumbnail.jpg"

    # Extract a frame at 5 seconds
    ffmpeg.input(input_path, ss=5).output(output_path, vframes=1).run()

    message.reply_photo(output_path, caption="📷 Here is your video thumbnail.")
    os.remove(input_path)
    os.remove(output_path)

# 📦 Command: Compress Files
@bot.on_message(filters.command("compress"))
def compress(client, message: Message):
    message.reply_text("🗜️ Send multiple files to compress.")

@bot.on_message(filters.document)
def handle_compress(client, message: Message):
    zip_filename = "compressed_files.zip"
    with zipfile.ZipFile(zip_filename, "w") as zipf:
        file_path = message.download()
        zipf.write(file_path, os.path.basename(file_path))
        os.remove(file_path)
    message.reply_document(zip_filename, caption="📦 Here is your compressed file.")
    os.remove(zip_filename)

# 📂 Command: Extract ZIP/RAR Files
@bot.on_message(filters.command("extract"))
def extract(client, message: Message):
    message.reply_text("📤 Send me a ZIP or RAR file to extract.")

@bot.on_message(filters.document)
def handle_extract(client, message: Message):
    file_path = message.download()
    extract_folder = "extracted_files"
    os.makedirs(extract_folder, exist_ok=True)

    if file_path.endswith(".zip"):
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_folder)
    elif file_path.endswith(".rar"):
        with rarfile.RarFile(file_path, 'r') as rar_ref:
            rar_ref.extractall(extract_folder)

    extracted_files = os.listdir(extract_folder)
    for file in extracted_files:
        extracted_file_path = os.path.join(extract_folder, file)
        message.reply_document(extracted_file_path, caption=f"📂 Extracted: {file}")
        os.remove(extracted_file_path)

    os.remove(file_path)
    os.rmdir(extract_folder)

# 🏷️ Command: Add Watermark
@bot.on_message(filters.command("watermark"))
def watermark(client, message: Message):
    message.reply_text("🖋️ Send me an image with the watermark text in the caption.")

def add_watermark(input_path, output_path, text="Sample Watermark"):
    image = Image.open(input_path)
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    text_position = (10, 10)
    draw.text(text_position, text, fill=(255, 255, 255), font=font)
    image.save(output_path)

@bot.on_message(filters.photo)
def handle_watermark(client, message: Message):
    if message.caption and message.caption.startswith("watermark:"):
        watermark_text = message.caption.replace("watermark:", "").strip()
        input_path = message.download()
        output_path = input_path.rsplit(".", 1)[0] + "_watermarked.jpg"

        add_watermark(input_path, output_path, watermark_text)
        message.reply_photo(output_path, caption="✅ Here is your watermarked image.")
        os.remove(input_path)
        os.remove(output_path)

# 🧹 Command: Clear Storage
@bot.on_message(filters.command("clear"))
def clear_storage(client, message: Message):
    folder = "downloads"
    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.makedirs(folder)
    message.reply_text("🗑️ Storage cleared successfully.")

# 🚀 Run Bot
bot.run()
