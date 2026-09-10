import os, json, requests, urllib.parse, asyncio, threading, base64, time, random, string
from datetime import datetime
from flask import Flask, render_template_string
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
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
MAJORLOGIN_REQ_DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x13MajorLoginReq.proto\"\xfa\n\n\nMajorLogin\x12\x12\n\nevent_time\x18\x03 \x01(\t\x12\x11\n\tgame_name\x18\x04 \x01(\t\x12\x13\n\x0bplatform_id\x18\x05 \x01(\x05\x12\x16\n\x0e\x63lient_version\x18\x07 \x01(\t\x12\x17\n\x0fsystem_software\x18\x08 \x01(\t\x12\x17\n\x0fsystem_hardware\x18\t \x01(\t\x12\x18\n\x10telecom_operator\x18\n \x01(\t\x12\x14\n\x0cnetwork_type\x18\x0b \x01(\t\x12\x14\n\x0cscreen_width\x18\x0c \x01(\r\x12\x15\n\rscreen_height\x18\r \x01(\r\x12\x12\n\nscreen_dpi\x18\x0e \x01(\t\x12\x19\n\x11processor_details\x18\x0f \x01(\t\x12\x0e\n\x06memory\x18\x10 \x01(\r\x12\x14\n\x0cgpu_renderer\x18\x11 \x01(\t\x12\x13\n\x0bgpu_version\x18\x12 \x01(\t\x12\x18\n\x10unique_device_id\x18\x13 \x01(\t\x12\x11\n\tclient_ip\x18\x14 \x01(\t\x12\x10\n\x08language\x18\x15 \x01(\t\x12\x0f\n\x07open_id\x18\x16 \x01(\t\x12\x14\n\x0copen_id_type\x18\x17 \x01(\t\x12\x13\n\x0b\x64\x65vice_type\x18\x18 \x01(\t\x12\'\n\x10memory_available\x18\x19 \x01(\x0b\x32\r.GameSecurity\x12\x14\n\x0c\x61\x63\x63\x65ss_token\x18\x1d \x01(\t\x12\x17\n\x0fplatform_sdk_id\x18\x1e \x01(\x05\x12\x1a\n\x12network_operator_a\x18) \x01(\t\x12\x16\n\x0enetwork_type_a\x18* \x01(\t\x12\x1c\n\x14\x63lient_using_version\x18\x39 \x01(\t\x12\x1e\n\x16\x65xternal_storage_total\x18< \x01(\x05\x12\"\n\x1a\x65xternal_storage_available\x18= \x01(\x05\x12\x1e\n\x16internal_storage_total\x18> \x01(\x05\x12\"\n\x1ainternal_storage_available\x18? \x01(\x05\x12#\n\x1bgame_disk_storage_available\x18@ \x01(\x05\x12\x1f\n\x17game_disk_storage_total\x18\x41 \x01(\x05\x12%\n\x1d\x65xternal_sdcard_avail_storage\x18\x42 \x01(\x05\x12%\n\x1d\x65xternal_sdcard_total_storage\x18\x43 \x01(\x05\x12\x10\n\x08login_by\x18I \x01(\x05\x12\x14\n\x0clibrary_path\x18J \x01(\t\x12\x12\n\nreg_avatar\x18L \x01(\x05\x12\x15\n\rlibrary_token\x18M \x01(\t\x12\x14\n\x0c\x63hannel_type\x18N \x01(\x05\x12\x10\n\x08\x63pu_type\x18O \x01(\x05\x12\x18\n\x10\x63pu_architecture\x18Q \x01(\t\x12\x1b\n\x13\x63lient_version_code\x18S \x01(\t\x12\x14\n\x0cgraphics_api\x18V \x01(\t\x12\x1d\n\x15supported_astc_bitset\x18W \x01(\r\x12\x1a\n\x12login_open_id_type\x18X \x01(\x05\x12\x18\n\x10\x61nalytics_detail\x18Y \x01(\x0c\x12\x14\n\x0cloading_time\x18\\ \x01(\r\x12\x17\n\x0frelease_channel\x18] \x01(\t\x12\x12\n\nextra_info\x18^ \x01(\t\x12 \n\x18\x61ndroid_engine_init_flag\x18_ \x01(\r\x12\x0f\n\x07if_push\x18\x61 \x01(\x05\x12\x0e\n\x06is_vpn\x18\x62 \x01(\x05\x12\x1c\n\x14origin_platform_type\x18\x63 \x01(\t\x12\x1d\n\x15primary_platform_type\x18\x64 \x01(\t\"5\n\x0cGameSecurity\x12\x0f\n\x07version\x18\x06 \x01(\x05\x12\x14\n\x0chidden_value\x18\x08 \x01(\x04\x62\x06proto3')
MAJORLOGIN_RES_DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x13MajorLoginRes.proto\"\x87\x05\n\rMajorLoginRes\x12\x12\n\naccount_id\x18\x01 \x01(\x03\x12\x13\n\x0block_region\x18\x02 \x01(\t\x12\x13\n\x0bnoti_region\x18\x03 \x01(\t\x12\x11\n\tip_region\x18\x04 \x01(\t\x12\x19\n\x11\x61gora_environment\x18\x05 \x01(\t\x12\x19\n\x11new_active_region\x18\x06 \x01(\t\x12\r\n\x05token\x18\x08 \x01(\t\x12\x0b\n\x03ttl\x18\t \x01(\x05\x12\x12\n\nserver_url\x18\n \x01(\t\x12\x16\n\x0e\x65mulator_score\x18\x0c \x01(\x03\x12\x32\n\tblacklist\x18\r \x01(\x0b\x32\x1f.MajorLoginRes.BlacklistInfoRes\x12\x31\n\nqueue_info\x18\x0f \x01(\x0b\x32\x1d.MajorLoginRes.LoginQueueInfo\x12\x0e\n\x06tp_url\x18\x10 \x01(\t\x12\x15\n\rapp_server_id\x18\x11 \x01(\x03\x12\x0f\n\x07\x61no_url\x18\x12 \x01(\t\x12\x0f\n\x07ip_city\x18\x13 \x01(\t\x12\x16\n\x0eip_subdivision\x18\x14 \x01(\t\x12\x0b\n\x03kts\x18\x15 \x01(\x03\x12\n\n\x02\x61k\x18\x16 \x01(\x0c\x12\x0b\n\x03\x61iv\x18\x17 \x01(\x0c\x1aQ\n\x10\x42lacklistInfoRes\x12\x12\n\nban_reason\x18\x01 \x01(\x05\x12\x17\n\x0f\x65xpire_duration\x18\x02 \x01(\x03\x12\x10\n\x08\x62\x61n_time\x18\x03 \x01(\x03\x1a\x66\n\x0eLoginQueueInfo\x12\r\n\x05\x41llow\x18\x01 \x01(\x08\x12\x16\n\x0equeue_position\x18\x02 \x01(\x03\x12\x16\n\x0eneed_wait_secs\x18\x03 \x01(\x03\x12\x15\n\rqueue_is_full\x18\x04 \x01(\x08\x62\x06proto3')
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
UNBIND_HTML = """<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><title>ZEVRIC Premium</title><style>body{font-family:Arial;background:#0a0a0a;color:#fff;padding:20px}.card{background:#1a1a1a;padding:25px;border-radius:15px;max-width:420px;margin:auto;border:2px solid #00ff88}</style></head><body><div class="card"><h2>🔥 ZEVRIC Premium V65 - 3 Options Added 💎</h2><p>💀 FF Ban | 📧 Resubscribe | 🔍 Platform</p></div></body></html>"""
@flask_app.route('/')
def home(): return "ZEVRIC PREMIUM V65 - 3 Options Added - @just_zevric Alive 💀📧🔍", 200
@flask_app.route('/health')
def health(): return "OK", 200
@flask_app.route('/unbind')
def unbind_page(): return render_template_string(UNBIND_HTML)
def run_flask():
    port=int(os.environ.get("PORT",8080))
    flask_app.run(host="0.0.0.0",port=port,debug=False,use_reloader=False)
