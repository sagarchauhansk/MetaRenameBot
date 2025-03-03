import os
import rarfile
import zipfile
from pyrogram import Client, filters

@Client.on_message(filters.command("extract") & filters.reply)
async def extract_file(client, message):
    if not message.reply_to_message.document:
        await message.reply_text("⚠️ Reply to a ZIP or RAR file with `/extract`.")
        return

    file_path = await message.reply_to_message.download()
    extract_path = os.path.splitext(file_path)[0]

    if file_path.endswith(".zip"):
        with zipfile.ZipFile(file_path, "r") as zip_ref:
            zip_ref.extractall(extract_path)
    elif file_path.endswith(".rar"):
        with rarfile.RarFile(file_path, "r") as rar_ref:
            rar_ref.extractall(extract_path)
    else:
        await message.reply_text("⚠️ Unsupported format!")

    await message.reply_text(f"✅ Extracted to `{extract_path}`!")

    os.remove(file_path)
