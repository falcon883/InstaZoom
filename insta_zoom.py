from colorama import Fore
from string_manager import string_manager
from bs4 import BeautifulSoup as bs
import re
import requests
import random
import shutil
import signal

class insta_zoom(object):
    def __init__(self):
        signal.signal(signal.SIGINT, self.signal_handler)
        self.stm = string_manager()
        self.insta_url = "https://www.instagram.com/{}"
        self.usernameList = []
        
        if self.is_connected():
            self.stm.print_start_screen()
            self.stm.set_print_color(Fore.RED)
            self.username = ""
            while self.username.strip() == "": 
                self.username = input("Enter Your Instagram Username: ")
            self.stm.reset_print_color()
            for user in self.username.split(","):
	            self.usernameList.append(user.replace(" ", ""))
            self.usernameList = list(dict.fromkeys(self.usernameList))
            self.usernameList = [i for i in self.usernameList if i] 
            self.get_img(self.usernameList)

    def signal_handler(self, sig, frame):
        exit()

    def is_connected(self):
        url='https://www.google.com/'
        timeout=5
        try:
            _ = requests.get(url, timeout=timeout)
            return True
        except requests.ConnectionError:
            self.stm.set_print_color(Fore.LIGHTRED_EX)
            print("No Internet Connection.")
            self.stm.reset_print_color()
        return False

    def get_img(self, list):
        with requests.Session() as r:
            for user in self.usernameList:
                insta_url = self.insta_url.format(user)
                print(insta_url)
                req = r.get(insta_url)
                
                if req.status_code == 200:
                    b = bs(req.content, 'html5lib')
                    image_url = b.find("script", text = re.compile(r'"profile_pic_url_hd":(.+?)"'))
                    image_url = re.search(r'"profile_pic_url_hd":(.+?)"', image_url.text)
                    if image_url != None:
                        img = image_url.group().split(':',1)[1][1:-1].replace("\\u0026","&")
                        self.stm.username_tree(user)
                        img = r.get(img, stream=True)
                        img.raw.decode_content = True
                        with open(f"image_{str(random.randint(1,100000))}.jpg", "wb+") as f:
                            self.stm.image_creation(False)
                            shutil.copyfileobj(img.raw, f)
                            del img
                            f.close()
                            self.stm.image_creation(True)
                elif req.status_code == 404:
                    self.stm.print_acc_not_found(user)
                else:
                    self.stm.set_print_color(Fore.LIGHTRED_EX)
        self.stm.reset_print_color()

insta_zoom()