threading.Thread(target=run_flask,daemon=True).start()
# ========== FIXED: FF BAN SECTION ==========

def decode_ff_name(b64_str):
    """Properly decode FF nickname with XOR decryption"""
    try:
        if not b64_str:
            return "Unknown"
        key = b"1e5898ccb8dfdd921f9bdea848768b64a201"
        b64_str = b64_str.strip()
        b64_str += "=" * ((4 - len(b64_str) % 4) % 4)
        encrypted_bytes = base64.b64decode(b64_str)
        decrypted_bytes = bytearray()
        for i, byte in enumerate(encrypted_bytes):
            key_byte = key[i % len(key)]
            if isinstance(key_byte, int):
                decrypted_bytes.append(byte ^ key_byte)
            else:
                decrypted_bytes.append(byte ^ ord(key_byte))
        name = decrypted_bytes.decode('utf-8', errors='ignore')
        return name if name and name.strip() else "Unknown"
    except:
        return "Unknown"

def enc(d):
    """Encrypt data with AES"""
    key = b"Yg&tc%DEuh6%Zc^8"
    iv = b"6oyZDr22E3ychjM%"
    return AES.new(key, AES.MODE_CBC, iv).encrypt(pad(d, 16))

def dec(d):
    """Decrypt data with AES"""
    key = b"Yg&tc%DEuh6%Zc^8"
    iv = b"6oyZDr22E3ychjM%"
    return unpad(AES.new(key, AES.MODE_CBC, iv).decrypt(d), 16)

