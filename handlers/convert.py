import os
import ffmpeg
from pyrogram import Client, filters

@Client.on_message(filters.command("convert") & filters.reply)
async def convert_video(client, message):
    if not message.reply_to_message.video:
        await message.reply_text("⚠️ Reply to a video with `/convert format` (e.g., mp4, mkv).")
        return

    try:
        new_format = message.text.split(" ", 1)[1]
        input_file = await message.reply_to_message.download()
        output_file = os.path.splitext(input_file)[0] + "." + new_format

        ffmpeg.input(input_file).output(output_file).run()
        await message.reply_video(output_file, caption=f"✅ Converted to `{new_format}`!")

        os.remove(input_file)
        os.remove(output_file)
    except IndexError:
        await message.reply_text("⚠️ Please specify a format. Example: `/convert mkv`")
