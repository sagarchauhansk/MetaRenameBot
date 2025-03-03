# 📂 Multi-Utility Telegram Bot

A powerful Telegram bot for file management, video conversion, compression, extraction, and more!

## 🌟 Features
✅ **File Renaming** – Rename any file easily.
✅ **Video Conversion** – Convert videos to different formats (MP4, MKV, etc.).
✅ **File Compression** – Compress multiple files into a ZIP.
✅ **File Extraction** – Extract ZIP & RAR files.
✅ **Image Watermarking** – Add text watermarks to images.
✅ **Metadata Retrieval** – Get detailed metadata of uploaded files.
✅ **Storage Cleanup** – Free up space by deleting old files.
✅ **Video Thumbnail Generator** – Extract thumbnails from videos.

## 🚀 Deployment

### 🔹 Deploy on **Render**
1. Fork this repository & edit `bot.py` with your API credentials.
2. Create a `requirements.txt` file:
   ```
   pyrogram
tgcrypto
ffmpeg-python
pillow
rarfile
   ```
3. Create a `start.sh` file:
   ```bash
   #!/bin/bash
   python bot.py
   ```
4. Push your changes to GitHub.
5. Deploy the bot on [Render](https://render.com/) using your GitHub repo.

## 🛠 Setup & Usage
1. Get **API_ID** and **API_HASH** from [my.telegram.org](https://my.telegram.org/apps).
2. Get **BOT_TOKEN** from [@BotFather](https://t.me/BotFather).
3. Run locally:
   ```bash
   python bot.py
   ```
4. Deploy on a server (VPS/Render/Heroku).

## 👤 Owner Details
- **Owner:** Your Name
- **GitHub:** [YourGitHubProfile](https://github.com/YourGitHubProfile)
- **Telegram:** [@YourTelegramUsername](https://t.me/YourTelegramUsername)
- **Email:** your.email@example.com

---
### 📢 Contributions & Issues
Feel free to fork, modify, and contribute! Report issues via GitHub.

🔹 **Star ⭐ this repo if you find it useful!**