def build_majorlogin(tok, open_id, p_type):
    """Build MajorLogin protobuf message"""
    m = MajorLogin()
    m.event_time = str(datetime.now())[:-7]
    m.game_name = "free fire"
    m.platform_id = p_type
    m.client_version = "1.120.1"
    m.system_software = "Android OS 9 / API-28"
    m.system_hardware = "Handheld"
    m.telecom_operator = "Verizon"
    m.network_type = "WIFI"
    m.screen_width = 1920
    m.screen_height = 1080
    m.screen_dpi = "280"
    m.processor_details = "ARM64 FP ASIMD AES VMH | 2865 | 4"
    m.memory = 3003
    m.gpu_renderer = "Adreno (TM) 640"
    m.gpu_version = "OpenGL ES 3.1 v1.46"
    m.unique_device_id = "Google|34a7dcdf-a7d5-4cb6-8d7e-3b0e448a0c57"
    m.client_ip = "223.191.51.89"
    m.language = "en"
    m.open_id = open_id
    m.open_id_type = str(p_type)
    m.device_type = "Handheld"
    m.access_token = tok
    m.platform_sdk_id = 1
    m.client_using_version = "7428b253defc164018c604a1ebbfebdf"
    m.login_by = 3
    m.channel_type = 3
    m.cpu_type = 2
    m.cpu_architecture = "64"
    m.client_version_code = "2019118695"
    m.login_open_id_type = p_type
    m.origin_platform_type = str(p_type)
    m.primary_platform_type = str(p_type)
    return enc(m.SerializeToString())

def fetch_majorlogin_jwt(tok):
    """Fetch JWT from MajorLogin endpoints"""
    # Check if already JWT
    if tok.startswith("ey") and "." in tok:
        return tok, None
    
    oId = None
    
    # Try method 1: oauth/token/inspect
    try:
        r = requests.get(f"https://100067.connect.garena.com/oauth/token/inspect?token={tok}", 
                        headers={"User-Agent": "Mozilla/5.0"}, timeout=5).json()
        oId = r.get("open_id")
    except:
        pass
    
    # Try method 2: reward API
    if not oId:
        try:
            uid_headers = {"access-token": tok, "user-agent": "Mozilla/5.0"}
            uid_res = requests.get("https://prod-api.reward.ff.garena.com/redemption/api/auth/inspect_token/", 
                                   headers=uid_headers, verify=False, timeout=5).json()
            uid = uid_res.get("uid")
            if uid:
                openid_res = requests.post("https://topup.pk/api/auth/player_id_login", 
                                           headers={"Content-Type": "application/json"}, 
                                           json={"app_id": 100067, "login_id": str(uid)}, 
                                           verify=False, timeout=5).json()
                oId = openid_res.get("open_id")
        except:
            pass
    
    if not oId:
        return None, "Failed to extract Open ID"
    
    # Try multiple MajorLogin endpoints with different platform types
    platforms = [8, 3, 4, 6]
    urls = [
        "https://loginbp.ggblueshark.com/MajorLogin",
        "https://loginbp.common.ggblue.net/MajorLogin",
        "https://loginbp.ggpolarbear.com/MajorLogin",
        "https://loginbp.common.garena.com/MajorLogin"
    ]
    
    for url in urls:
        for p_type in platforms:
            pl = build_majorlogin(tok, oId, p_type)
            try:
                key = b"Yg&tc%DEuh6%Zc^8"
                iv = b"6oyZDr22E3ychjM%"
                headers = {
                    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 11; SM-S908E Build/TP1A.220624.014)",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                    "Content-Type": "application/octet-stream",
                    "X-GA": "v1 1",
                    "X-Unity-Version": "2018.4.11f1",
                    "ReleaseVersion": "OB54"
                }
                x = requests.post(url, headers=headers, data=pl, timeout=10, verify=False)
                if x.status_code == 200:
                    res = MajorLoginRes()
                    try:
                        res.ParseFromString(dec(x.content))
                    except:
                        res.ParseFromString(x.content)
                    if res.token:
                        return res.token, None
            except:
                continue
    
    return None, "MajorLogin failed"

