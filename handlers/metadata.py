import os
from pyrogram import Client, filters

@Client.on_message(filters.command("metadata") & filters.reply)
async def get_metadata(client, message):
    if not message.reply_to_message.document:
        await message.reply_text("⚠️ Reply to a file with `/metadata`.")
        return

    file_path = await message.reply_to_message.download()
    file_size = os.path.getsize(file_path)

    await message.reply_text(f"📂 File: `{message.reply_to_message.document.file_name}`\n📏 Size: `{file_size} bytes`")
    os.remove(file_path)
