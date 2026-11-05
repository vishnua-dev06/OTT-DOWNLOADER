# OTT-DOWNLOADER Bot 🎬

A powerful Telegram bot designed to download content from popular OTT platforms (such as JioHotstar, Zee5, etc.) with Widevine DRM decryption support. The bot can upload downloaded media directly to Telegram (up to 4GB with Telegram Session String) or directly to Google Drive / Team Drive.

---

## 📑 Table of Contents

- [Features](#-features)
- [Project Directory Structure](#-project-directory-structure)
- [Prerequisites](#-prerequisites)
- [Environment Variables](#-environment-variables)
- [Deployment Guide](#-deployment-guide)
  - [Deploy on Koyeb (Recommended)](#1-deploy-on-koyeb-recommended)
  - [Deploy on Heroku](#2-deploy-on-heroku)
  - [Deploy with Docker (VPS / Local)](#3-deploy-with-docker-vps--local)
  - [Manual Run on Local / VPS](#4-manual-run-on-local--vps)
- [Bot Commands](#-bot-commands)
  - [User Commands](#user-commands)
  - [Owner / Admin Commands](#owner--admin-commands)
- [Troubleshooting & FAQ](#-troubleshooting--faq)
- [Disclaimer](#-disclaimer)

---

## ✨ Features

- **Widevine DRM Decryption**: Built-in support for `pywidevine` and `mp4decrypt` to process DRM-protected streams.
- **Multi-OTT Support**: Download video streams from JioHotstar, Zee5, and more.
- **Dual Upload Destinations**:
  - **Telegram**: Uploads up to 2GB via standard bot token, or up to 4GB using a Pyrogram User Session String.
  - **Google Drive**: Direct upload to standard folders or Google Workspace Team Drives / Shared Drives.
- **Database & User Management**: MongoDB integration to manage user authorizations, subscription tiers, and download quotas.
- **Custom Metadata & Thumbnails**: Custom video titles, metadata tags, and personalized thumbnails.
- **Admin Control Panel**: Broadcasting messages to all users, user authorization controls, runtime server statistics, and log inspections.

---

## 📁 Project Directory Structure

```text
OTT-DOWNLOADER/
├── Dockerfile                # Docker container definition with system packages (ffmpeg, aria2, libmagic)
├── Procfile                  # Process file for Heroku / buildpack workers (worker: python3 bot.py)
├── README.md                 # Project documentation and deployment guides
├── app.json                  # One-click deployment specification for Heroku
├── bot.py                    # Main Telegram bot application & event handlers
├── config.py                 # Configuration loader reading environment variables
├── jvdb.py                   # MongoDB asynchronous client & user management methods
├── jvdrive.py                # Google Drive API upload and authentication helper
├── jvripper.py               # Core download, decryption, and processing pipeline
├── requirements.txt          # Python library dependencies
├── util.py                   # Utility functions for media info, formatting, and file handling
├── .dockerignore             # Files excluded from Docker image builds
├── .gitignore               # Files excluded from Git version control
├── ott/                      # Precompiled helper binaries and tools
│   ├── aria2c               # High-speed segmented download binary
│   ├── mp4decrypt            # Widevine decryption binary for MP4 streams
│   └── __init.py
└── pywidevine/               # Widevine CDM implementation & license processing
    ├── cdm/                  # Content Decryption Module formats, keys, and session configs
    │   ├── devices/          # CDM device client IDs and private keys
    │   └── formats/          # Protobuf definitions for Widevine licenses
    ├── decrypt/              # Custom stream decryptors
    ├── getPSSH.py            # PSSH extraction utility
    └── __init__.py
```

---

## 🔑 Prerequisites

Before deploying, ensure you have gathered the following:

1. **Telegram API Credentials**:
   - `API_ID` & `API_HASH`: Get them from [my.telegram.org](https://my.telegram.org).
   - `BOT_TOKEN`: Create a bot with [@BotFather](https://t.me/BotFather) on Telegram and copy the bot token.
2. **MongoDB Database**:
   - A free MongoDB cluster from [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).
   - Get the connection URI (e.g., `mongodb+srv://<user>:<password>@cluster0.mongodb.net/?retryWrites=true&w=majority`).
3. **Your Telegram User ID**:
   - Get your numeric Telegram ID from [@userinfobot](https://t.me/userinfobot) to set as `OWNER_ID`.
4. **Log Channel ID**:
   - Create a private Telegram channel, add your bot as an admin, and fetch the channel ID (usually starts with `-100...`).
5. **(Optional) 4GB Telegram Upload Session**:
   - A Pyrogram / Pyrofork session string for uploading files up to 4GB.
6. **(Optional) Google Drive**:
   - Google Drive Folder ID, Service Account credentials, or Team Drive ID.

---

## ⚙️ Environment Variables

Configure the following variables in your platform settings (or in a `.env` / `config.env` file for local development):

| Variable | Required | Description | Example / Default |
| :--- | :---: | :--- | :--- |
| `API_ID` | **Yes** | Telegram API ID from [my.telegram.org](https://my.telegram.org) | `17108931` |
| `API_HASH` | **Yes** | Telegram API Hash from [my.telegram.org](https://my.telegram.org) | `436b24700208cae55ded351d8f...` |
| `BOT_TOKEN` | **Yes** | Telegram Bot Token from [@BotFather](https://t.me/BotFather) | `8162787823:AAEIHC9...` |
| `DB_URL` | **Yes** | MongoDB connection string | `mongodb+srv://user:pass@cluster.mongodb.net/...` |
| `OWNER_ID` | **Yes** | Numeric Telegram ID of the bot owner(s) (space-separated for multiple) | `5300197778` |
| `LOG_CHANNEL` | **Yes** | Channel ID for bot operational logs | `-1002784468904` |
| `SESSION_STRING` | No | Pyrogram / Pyrofork User Session String for 4GB uploads | `BQEFD8MAWH9...` |
| `PROXY` | No | Proxy URL for bypassing geographical restrictions | `http://user:pass@ip:port` |
| `HOTSTAR_USER_TOKEN` | No | User token JWT for JioHotstar | `eyJhbGci...` |
| `ZEE5_TOKEN` | No | Authentication token for Zee5 | `eyJraWQi...` |
| `GDRIVE_FOLDER_ID` | No | Target Google Drive folder ID for uploads | `12JYZZlAlt5g...` |
| `IS_TEAM_DRIVE` | No | Set to `True` if using a Shared / Team Drive | `False` |
| `USE_SERVICE_ACCOUNTS` | No | Set to `True` if using Google Service Accounts | `False` |
| `INDEX_LINK` | No | Cloudflare / Google Drive index URL | `https://index.example.com` |
| `END_NAME` | No | Text appended to the end of downloaded video file names | `OTT_Downloader` |
| `METADATA_NAME` | No | Custom channel / author credit in media metadata | `@MyChannel` |
| `TG_SPLIT_SIZE` | No | Max file split threshold for Telegram (in bytes) | `2000000000` (or `4000000000`) |
| `TEMP_DIR` | No | Temporary directory for processing media | `output` |

---

## 🚀 Deployment Guide

### 1. Deploy on Koyeb (Recommended)

[Koyeb](https://www.koyeb.com) is a serverless platform that provides a free Eco tier, automated GitHub builds, and seamless Docker execution.

#### Step 1: Push Repository to GitHub
Ensure your repository contains the code and `Dockerfile`:
```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

#### Step 2: Create a Service on Koyeb
1. Sign up or log into [Koyeb Console](https://app.koyeb.com/).
2. Click **Create Service**.
3. Under **Deployment method**, select **GitHub**.
4. Authorize your GitHub account and choose your repository: `vishnua-dev06/OTT-DOWNLOADER`.
5. Select the `main` branch.

#### Step 3: Choose Service Type
- Select **Worker** service.
  > **Note**: A Telegram bot runs continuously as a background process polling for messages. Selecting **Worker** ensures it runs 24/7 without needing an HTTP port or health check.
  *(If you select **Web**, disable the HTTP health check or configure it to TCP).*

#### Step 4: Configure Builder
- Under **Builder**, select **Dockerfile**.
- The build will automatically use the repository's [`Dockerfile`](./Dockerfile) which pre-installs `ffmpeg`, `aria2`, `mediainfo`, and `libmagic1`.

#### Step 5: Configure Instance & Environment Variables
- **Instance Type**: Choose `Free` (Nano) or any Eco instance.
- **Environment Variables**: Add all your environment variables under the **Environment variables** section:
  - `API_ID`
  - `API_HASH`
  - `BOT_TOKEN`
  - `DB_URL`
  - `OWNER_ID`
  - `LOG_CHANNEL`
  - *(Any other optional variables like `HOTSTAR_USER_TOKEN`, `ZEE5_TOKEN`, etc.)*

#### Step 6: Deploy
1. Click **Deploy**.
2. Koyeb will build the Docker container and start your bot worker.
3. Open the **Runtime Logs** tab in Koyeb to confirm the bot has connected to Telegram:
   ```text
   [+] Bot Started Successfully!
   ```

---

### 2. Deploy on Heroku

1. Click the button below or fork the repository:
   [![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)
2. Fill in the required environment variables in the Heroku dashboard.
3. Make sure the `worker` dyno is switched **ON** in the **Resources** tab:
   ```bash
   heroku ps:scale worker=1 -a your-app-name
   ```

---

### 3. Deploy with Docker (VPS / Local)

If you have a Linux VPS (Ubuntu/Debian) or want to run with Docker locally:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/vishnua-dev06/OTT-DOWNLOADER.git
   cd OTT-DOWNLOADER
   ```

2. **Create a `.env` file:**
   ```bash
   nano .env
   ```
   Add your variables:
   ```env
   API_ID=123456
   API_HASH=your_api_hash
   BOT_TOKEN=123456:ABC-DEF...
   DB_URL=mongodb+srv://...
   OWNER_ID=5300197778
   LOG_CHANNEL=-100123456789
   ```

3. **Build the Docker Image:**
   ```bash
   docker build -t ott-downloader-bot .
   ```

4. **Run the Container in Background:**
   ```bash
   docker run -d --name ott_bot --restart unless-stopped --env-file .env ott-downloader-bot
   ```

5. **View Logs:**
   ```bash
   docker logs -f ott_bot
   ```

---

### 4. Manual Run on Local / VPS

If you prefer running directly in Python:

1. **Install System Dependencies (Ubuntu/Debian):**
   ```bash
   sudo apt update
   sudo apt install -y ffmpeg aria2 mediainfo libmagic1 python3 python3-pip python3-venv
   ```

2. **Clone and Setup Virtual Environment:**
   ```bash
   git clone https://github.com/vishnua-dev06/OTT-DOWNLOADER.git
   cd OTT-DOWNLOADER
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Python Packages:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Set Permissions for Helpers:**
   ```bash
   chmod +x ott/aria2c ott/mp4decrypt
   ```

5. **Start the Bot:**
   ```bash
   python3 bot.py
   ```

---

## 🤖 Bot Commands

### User Commands

| Command | Description |
| :--- | :--- |
| `/start` | Starts the bot and shows the welcome message |
| `/help` | Displays help information and guide |
| `/about` | Bot information and developer details |
| `/ott` or `/otts` | Shows the list of supported OTT platforms |
| `/hs <url>` | Download video from JioHotstar |
| `/zee5 <url>` | Download video from Zee5 |
| `/rip <url>` or `/dl <url>` | Download video from supported OTT platforms |
| `/upload_mode` or `/mode` | Switch upload destination between **Telegram** and **Google Drive** |
| `/myplan` or `/usage` | View your subscription details and remaining daily quota |
| `/plans` | View available premium plans and pricing |
| `/getthumb` | View your currently saved custom thumbnail |
| `/delthumb` | Delete your custom thumbnail |

### Owner / Admin Commands

| Command | Syntax | Description |
| :--- | :--- | :--- |
| `/auth` | `/auth <user_id>` | Authorize a user to use the bot |
| `/unauth` | `/unauth <user_id>` | Revoke a user's authorization |
| `/sub` | `/sub <user_id> <days> <quota>` | Grant or renew a user's subscription |
| `/broadcast` or `/b` | `/broadcast (reply to msg)` | Broadcast a message to all registered users |
| `/status` or `/stats` | `/status` | View system stats (CPU, RAM, Uptime, Disk space) |
| `/clean` | `/clean` | Delete cached downloads and temporary output files |
| `/logs` or `/log` | `/logs` | Get the latest runtime `log.txt` file |

---

## ❓ Troubleshooting & FAQ

#### Q: Bot crashes with `Could not find a version that satisfies the requirement pywidevine`
> The Widevine CDM files are bundled locally inside the [`pywidevine`](./pywidevine) folder of this repository. You do not need to install an external package from PyPI.

#### Q: How do I get 4GB uploads on Telegram?
> By default, standard Telegram bot tokens can only upload files up to 2GB. To enable 4GB uploads, generate a Pyrogram / Pyrofork session string using your Telegram account and set the `SESSION_STRING` environment variable.

#### Q: Koyeb deployment health check fails
> If deploying on Koyeb as a **Web Service**, Koyeb will expect an open HTTP port. To resolve this, make sure to set the **Service Type** to **Worker** in Koyeb, which does not require an HTTP health check.

---

## ⚠️ Disclaimer

This repository is created **strictly for educational and research purposes**. 
- The developers and contributors are not responsible for any misuse of this software.
- Users are solely responsible for ensuring compliance with the Terms of Service of any third-party platforms, as well as applicable local copyright laws.
