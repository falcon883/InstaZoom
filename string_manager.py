from colorama import init, Fore, Style
import shutil

class string_manager(object):
    def __init__(self):
        init()
        self.info = '''\n Enter comma seperated usernames for multiple entries, like user1,user2. 
                    \n Keep the input empty and press Enter to exit the script. \n\n'''

    def print_start_screen(self):
	    print(Fore.LIGHTRED_EX + self.bordered(self.info))

    def set_print_color(self, color):
        print(color)
    
    def reset_print_color(self):
        Style.RESET_ALL

    def username_tree(self, username):
        self.set_print_color(Fore.GREEN)
        self.consoleSize()
        print(f"\n Username: {username}")
        print("  │")
        print("  │─ Downloading Image")

    def image_creation(self, task_done):
        if task_done:
            print("  │")
            print("  │─ Download Complete\n ")
            self.consoleSize()
            self.reset_print_color()
        else:
            print("  │")
            print("  │─ Creating Image File")

    def print_download_error(self):
        self.set_print_color(Fore.LIGHTRED_EX)
        print("Error Downloading Image File")
        self.reset_print_color()

    def print_acc_not_found(self, username):
        self.set_print_color(Fore.LIGHTRED_EX)
        self.consoleSize()
        print(f"\n Username: {username}")
        print("  │")
        print("  │─ Account Not Found\n ")
        self.consoleSize()
        self.reset_print_color()

    def bordered(self, text):
        lines = text.splitlines()
        width = max(len(s) for s in lines)
        res = ['┌' + '─' * width + '┐']
        for s in lines:
            res.append('│' + (s + ' ' * width)[:width] + '│')
        res.append('└' + '─' * width + '┘')
        return '\n'.join(res)

    def consoleSize(self):
	    for _ in range(shutil.get_terminal_size((80,20))[0]):
		    print("─",end="")