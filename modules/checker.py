import cloudscraper
import json
import linecache
import time
from termcolor import colored


def accountchecker(threadnum, num_of_threads):
    print(colored('[*] Worker Started', 'magenta'))
    threadnum += 1
    time.sleep(2)
    with open('./data/config.json') as json_file:
        data = json.load(json_file)
    proxydata = data['proxy'].split(':')
    proxies = {
        'https': f'http://{proxydata[0]}:{proxydata[1]}@{proxydata[2]}:{proxydata[3]}',
        'http': f'http://{proxydata[0]}:{proxydata[1]}@{proxydata[2]}:{proxydata[3]}',
    }
    while True:
        account = linecache.getline('./data/accounts.txt', threadnum)
        try:
            x = account.split(":")
            name = x[0]
        except Exception as n:
            print(colored('[!] Worker Ran Out Of Accounts', 'red'))
            break
        requester = cloudscraper.create_scraper(browser={'browser': 'firefox', 'platform': 'windows', 'mobile': False})
        try:
            resp = requester.get(f'https://ogu.gg/{name}', proxies=proxies)
        except Exception as n:
            print(colored('[-] Proxy Error', 'red'))
            continue
        if name =='':
            break
        if 'banned' in resp.text:
            print(colored(f'[!] Account {name} Banned', 'red'))
            threadnum += num_of_threads
            continue
        else:
            print(colored(f'[+] Account {name} Works', 'green'))
            threadnum += num_of_threads
            continue