# ========== FIXED: RESUBSCRIBE OTP SECTION ==========

def generate_username(length=12):
    """Generate random username"""
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for _ in range(length))

def send_register_code_email(email):
    """Send registration code to email via Garena"""
    url = "https://authgop.garena.com/api/send_register_code_email"
    
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
        response = requests.post(url, headers=headers, data=data, timeout=30)
        return response.status_code, response.text
    except Exception as e:
        return None, str(e)

# ========== FIXED: TELEGRAM BOT HANDLERS ==========

async def ff_ban_start(update, context):
    """Start FF Ban process"""
    await update.message.reply_text(
        "💀 𝗙𝗙 𝗣𝗘𝗥𝗠𝗔𝗡𝗘𝗡𝗧 𝗕𝗔𝗡 💀\n\n"
        "🔐 𝗘𝗻𝘁𝗲𝗿 𝗔𝗰𝗰𝗲𝘀𝘀 𝗧𝗼𝗸𝗲𝗻 / 𝗝𝗪𝗧 💎\n\n"
        "⚠️ 𝗧𝗵𝗶𝘀 𝗪𝗜𝗟𝗟 𝗣𝗘𝗥𝗠𝗔𝗡𝗘𝗡𝗧𝗟𝗬 𝗕𝗔𝗡 𝗔𝗖𝗖𝗢𝗨𝗡𝗧!",
        reply_markup=get_main_keyboard()
    )
    return FF_BAN_TOKEN

async def ff_ban_token(update, context):
    """Process FF Ban token"""
    if update.message.text in ALL_BUTTONS:
        return await switch_menu(update, context)
    
    token = update.message.text.strip()
    
    if len(token) < 20:
        await update.message.reply_text("❌ Invalid token!", reply_markup=get_main_keyboard())
        return FF_BAN_TOKEN
    
    context.user_data['ff_ban_token'] = token
    
    msg = await update.message.reply_text("🔍 Authenticating... ⏳")
    
    try:
        def authenticate():
            return fetch_majorlogin_jwt(token)
        
        jwt_token, error_msg = await asyncio.to_thread(authenticate)
        
        if not jwt_token:
            await msg.edit_text(f"❌ Authentication Failed!\n\nReason: {error_msg}")
            return ConversationHandler.END
        
        context.user_data['ff_ban_jwt'] = jwt_token
        user_data = decode_jwt(jwt_token)
        
        raw_nick = user_data.get('nickname', '')
        nickname = decode_ff_name(raw_nick)
        account_id = user_data.get('account_id', 'Unknown')
        region = user_data.get('lock_region', user_data.get('region', 'IND'))
        
        await msg.edit_text(
            f"✅ 𝗧𝗢𝗞𝗘𝗡 𝗩𝗔𝗟𝗜𝗗 ✅\n\n"
            f"👤 𝗡𝗶𝗰𝗸𝗻𝗮𝗺𝗲: {nickname}\n"
            f"🆔 𝗔𝗖𝗖𝗼𝘂𝗻𝘁 𝗜𝗗: {account_id}\n"
            f"🌍 𝗥𝗲𝗴𝗶𝗼𝗻: {region}\n\n"
            f"⚠️ 𝗦𝗨𝗥𝗘 𝗬𝗢𝗨 𝗪𝗔𝗡𝗧 𝗧𝗢 𝗕𝗔𝗡?",
            reply_markup=get_ban_confirm_keyboard()
        )
        
        return FF_BAN_CONFIRM
        
    except Exception as e:
        await msg.edit_text(f"❌ Error: {str(e)[:100]}")
        return ConversationHandler.END

