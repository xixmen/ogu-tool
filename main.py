import time
import threading
import json
import os
from termcolor import colored
from modules.info import geninfo
from modules.captcha import solve_captcha
from modules.generator import gen
from modules.likebot import likebot
from modules.massdm import massdm
from modules.threadspam import threadspam
from modules.checker import accountchecker


def auto_gen():
    print(colored('[*] Worker Started', 'magenta'))
    while True:
        starttime = time.time()
        info = geninfo()
        captcha = solve_captcha()
        g = gen(info, captcha)
        if g[0].status_code == 200:
            executiontime = time.time() - starttime
            account = [info[0], info[1], g[1], g[2]]
            accs = open("./data/accounts.txt", "a")
            accs.write(f'{account[0]}:{account[1]}:{account[2]}:{account[3]}\n')
            accs.close()
            print(colored(f'[+] Account Generated In {round(executiontime)} Seconds', 'green'))
            continue
        else:
            print('unk error')
            continue


def auto_like(i, num_of_threads, username, pid):
    likebot(username, pid, i, num_of_threads)
    # menu() Annoying
1

def menu():
    print('''
    --------------------------------------------------
    |                                                |
    |   1. Generate Accounts                         |
    |   2. Bot Post's Likes                          |
    |   3. Bot User's Messages                       |
    |   4. Bot Thread Replys                         |
    |   5. Check Accounts                            |
    |                                                |
    --------------------------------------------------
    ''')
    choice = input('[*] Enter your choice: ')
    if choice == '1':
        with open('./data/config.json') as json_file:
            data = json.load(json_file)
        num_of_threads = int(data['threads'])
        if num_of_threads > 2:
            print(colored('[*] Using over 2 threads is not recommended because ogu is hosted on a smart fridge', 'magenta'))
        threads = []
        for i in range(1, num_of_threads + 1):
            time.sleep(0.025)
            th = threading.Thread(target=auto_gen)
            threads.append(th)
            th.start()

    elif choice == '2':
        username = input('[*] Enter username of poster: ')
        message = input('[*] Enter post id: ')
        with open('./data/config.json') as json_file:
            data = json.load(json_file)
        num_of_threads = int(data['threads'])
        threads = []
        for i in range(1, num_of_threads + 1):
            time.sleep(0.025)
            th = threading.Thread(target=auto_like, args=(i, num_of_threads, username, message))
            threads.append(th)
            th.start()
    elif choice == '3':
        username = input('[*] Enter user to spam: ')
        message = input('[*] Enter spam message: ')
        with open('./data/config.json') as json_file:
            data = json.load(json_file)
        num_of_threads = int(data['threads'])
        threads = []
        for i in range(1, num_of_threads + 1):
            time.sleep(0.025)
            th = threading.Thread(target=massdm, args=(username, message, i, num_of_threads))
            threads.append(th)
            th.start()
    elif choice == '4':
        tid = input('[*] Enter thread id: ')
        message = input('[*] Enter reply message: ')
        with open('./data/config.json') as json_file:
            data = json.load(json_file)
        num_of_threads = int(data['threads'])
        threads = []
        for i in range(1, num_of_threads + 1):
            time.sleep(0.025)
            th = threading.Thread(target=threadspam, args=(tid, message, i, num_of_threads))
            threads.append(th)
            th.start()
    elif choice == '5':
        with open('./data/config.json') as json_file:
            data = json.load(json_file)
        num_of_threads = int(data['threads'])
        threads = []
        for i in range(1, num_of_threads + 1):
            time.sleep(0.025)
            th = threading.Thread(target=accountchecker, args=(i, num_of_threads))
            threads.append(th)
            th.start()

    else:
        print('[-] Wrong choice')
        menu()


if __name__ == '__main__':
    menu()
