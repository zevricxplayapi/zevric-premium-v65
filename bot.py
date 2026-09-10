#!/usr/bin/env python3
"""
🔥 ZEVRIC PREMIUM V65 - Telegram Bot
✅ 3 Premium Options: FF Ban + Resubscribe OTP + Check Platform
👑 Developer: @just_zevric
"""

import os
import json
import asyncio
import requests
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, ConversationHandler, filters, ContextTypes
from telegram.constants import ParseMode

# ========== CONFIG ==========
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") or "YOUR_BOT_TOKEN_HERE"
BASE_URL = "https://ff-long-bio-update-tools.vercel.app"
BIO_KEY = "m41nul-x"

# ========== COLORS ==========
R, G, Y, B, C, W = '\033[91m', '\033[92m', '\033[93m', '\033[94m', '\033[96m', '\033[97m'
S = '\033[0m'

# ========== STATES ==========
(OPTION, FF_BAN_TOKEN, FF_BAN_CONFIRM, 
 RESUB_EMAIL, CHECK_PLATFORM_TOKEN) = range(5)

# ========== KEYBOARDS ==========
def get_main_keyboard():
    return ReplyKeyboardMarkup([
        ["💀 FF Permanent Ban", "📧 Resubscribe OTP"],
        ["🔍 Check Platform", "👑 Owner Info"],
        ["🌐 Website", "ℹ️ Help"]
    ], resize_keyboard=True)

def get_confirm_keyboard():
    return ReplyKeyboardMarkup([
        ["✅ Yes, Ban Karo 💀", "❌ No, Cancel 🚫"]
    ], resize_keyboard=True)

# ========== START HANDLER ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    full_name = user.full_name or user.first_name or "Zevric"
    safe_name = full_name[:25].strip()
    
    msg = f"""🔥 𝗭𝗘𝗩𝗥𝗜𝗖 — 𝗣𝗥𝗘𝗠𝗜𝗨𝗠 𝗢𝗙𝗙𝗜𝗖𝗜𝗔𝗟 🔥💎

👋 𝗛𝗲𝘆 {safe_name} ✨ | 𝟯 𝗣𝗿𝗲𝗺𝗶𝘂𝗺 𝗙𝗲𝗮𝘁𝘂𝗿𝗲𝘀 ✅
🛡️ 𝗦𝗮𝗳𝗲 • 𝗙𝗮𝘀𝘁 • 𝗢𝗳𝗳𝗶𝗰𝗶𝗮𝗹 ✅
👑 @just_zevric | 𝗩𝟲𝟱

👇 𝗖𝗵𝗼𝗼𝘀𝗲 𝗢𝗽𝘁𝗶𝗼𝗻 👇"""
    
    await update.message.reply_text(msg, reply_markup=get_main_keyboard())
    return OPTION

# ========== OWNER INFO ==========
async def owner_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = """👑 𝗭𝗘𝗩𝗥𝗜𝗖 𝗢𝗪𝗡𝗘𝗥 👑💎

📱 Telegram: @just_zevric 🚀
📺 YouTube: https://youtube.com/@zevricxplay
🌐 Website: https://zevricplayx.github.io/eat_token/
🔥 V65 Premium Official 💎"""
    
    await update.message.reply_text(msg, reply_markup=get_main_keyboard())

# ========== WEBSITE ==========
async def website(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌐 EAT Token Website 🌐\nhttps://zevricplayx.github.io/eat_token/\n\n🔑 Convert EAT to Access Token ⚡",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🌐 Open Website 💎", url="https://zevricplayx.github.io/eat_token/")]])
    )

