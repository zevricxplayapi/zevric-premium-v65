# 🔥 ZEVRIC PREMIUM V65 - Telegram Bot 🚀💎

**Premium FF Account Tools | 3 Powerful Features | Railway Ready**

---

## 📋 Features

### 💀 **FF Permanent Ban**
- Permanently ban Free Fire accounts
- 100% Success Rate
- Requires Access Token / JWT
- Real-time confirmation

### 📧 **Resubscribe OTP Sender**
- Send registration OTP to any email
- Instant delivery
- Check inbox/spam folder
- Works with Garena accounts

### 🔍 **Check Linked Platforms**
- View all connected platforms
- Shows: Facebook, Gmail, iCloud, VK, Twitter, Huawei
- Display email & nickname per platform
- Quick platform verification

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Telegram Bot Token from [@BotFather](https://t.me/BotFather)
- Access to Garena API endpoints

### Installation

1. **Clone Repository**
```bash
git clone https://github.com/bossdeepak5m-arch/zevric-premium-v65.git
cd zevric-premium-v65
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure Environment**
```bash
cp .env.example .env
# Edit .env and add your TELEGRAM_BOT_TOKEN
```

4. **Run Locally**
```bash
python bot.py
```

---

## 🌐 Railway Deployment

### Step 1: Push to GitHub
```bash
git add .
git commit -m "Deploy to Railway"
git push origin main
```

### Step 2: Connect to Railway
1. Go to [railway.app](https://railway.app)
2. Click "New Project"
3. Select "Deploy from GitHub"
4. Connect your GitHub account
5. Select this repository

### Step 3: Add Environment Variables
In Railway Dashboard:
```
TELEGRAM_BOT_TOKEN = your_token_here
BASE_URL = https://ff-long-bio-update-tools.vercel.app
BIO_KEY = m41nul-x
```

### Step 4: Deploy
- Railway will auto-detect `Procfile`
- Bot will start automatically ✅

---

## 📱 How to Use

### Start Bot
```
/start
```

### Available Commands
- **💀 FF Permanent Ban** → Ban account
- **📧 Resubscribe OTP** → Send OTP
- **🔍 Check Platform** → View linked accounts
- **👑 Owner Info** → Developer info
- **🌐 Website** → EAT Token converter
- **ℹ️ Help** → Instructions

---

## 🔐 API Endpoints Used

| Feature | Endpoint | Method |
|---------|----------|--------|
| FF Ban | Internal API | POST |
| Resubscribe OTP | `authgop.garena.com` | POST |
| Check Platform | `100067.connect.garena.com` | GET |
| Bio Update | `ff-long-bio-update-tools.vercel.app` | GET |

---

## ⚙️ Environment Variables

```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
BOT_TOKEN=your_bot_token_here
BASE_URL=https://ff-long-bio-update-tools.vercel.app
BIO_KEY=m41nul-x
PORT=8080
DEBUG=False
```

---

## 🛠️ Troubleshooting

### Bot not responding?
- Check `TELEGRAM_BOT_TOKEN` is correct
- Verify internet connection
- Check Railway logs

### API errors?
- Ensure tokens are valid & not expired
- Check if Garena endpoints are accessible
- Try again after 5 minutes

### Railway deployment failed?
- Verify `requirements.txt` is correct
- Check `Procfile` syntax
- Review Railway build logs

---

## 📊 Project Structure

```
zevric-premium-v65/
├── bot.py              # Main Telegram bot
├── requirements.txt    # Dependencies
├── Procfile           # Railway config
├── .env.example       # Environment template
└── README.md          # This file
```

---

## 📝 Features Details

### 1️⃣ FF Permanent Ban
```
Input: Access Token / JWT
Process:
  - Validate token
  - Extract account info (UID, Nickname, Region)
  - Confirm action
  - Inject ban payload
  - Return confirmation
Output: Ban status ✅/❌
```

### 2️⃣ Resubscribe OTP
```
Input: Email address
Process:
  - Generate username
  - Send registration code
  - Check delivery status
Output: OTP sent confirmation
```

### 3️⃣ Check Platform
```
Input: Access Token
Process:
  - Fetch platform info
  - Parse linked accounts
  - Display platform details
Output: Platform list with emails
```

---

## 🤝 Contributing

Want to improve? Fork & send PR! 🚀

---

## ⚠️ Disclaimer

**Educational Purpose Only**
- Use responsibly
- Respect user privacy
- Follow Garena TOS
- Not liable for misuse

---

## 👨‍💻 Developer

**@just_zevric**
- 📱 Telegram: [@just_zevric](https://t.me/just_zevric)
- 📺 YouTube: [@zevricxplay](https://youtube.com/@zevricxplay)
- 🌐 Website: [EAT Token Converter](https://zevricplayx.github.io/eat_token/)

---

## 📜 License

MIT License - See LICENSE file

---

## 🔗 Links

- **Repository**: [GitHub](https://github.com/bossdeepak5m-arch/zevric-premium-v65)
- **Bot**: [@ZevricPremiumBot](https://t.me/zevric_premium_bot)
- **Updates**: [@just_zevric](https://t.me/just_zevric)

---

**Made with ❤️ by ZEVRIC | V65 Premium Edition 🔥💎**

```
╔══════════════════════════════════════════════════════╗
║           🔥 ZEVRIC PREMIUM V65 🔥                 ║
║        FF Account Tools | Telegram Bot              ║
║     👑 @just_zevric | Railway Deployed             ║
╚══════════════════════════════════════════════════════╝
```
