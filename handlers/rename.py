from pyrogram import Client, filters

@Client.on_message(filters.command("rename") & filters.reply)
def rename_file(client, message):
    if not message.reply_to_message.document:
        message.reply_text("Reply to a file with /rename [new_name.extension]")
        return

    try:
        new_name = message.text.split(" ", 1)[1]
        file_id = message.reply_to_message.document.file_id
        message.reply_to_message.download(file_name=new_name)
        message.reply_text(f"✅ File renamed to {new_name}!")
    except IndexError:
        message.reply_text("⚠️ Please provide a new file name. Example: /rename newfile.pdf")