async def ff_ban_confirm(update, context):
    """Confirm FF Ban"""
    text = update.message.text.strip()
    
    if text in ALL_BUTTONS:
        return await switch_menu(update, context)
    
    if text in ["❌ No, Cancel 🚫", "No", "❌ No"]:
        await update.message.reply_text(
            "❌ 𝗕𝗔𝗡 𝗔𝗡𝗦𝗖𝗥𝗘𝗪𝗦𝗟𝗬 𝗖𝗔𝗡𝗖𝗘𝗟𝗟𝗘𝗗! ✅",
            reply_markup=get_main_keyboard()
        )
        return ConversationHandler.END
    
    if text not in ["✅ Yes, Ban Karo 💀", "Yes", "✅ Yes"]:
        await update.message.reply_text(
            "⚠️ 𝗣𝗹𝗲𝗮𝘀𝗲 𝗖𝗵𝗼𝗼𝘀𝗲:\n"
            "✅ Yes, Ban Karo 💀\n"
            "❌ No, Cancel 🚫",
            reply_markup=get_ban_confirm_keyboard()
        )
        return FF_BAN_CONFIRM
    
    jwt_token = context.user_data.get('ff_ban_jwt')
    if not jwt_token:
        await update.message.reply_text("❌ Token lost! Try again", reply_markup=get_main_keyboard())
        return ConversationHandler.END
    
    msg = await update.message.reply_text("💀 𝗜𝗡𝗝𝗘𝗖𝗧𝗜𝗡𝗚 𝗕𝗔𝗡 𝗣𝗔𝗬𝗟𝗢𝗔𝗗... ⚡")
    
    try:
        def inject():
            return trigger_injection(jwt_token, "Latest")
        
        ban_resp = await asyncio.to_thread(inject)
        
        if ban_resp.status_code == 200:
            user_data = decode_jwt(jwt_token)
            nickname = decode_ff_name(user_data.get('nickname', ''))
            account_id = user_data.get('account_id', 'Unknown')
            
            await msg.edit_text(
                f"🎯 𝗕𝗔𝗡𝗡𝗘𝗗 𝗦𝗨𝗖𝗖𝗘𝗦𝗦𝗙𝗨𝗟𝗟𝗬! 💀🔥\n\n"
                f"👤 𝗔𝗰𝗰𝗼𝘂𝗻𝘁: {nickname}\n"
                f"🆔 𝗨𝗜𝗗: {account_id}\n\n"
                f"💀 𝗦𝘁𝗮𝘁𝘂𝘀: 𝟭𝟬𝟬% 𝗣𝗘𝗥𝗠𝗔𝗡𝗘𝗡𝗧𝗟𝗬 𝗕𝗔𝗡𝗡𝗘𝗗 💀\n\n"
                f"👑 @just_zevric Premium",
                reply_markup=get_main_keyboard()
            )
        else:
            await msg.edit_text(
                f"❌ 𝗕𝗔𝗡 𝗙𝗔𝗜𝗟𝗘𝗗!\n\n"
                f"HTTP Status: {ban_resp.status_code}\n"
                f"💡 Token might be expired or server error",
                reply_markup=get_main_keyboard()
            )
    
    except Exception as e:
        await msg.edit_text(f"❌ Error: {str(e)[:100]}", reply_markup=get_main_keyboard())
    
    return ConversationHandler.END

async def resubscribe_start(update, context):
    """Start Resubscribe OTP"""
    await update.message.reply_text(
        "📧 𝗥𝗘𝗦𝗨𝗕𝗦𝗖𝗥𝗜𝗕𝗘 𝗢𝗧𝗣 𝗦𝗘𝗡𝗗𝗘𝗥 📧\n\n"
        "✉️ 𝗘𝗻𝘁𝗲𝗿 𝗬𝗼𝘂𝗿 𝗘𝗺𝗮𝗶𝗹 𝗔𝗱𝗱𝗿𝗲𝘀𝘀 💎",
        reply_markup=get_main_keyboard()
    )
    return RESUB_EMAIL

