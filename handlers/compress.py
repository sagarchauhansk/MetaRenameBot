import zipfile
import os
from pyrogram import Client, filters

@Client.on_message(filters.command("compress") & filters.reply)
def compress_file(client, message):
    if not message.reply_to_message.document:
        message.reply_text("⚠️ Reply to a file with /compress.")
        return

    file_path = message.reply_to_message.download()
    zip_path = file_path + ".zip"

    with zipfile.ZipFile(zip_path, "w") as zipf:
        zipf.write(file_path, os.path.basename(file_path))

    message.reply_document(zip_path, caption="✅ File compressed!")

    os.remove(file_path)
    os.remove(zip_path)
