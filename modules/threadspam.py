import random, cloudscraper, linecache, time, json
from termcolor import colored


# all the threadnum and num_of_threads shit is just to make sure that the threads arent overlapping
def threadspam(tid, message, threadnum, num_of_threads):
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
        data = {
            'my_post_key': postkey.rstrip(),
            'subject': message,
            'action': 'do_newreply',
            'posthash': 'b90e401e79720126e76f54c3916c7d93',
            'quoted_ids': '',
            'lastpid': 0,
            'from_page': '1',
            'tid': tid.rstrip(),
            'method': 'quickreply',
            'message': message,
        }
        cookies = {
            'ogumybbuser': ogumybbuser,
        }
        try:
            resp = requester.post(url=f'https://ogu.gg/newreply.php',cookies=cookies, proxies=proxies, data=data)
        except Exception as n:
            print(colored('[-] Proxy Error', 'red'))
            continue
        if 'The message is too short.' in resp.text:
            print(colored('[!] Message Too Short', 'red'))
            break
        if resp.status_code == 200:
            threadnum += num_of_threads
            print(colored('[+] Reply Sent', 'green'))
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