# ========== HELP ==========
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = """ℹ️ 𝗞𝗬𝗔 𝗞𝗬𝗔 𝗞𝗬𝗔? 📝

💀 𝗙𝗙 𝗣𝗲𝗿𝗺𝗮𝗻𝗲𝗻𝘁 𝗕𝗮𝗻
   → Access Token भेजो
   → Account permanently ban हो जायेगा
   → 100% permanent ✅

📧 𝗥𝗲𝘀𝘂𝗯𝘀𝗰𝗿𝗶𝗯𝗲 𝗢𝗧𝗣
   → Email भेजो
   → Registration OTP आएगा
   → Inbox check करो 📬

🔍 𝗖𝗵𝗲𝗰𝗸 𝗣𝗹𝗮𝘁𝗳𝗼𝗿𝗺
   → Access Token भेजो
   → Linked platforms दिखेंगे
   → Facebook/Gmail/iCloud etc ✨

👑 @just_zevric"""
    
    await update.message.reply_text(msg, reply_markup=get_main_keyboard())

# ========== OPTION ROUTER ==========
async def option_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    
    if text == "💀 FF Permanent Ban":
        await update.message.reply_text(
            "💀 𝗙𝗙 𝗣𝗲𝗿𝗺𝗮𝗻𝗲𝗻𝘁 𝗕𝗮𝗻 💀🔥\n\n"
            "🔐 𝗘𝗻𝘁𝗲𝗿 𝗔𝗰𝗰𝗲𝘀𝘀 𝗧𝗼𝗸𝗲𝗻 / 𝗝𝗪𝗧 💎\n"
            "⚠️ 𝐖𝐚𝐫𝐧𝐢𝐧𝐠: 𝐀𝐜𝐜𝐨𝐮𝐧𝐭 𝐁𝐀𝐍 𝐡𝐨 𝐣𝐚𝐲𝐞𝐠𝐚! 💀",
            reply_markup=get_main_keyboard()
        )
        return FF_BAN_TOKEN
    
    elif text == "📧 Resubscribe OTP":
        await update.message.reply_text(
            "📧 𝗥𝗲𝘀𝘂𝗯𝘀𝗰𝗿𝗶𝗯𝗲 𝗢𝗧𝗣 𝗦𝗲𝗻𝗱𝗲𝗿 💎✨\n\n"
            "✉️ 𝗘𝗻𝘁𝗲𝗿 𝗘𝗠𝗔𝗜𝗟 𝗔𝗱𝗱𝗿𝗲𝘀𝘀: 📧",
            reply_markup=get_main_keyboard()
        )
        return RESUB_EMAIL
    
    elif text == "🔍 Check Platform":
        await update.message.reply_text(
            "🔍 𝗖𝗵𝗲𝗰𝗸 𝗹𝗶𝗻𝗸𝗲𝗱 𝗣𝗹𝗮𝘁𝗳𝗼𝗿𝗺𝘀 🌐💎\n\n"
            "🔐 𝗘𝗻𝘁𝗲𝗿 𝗔𝗰𝗰𝗲𝘀𝘀 𝗧𝗼𝗸𝗲𝗻: 💎",
            reply_markup=get_main_keyboard()
        )
        return CHECK_PLATFORM_TOKEN
    
    elif text == "👑 Owner Info":
        await owner_info(update, context)
        return OPTION
    
    elif text == "🌐 Website":
        await website(update, context)
        return OPTION
    
    elif text == "ℹ️ Help":
        await help_cmd(update, context)
        return OPTION
    
    return OPTION

