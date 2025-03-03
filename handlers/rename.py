from pyrogram import Client, filters
import os

@Client.on_message(filters.command("rename") & filters.reply)
async def rename_file(client, message):
    if not message.reply_to_message.document:
        await message.reply_text("⚠️ Reply to a file with `/rename new_name.extension`")
        return

    try:
        new_name = message.text.split(" ", 1)[1]
        file = await message.reply_to_message.download()
        os.rename(file, new_name)
        await message.reply_document(new_name, caption=f"✅ Renamed to `{new_name}`")
        os.remove(new_name)
    except IndexError:
        await message.reply_text("⚠️ Please provide a new file name. Example: `/rename newfile.pdf`")
