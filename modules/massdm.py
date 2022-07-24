import random, cloudscraper, linecache, time, json
from termcolor import colored


# all the threadnum and num_of_threads shit is just to make sure that the threads arent overlapping
def massdm(username, message, threadnum, num_of_threads):
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
        data = {
            'my_post_key': postkey.rstrip(),
            'action': 'do_send',
            'to': username,
            'message': f'{message}',
        }
        cookies = {
            'ogumybbuser': ogumybbuser,
        }
        try:
            resp = requester.post(url=f'https://ogu.gg/private.php',cookies=cookies,data=data, proxies=proxies)
        except Exception as n:
            print(colored('[-] Proxy Error', 'red'))
            continue
        if resp.status_code == 200:
            threadnum += num_of_threads
            print(colored('[+] Message Sent', 'green'))
            continue
        if resp.status_code == 404:
            print(colored('[!] Account Error', 'red'))
            threadnum += num_of_threads
            continue
        if resp.status_code == 403:
            #threadnum += num_of_threads
            print(colored('[!] Cloudflare Error | Sleeping', 'red'))
            time.sleep(10)
            continue

        else:
            print(colored('[!] Unknown Error', 'magenta'))
