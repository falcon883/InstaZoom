from bs4 import BeautifulSoup
from colorama import init
from colorama import Fore, Style
import requests
import re
import random
import os.path
import shutil
import signal
import sys

init()

def consoleSize():
	for i in range(shutil.get_terminal_size((80,20))[0]):
		print("─",end="")
		
def signal_handler(sig, frame):
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

def check_internet():
    url='https://www.google.com/'
    timeout=5
    try:
        _ = requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        print("No Internet Connection.")
    return False

def bordered(text):
    lines = text.splitlines()
    width = max(len(s) for s in lines)
    res = ['┌' + '─' * width + '┐']
    for s in lines:
        res.append('│' + (s + ' ' * width)[:width] + '│')
    res.append('└' + '─' * width + '┘')
    return '\n'.join(res)

if check_internet():

	info = '\n Enter comma seperated usernames for multiple entries, like user1,user2. \n Keep the input empty and press Enter to exit the script.\n ' 
	print(Fore.LIGHTRED_EX + bordered(info))

	insta_url = "https://www.instagram.com/{}"
	usernameList = []
	print(Fore.RED)
	username = input("Enter Your Instagram Username: ")
	print(Style.RESET_ALL)

	if username == "":
		exit()

	for user in username.split(","):
	    usernameList.append(user)
	usernameList = list(dict.fromkeys(usernameList))
	usernameList = [i for i in usernameList if i] 

	while usernameList:

		url = insta_url.format(usernameList[0])
		result = requests.get(url)

		if result.status_code == 200:

			soup = BeautifulSoup(result.content,"html.parser")

			for script in soup.findAll("script"):

				text = "".join(script.findAll(text=True))
				image_url = re.search(r'"profile_pic_url_hd":(.+?)"',text)

				if image_url != None:
					img = image_url.group()
					img = img.split(':',1)
					img = img[1]
					img = img[1:-1]
					img = img.replace("\\u0026","&")
					
					print(Fore.GREEN)
					consoleSize()
					print("\n Username: " + usernameList[0])
					print("  │")
					print("  │─ Downloading Image")

			while True:
				filename = "image_" + str(random.randint(1,100000)) + ".jpg"
				file_exists = os.path.isfile(filename)

				if not file_exists:

					print("  │")
					print("  │─ Creating Image File")

					resp = requests.get(img, stream=True)
					local_file = open(filename, 'wb+')
					resp.raw.decode_content = True
					shutil.copyfileobj(resp.raw,local_file)
					del resp

					print("  │")
					print("  │─ Download Complete\n ")
					consoleSize()
					print(Style.RESET_ALL)
					usernameList.pop(0)
					break

				else:
					print(Fore.LIGHTRED_EX + "Error Downloading Image File" + Style.RESET_ALL)
					break

		elif result.status_code == 404:
			print(Fore.LIGHTRED_EX)
			consoleSize()
			print("\n Username: " + usernameList[0])
			print("  │")
			print("  │─ Account Not Found\n ")
			consoleSize()
			print(Style.RESET_ALL)
			usernameList.pop(0)
			continue

print(Style.RESET_ALL)
