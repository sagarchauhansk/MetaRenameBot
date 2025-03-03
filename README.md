# 🚀 Multi-Utility Telegram Bot 🤖

A **powerful** and **feature-rich** Telegram bot for **file management, renaming, video conversion, compression, extraction, and more!** 🎯

---

## 🌟 Features & Commands

✅ **Force Subscription** – Requires users to join a channel before using the bot.
   ```
   Auto-Check on Start
   ```
✅ **File Renaming** – Rename any uploaded file instantly.  
   ```
   /rename
   ```
✅ **Custom Thumbnails** – Users can set and retrieve thumbnails.
   ```
   /set_thumbnail
   /show_thumbnail
   ```
✅ **Video Conversion** – Convert videos to different formats (MP4, MKV, etc.).  
   ```
   /convert
   ```
✅ **File Compression** – Zip multiple files together.  
   ```
   /compress
   ```
✅ **File Extraction** – Extract ZIP & RAR files effortlessly.  
   ```
   /extract
   ```
✅ **Image Watermarking** – Add a watermark text to your images.  
   ```
   /watermark
   ```
✅ **Metadata Retrieval** – Get detailed metadata of any file.  
   ```
   /metadata
   ```
✅ **Storage Cleanup** – Free up space by deleting old files.  
   ```
   /clear
   ```
✅ **Video Thumbnail Generator** – Extract a thumbnail from videos.  
   ```
   /thumbnail
   ```

🚀 **Fast & Secure** | 🎨 **User-Friendly** | ⚡ **Lightweight & Efficient**

---

## 🔧 Installation & Setup

### 📌 **Prerequisites**
- **Python 3.7+** installed ✅
- **API_ID & API_HASH** from [my.telegram.org](https://my.telegram.org/apps) ✅
- **BOT_TOKEN** from [@BotFather](https://t.me/BotFather) ✅

---

## ⚙️ API Settings & Environment Variables

Before running the bot, set the following environment variables:

```
API_ID = your_api_id
API_HASH = your_api_hash
BOT_TOKEN = your_bot_token
FORCE_SUB_CHANNEL = your_channel
```

You can set them in **Render**, **Heroku**, or export them in your terminal:

```bash
export API_ID="your_api_id"
export API_HASH="your_api_hash"
export BOT_TOKEN="your_bot_token"
export FORCE_SUB_CHANNEL="your_channel"
```

---

## ☁️ Deployment

<details>
<summary>🚀 Deploy on Render (Easiest Way)</summary>

1️⃣ Fork this repository & edit `bot.py` with your API credentials.  
2️⃣ Push your changes to GitHub.  
3️⃣ Create a **Render Web Service** and link your GitHub repository.  
4️⃣ Set the **Start Command** to:
   ```bash
   bash start.sh
   ```
5️⃣ Deploy & enjoy your bot! 🎉

</details>

<details>
<summary>🌍 Deploy on VPS / Cloud Server</summary>

1️⃣ Install required packages:
   ```bash
   sudo apt update && sudo apt install python3 ffmpeg zip unzip -y
   ```
2️⃣ Clone the repo:
   ```bash
   git clone https://github.com/sagarchauhansk/YourRepoName.git
   ```
3️⃣ Go inside the folder:
   ```bash
   cd YourRepoName
   ```
4️⃣ Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5️⃣ Run the bot:
   ```bash
   python bot.py
   ```

</details>

<details>
<summary>☁️ Deploy on Heroku</summary>

1️⃣ Install Heroku CLI & login:
   ```bash
   heroku login
   ```
2️⃣ Create a new Heroku app:
   ```bash
   heroku create your-app-name
   ```
3️⃣ Add a Git remote:
   ```bash
   heroku git:remote -a your-app-name
   ```
4️⃣ Push the code to Heroku:
   ```bash
   git push heroku main
   ```
5️⃣ Set required environment variables in Heroku dashboard.  
6️⃣ Start the bot:
   ```bash
   heroku ps:scale worker=1
   ```

</details>

---

## 📜 **Configuration Files**

### 📂 `requirements.txt`
```txt
pyrogram
tgcrypto
ffmpeg-python
pillow
rarfile
zipfile
```

### 📂 `start.sh`
```bash
#!/bin/bash
python bot.py
```

---

## 👤 **Owner Details**
- **👨‍💻 Developer:** Sagar Chauhan  
- **🔗 GitHub:** [Sagar Chauhan](https://github.com/sagarchauhansk)  
- **📩 Telegram:** [📨 Contact on Telegram](https://t.me/Pentasteradmin)  

💡 **Suggestions & Contributions are Welcome!** 🤝

---

### ⭐ **Support the Project**
If you find this bot helpful, please give it a **star ⭐** on GitHub! It keeps me motivated to improve it further! 🚀🎉