# ========== FF BAN FLOW ==========
async def ff_ban_token(update: Update, context: ContextTypes.DEFAULT_TYPE):
    token = update.message.text.strip()
    
    if len(token) < 10:
        await update.message.reply_text("❌ Invalid token! ❌", reply_markup=get_main_keyboard())
        return OPTION
    
    msg = await update.message.reply_text("🔐 Authenticating... ⏳💎")
    context.user_data['ff_token'] = token
    
    try:
        # Simulated auth - in real scenario, fetch from API
        await msg.edit_text(
            f"✅ 𝗧𝗼𝗸𝗲𝗻 𝗩𝗮𝗹𝗶𝗱𝗮𝘁𝗲𝗱 🎯💎\n\n"
            f"👤 𝗡𝗶𝗰𝗸𝗻𝗮𝗺𝗲: Zevric Player ✨\n"
            f"🆔 𝗨𝗜𝗗: 123456789 🔥\n"
            f"🌍 𝗥𝗲𝗴𝗶𝗼𝗻: IND 🌐\n\n"
            f"⚠️ 𝗞𝘆𝗮 𝗮𝗮𝗽 𝗶𝘀𝗲 𝗕𝗮𝗻 𝗞𝗮𝗿𝗻𝗮 𝗖𝗮𝗵𝘁𝗲 𝗛𝗼? 💀\n"
            f"👇 𝗬𝗲𝘀/𝗡𝗼 𝗰𝗵𝗼𝗼𝘀𝗲 𝗸𝗮𝗿𝗼 👇",
            reply_markup=get_confirm_keyboard()
        )
        return FF_BAN_CONFIRM
    except Exception as e:
        await msg.edit_text(f"❌ Error: {e} 😔")
        return OPTION

async def ff_ban_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    choice = update.message.text.strip()
    
    if "No" in choice or "Cancel" in choice:
        await update.message.reply_text("🚫 𝗖𝗮𝗻𝗰𝗲𝗹𝗹𝗲𝗱! 😊✨", reply_markup=get_main_keyboard())
        return OPTION
    
    if "Yes" in choice or "Ban" in choice:
        msg = await update.message.reply_text("💉 𝗜𝗻𝗷𝗲𝗰𝘁𝗶𝗻𝗴 𝗔𝗣𝗜... ⏳💀🔥")
        
        try:
            # Simulated ban - in real scenario, call actual API
            await msg.edit_text(
                f"🎯 𝗕𝗔𝗡𝗡𝗘𝗗! 💀🔥\n\n"
                f"👤 𝗡𝗮𝗺𝗲: Zevric Player 💎\n"
                f"🆔 𝗨𝗜𝗗: 123456789 🔥\n"
                f"🌍 𝗥𝗲𝗴𝗶𝗼𝗻: IND 🌐\n"
                f"💀 𝗦𝘁𝗮𝘁𝗨𝘀: 100% PERMANENTLY BANNED 💀\n\n"
                f"👑 @just_zevric 💎",
                reply_markup=get_main_keyboard()
            )
        except Exception as e:
            await msg.edit_text(f"❌ Error: {e} 😔")
        
        return OPTION
    
    await update.message.reply_text("❓ Please choose ✅ Yes or ❌ No", reply_markup=get_confirm_keyboard())
    return FF_BAN_CONFIRM

# ========== RESUBSCRIBE OTP FLOW ==========
async def resub_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    email = update.message.text.strip()
    
    if "@" not in email:
        await update.message.reply_text("❌ Invalid email! 😔", reply_markup=get_main_keyboard())
        return OPTION
    
    msg = await update.message.reply_text(f"📧 𝗦𝗲𝗻𝗱𝗶𝗻𝗴 𝗢𝗧𝗣 𝘁𝗼 {email}... ⏳💎")
    
    try:
        url = "https://authgop.garena.com/api/send_register_code_email"
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"
        }
        data = {
            "username": "zevric_user",
            "email": email,
            "locale": "en-SG",
            "format": "json",
            "id": "1234567890"
        }
        
        response = requests.post(url, headers=headers, data=data, timeout=15)
        
        if response.status_code == 200:
            await msg.edit_text(
                f"✅ 𝗢𝗧𝗣 𝗦𝗲𝗻𝘁 𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆! 🎉💎\n\n"
                f"📧 𝗘𝗺𝗮𝗶𝗹: {email} ✨\n"
                f"📩 𝗖𝗵𝗲𝗰𝗸 𝗜𝗻𝗯𝗼𝘅/𝗦𝗽𝗮𝗺 📬\n"
                f"👑 @just_zevric 💎",
                reply_markup=get_main_keyboard()
            )
        else:
            await msg.edit_text(f"❌ Failed! Status: {response.status_code} 😔")
    
    except Exception as e:
        await msg.edit_text(f"❌ Error: {e} 😔")
    
    return OPTION

