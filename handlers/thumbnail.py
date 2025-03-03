import os
import ffmpeg
from pyrogram import Client, filters

@Client.on_message(filters.command("thumbnail") & filters.reply)
async def extract_thumbnail(client, message):
    if not message.reply_to_message.video:
        await message.reply_text("⚠️ Reply to a video with `/thumbnail`.")
        return

    file_path = await message.reply_to_message.download()
    thumbnail_path = "thumbnail.jpg"

    ffmpeg.input(file_path).filter("scale", 320, -1).output(thumbnail_path, vframes=1).run()
    await message.reply_photo(thumbnail_path, caption="✅ Extracted Thumbnail!")

    os.remove(file_path)
    os.remove(thumbnail_path)
