# 🚀 Multi-Utility Telegram Bot 🤖

A **powerful** and **feature-rich** Telegram bot for **file management, video conversion, compression, extraction, and more!** 🎯

---

## 🌟 Features & Commands

✅ **File Renaming** – Rename any uploaded file instantly. `/rename`
✅ **Video Conversion** – Convert videos to different formats (MP4, MKV, etc.). `/convert`
✅ **File Compression** – Zip multiple files together. `/compress`
✅ **File Extraction** – Extract ZIP & RAR files effortlessly. `/extract`
✅ **Image Watermarking** – Add a watermark text to your images. `/watermark`
✅ **Metadata Retrieval** – Get detailed metadata of any file. `/metadata`
✅ **Storage Cleanup** – Free up space by deleting old files. `/clear`
✅ **Video Thumbnail Generator** – Extract a thumbnail from videos. `/thumbnail`

🚀 **Fast & Secure** | 🎨 **User-Friendly** | ⚡ **Lightweight & Efficient**

---

## 🔧 Installation & Setup

### 📌 **Prerequisites**
- **Python 3.7+** installed ✅
- **API_ID & API_HASH** from [my.telegram.org](https://my.telegram.org/apps) ✅
- **BOT_TOKEN** from [@BotFather](https://t.me/BotFather) ✅

### 🔹 **Install Dependencies**
Run this command in the terminal:
```bash
pip install -r requirements.txt
```

### 🔹 **Run Locally**
```bash
python bot.py
```

---

## ☁️ Deployment

### 🚀 Deploy on **Render** (Easiest Way)
1️⃣ Fork this repository & edit `bot.py` with your API credentials.
2️⃣ Push your changes to GitHub.
3️⃣ Create a **Render Web Service** and link your GitHub repository.
4️⃣ Set the **Start Command** to:
   ```bash
   bash start.sh
   ```
5️⃣ Deploy & enjoy your bot! 🎉

### 🌍 Deploy on **VPS / Cloud Server**
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