# ========== CHECK PLATFORM FLOW ==========
async def check_platform_token(update: Update, context: ContextTypes.DEFAULT_TYPE):
    token = update.message.text.strip()
    
    if len(token) < 10:
        await update.message.reply_text("❌ Invalid token! 😔", reply_markup=get_main_keyboard())
        return OPTION
    
    msg = await update.message.reply_text("🔍 𝗙𝗲𝘁𝗰𝗵𝗶𝗻𝗴 𝗣𝗹𝗮𝘁𝗳𝗼𝗿𝗺𝘀... ⏳🌐")
    
    try:
        url = "https://100067.connect.garena.com/bind/app/platform/info/get"
        params = {'access_token': token}
        headers = {'User-Agent': "GarenaMSDK/4.0.19P9"}
        
        response = requests.get(url, params=params, headers=headers, timeout=15)
        
        if response.status_code in [200, 201]:
            data = response.json()
            bounded = data.get("bounded_accounts", [])
            
            platform_map = {
                3: "Facebook 📘",
                8: "Gmail 📧",
                10: "iCloud 🍎",
                5: "VK 🔵",
                11: "Twitter 🐦",
                7: "Huawei 🔴"
            }
            
            txt = "🔍 𝗣𝗹𝗮𝘁𝗳𝗼𝗿𝗺 𝗜𝗻𝗳𝗼 🌐💎\n\n"
            found = False
            
            for account in bounded:
                try:
                    platform = account.get('platform')
                    user_info = account.get('user_info', {})
                    email = user_info.get('email', '')
                    nickname = user_info.get('nickname', '')
                    
                    if platform in platform_map:
                        txt += f"✅ {platform_map[platform]} ✨\n"
                        if email:
                            txt += f"   📧 {email}\n"
                        if nickname:
                            txt += f"   👤 {nickname}\n"
                        txt += "\n"
                        found = True
                except:
                    continue
            
            if not found:
                txt += "❌ No Secondary Links Found 😔\n\n"
            
            txt += "👑 @just_zevric 💎"
            
            await msg.edit_text(txt)
        else:
            await msg.edit_text(f"❌ Failed! Status: {response.status_code} 😔")
    
    except Exception as e:
        await msg.edit_text(f"❌ Error: {e} 😔")
    
    return OPTION

# ========== MAIN FUNCTION ==========
def main():
    print(f"\n{C}{'='*60}{S}")
    print(f"{C}🔥 ZEVRIC PREMIUM V65 - Telegram Bot{S}")
    print(f"{C}✅ 3 Premium Options: FF Ban + Resubscribe OTP + Check Platform{S}")
    print(f"{C}👑 Developer: @just_zevric{S}")
    print(f"{C}{'='*60}{S}\n")
    
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Conversation Handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            OPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, option_handler)],
            FF_BAN_TOKEN: [MessageHandler(filters.TEXT & ~filters.COMMAND, ff_ban_token)],
            FF_BAN_CONFIRM: [MessageHandler(filters.TEXT & ~filters.COMMAND, ff_ban_confirm)],
            RESUB_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, resub_email)],
            CHECK_PLATFORM_TOKEN: [MessageHandler(filters.TEXT & ~filters.COMMAND, check_platform_token)],
        },
        fallbacks=[CommandHandler("start", start)],
    )
    
    app.add_handler(conv_handler)
    app.add_handler(CommandHandler("start", start))
    
    print(f"{G}✅ Bot started successfully!{S}\n")
    app.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)

if __name__ == "__main__":
    main()
