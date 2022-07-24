import cloudscraper
import json
import time
import linecache
from termcolor import colored

global threadnum


# all the threadnum and num_of_threads shit is just to make sure that the threads arent overlapping
def likebot(username, pid, threadnum, num_of_threads):
    print(colored('[*] Worker Started', 'magenta'))
    threadnum += 1
    time.sleep(2)
    requester = cloudscraper.create_scraper(browser={'browser': 'firefox', 'platform': 'windows', 'mobile': False})
    with open('./data/config.json') as json_file:
        data = json.load(json_file)
    proxydata = data['proxy'].split(':')
    proxies = {
        'https': f'http://{proxydata[0]}:{proxydata[1]}@{proxydata[2]}:{proxydata[3]}',
        'http': f'http://{proxydata[0]}:{proxydata[1]}@{proxydata[2]}:{proxydata[3]}',
    }
    while True:
        account = linecache.getline('./data/accounts.txt', threadnum)
        x = account.split(":")
        try:
            ogumybbuser = (x[2])
        except Exception as n:
            print(colored('[!] Worker Ran Out Of Accounts', 'red'))
            break
        postkey = (x[3])
        cookies = {
            'ogumybbuser': ogumybbuser.rstrip(),
        }
        try:
            resp = requester.post(url=f'https://ogu.gg/thankyoulike.php?{username.rstrip()}=1&action=add&pid={pid.rstrip()}&my_post_key={postkey.rstrip()}',cookies=cookies, proxies=proxies)
        except Exception as n:
            print(colored('[-] Proxy Error', 'red'))
            continue
        if resp.status_code == 200:
            threadnum += num_of_threads
            print(colored('[+] Liked', 'green'))
            continue
        if resp.status_code == 404:
            print(colored('[!] Already Liked', 'grey'))
            threadnum += num_of_threads
            continue
        if resp.status_code == 403:
            # lmao even if cloudflare blocks it will still like the post
            threadnum += num_of_threads
            print(colored('[+] Liked', 'green'))
            continue

        else:
            print(colored('[!] Unknown Error', 'magenta'))
