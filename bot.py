import os
import logging
import ffmpeg
import zipfile
import rarfile
import shutil
import traceback
from pyrogram import Client, filters
from pyrogram.types import Message
from PIL import Image, ImageDraw, ImageFont

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
async def start(client, message: Message):
    await message.reply_text(
        "👋 Hello! I am your Multi-Utility File Bot.\n\n"
        "🔹 Use /convert to change video formats.\n"
        "🔹 Use /rename to rename files.\n"
        "🔹 Use /compress to zip files.\n"
        "🔹 Use /extract to extract ZIP or RAR files.\n"
        "🔹 Use /watermark to add watermark to images.\n"
        "🔹 Use /metadata to get file metadata.\n"
        "🔹 Use /thumbnail to generate video thumbnails.\n"
        "🔹 Use /clear to free up space."
    )

# 📝 Command: Rename File
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
        except ffmpeg.Error as e:
            logging.error(f"FFmpeg Error: {str(e)}\n{traceback.format_exc()}")
            await message.reply_text(f"❌ Conversion failed: {str(e)}")
        finally:
            os.remove(input_path)
            if os.path.exists(output_path):
                os.remove(output_path)

# 📸 Command: Generate Thumbnail
@bot.on_message(filters.command("thumbnail"))
async def thumbnail(client, message: Message):
    await message.reply_text("📸 Send me a video, and I'll generate a thumbnail from it.")

@bot.on_message(filters.video)
async def handle_thumbnail(client, message: Message):
    input_path = await message.download("downloads/")
    output_path = input_path.rsplit(".", 1)[0] + "_thumbnail.jpg"

    try:
        ffmpeg.input(input_path, ss=5).output(output_path, vframes=1).run()
        await message.reply_photo(output_path, caption="📷 Here is your video thumbnail.")
    except Exception as e:
        logging.error(f"Thumbnail Generation Error: {str(e)}\n{traceback.format_exc()}")
        await message.reply_text(f"❌ Failed to generate thumbnail: {str(e)}")
    finally:
        os.remove(input_path)
        if os.path.exists(output_path):
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
    except Exception as e:
        logging.error(f"Compression Error: {str(e)}\n{traceback.format_exc()}")
        await message.reply_text(f"❌ Compression failed: {str(e)}")
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
        else:
            raise ValueError("Unsupported file format.")

        extracted_files = os.listdir(extract_folder)
        for file in extracted_files:
            extracted_file_path = os.path.join(extract_folder, file)
            await message.reply_document(extracted_file_path, caption=f"📂 Extracted: {file}")
            os.remove(extracted_file_path)
    except Exception as e:
        logging.error(f"Extraction Error: {str(e)}\n{traceback.format_exc()}")
        await message.reply_text(f"❌ Extraction failed: {str(e)}")
    finally:
        os.remove(file_path)
        shutil.rmtree(extract_folder, ignore_errors=True)

# 🏷️ Command: Add Watermark
@bot.on_message(filters.command("watermark"))
async def watermark(client, message: Message):
    await message.reply_text("🖋️ Send me an image with the watermark text in the caption.")

def add_watermark(input_path, output_path, text="Sample Watermark"):
    image = Image.open(input_path)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("arial.ttf", 30)
    text_position = (10, 10)
    draw.text(text_position, text, fill=(255, 255, 255), font=font)
    image.save(output_path)

@bot.on_message(filters.photo)
async def handle_watermark(client, message: Message):
    if message.caption and message.caption.startswith("watermark:"):
        watermark_text = message.caption.replace("watermark:", "").strip()
        input_path = await message.download("downloads/")
        output_path = input_path.rsplit(".", 1)[0] + "_watermarked.jpg"

        try:
            add_watermark(input_path, output_path, watermark_text)
            await message.reply_photo(output_path, caption="✅ Here is your watermarked image.")
        finally:
            os.remove(input_path)
            os.remove(output_path)

# 🧹 Command: Clear Storage
@bot.on_message(filters.command("clear"))
async def clear_storage(client, message: Message):
    shutil.rmtree("downloads", ignore_errors=True)
    os.makedirs("downloads")
    await message.reply_text("🗑️ Storage cleared successfully.")

# 🚀 Run Bot
bot.run()