async def resubscribe_email(update, context):
    """Process Resubscribe email"""
    if update.message.text in ALL_BUTTONS:
        return await switch_menu(update, context)
    
    email = update.message.text.strip()
    
    # Validate email
    if "@" not in email or "." not in email or len(email) < 5:
        await update.message.reply_text(
            "❌ Invalid email format!\n\n"
            "📧 Example: user@gmail.com",
            reply_markup=get_main_keyboard()
        )
        return RESUB_EMAIL
    
    msg = await update.message.reply_text(f"📧 𝗦𝗲𝗻𝗱𝗶𝗻𝗴 𝗢𝗧𝗣 𝗧𝗼 {email}... ⏳")
    
    try:
        def send_otp():
            return send_register_code_email(email)
        
        status_code, response = await asyncio.to_thread(send_otp)
        
        if status_code == 200:
            try:
                result = json.loads(response)
                if result.get("result") == 0:
                    await msg.edit_text(
                        f"✅ 𝗢𝗧𝗣 𝗦𝗘𝗡𝗧 𝗦𝗨𝗖𝗖𝗘𝗦𝗦𝗙𝗨𝗟𝗟𝗬! 🎉\n\n"
                        f"📧 𝗘𝗺𝗮𝗶𝗹: {email}\n"
                        f"📩 𝗖𝗵𝗲𝗰𝗸 𝗬𝗼𝘂𝗿 𝗜𝗻𝗯𝗼𝘅!\n\n"
                        f"⏱️ 𝗢𝗧𝗣 𝗘𝘅𝗽𝗶𝗿𝗲𝘀 𝗜𝗻: 𝟭𝟬 𝗠𝗶𝗻𝘂𝘁𝗲𝘀\n\n"
                        f"👑 @just_zevric",
                        reply_markup=get_main_keyboard()
                    )
                else:
                    await msg.edit_text(
                        f"❌ 𝗙𝗮𝗶𝗹𝗲𝗱 𝘁𝗼 𝗦𝗲𝗻𝗱 𝗢𝗧𝗣!\n\n"
                        f"💡 {result.get('message', 'Unknown error')}\n\n"
                        f"🔄 𝗧𝗿𝘆 𝗔𝗻𝗼𝘁𝗵𝗲𝗿 𝗘𝗺𝗮𝗶𝗹",
                        reply_markup=get_main_keyboard()
                    )
            except:
                await msg.edit_text(
                    f"✅ 𝗢𝗧𝗣 𝗦𝗘𝗡𝗧! 📧\n\n"
                    f"📧 Email: {email}\n"
                    f"📩 Check inbox and spam folder!",
                    reply_markup=get_main_keyboard()
                )
        else:
            await msg.edit_text(
                f"❌ 𝗦𝗲𝗿𝘃𝗲𝗿 𝗘𝗿𝗿𝗼𝗿!\n\n"
                f"HTTP Status: {status_code}\n"
                f"💡 Try again later",
                reply_markup=get_main_keyboard()
            )
    
    except Exception as e:
        await msg.edit_text(
            f"❌ Error: {str(e)[:100]}\n\n"
            f"🔄 Try again!",
            reply_markup=get_main_keyboard()
        )
    
    return ConversationHandler.END

# ========== ADD HANDLERS TO CONVERSATION ==========
# Add these to your main ConversationHandler:

conv_handler = ConversationHandler(
    entry_points=[
        MessageHandler(filters.Regex(P_FF_BAN), ff_ban_start),
        MessageHandler(filters.Regex(P_RESUB), resubscribe_start),
        # ... other entry points
    ],
    states={
        FF_BAN_TOKEN: [MessageHandler(filters.TEXT & ~filters.COMMAND, ff_ban_token)],
        FF_BAN_CONFIRM: [MessageHandler(filters.TEXT & ~filters.COMMAND, ff_ban_confirm)],
        RESUB_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, resubscribe_email)],
        # ... other states
    },
    fallbacks=[CommandHandler('start', start)],
)
