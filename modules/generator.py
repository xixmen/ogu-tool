import cloudscraper
import json
import re
import time
from termcolor import colored


def gen(info, captcha):
    with open('./data/config.json') as json_file:
        data = json.load(json_file)
    proxydata = data['proxy'].split(':')
    proxies = {
        'https': f'http://{proxydata[0]}:{proxydata[1]}@{proxydata[2]}:{proxydata[3]}',
        'http': f'http://{proxydata[0]}:{proxydata[1]}@{proxydata[2]}:{proxydata[3]}',
    }

    requester = cloudscraper.create_scraper(browser={'browser': 'firefox', 'platform': 'windows', 'mobile': False})
    while True:
        try:
            data = {
                'allownotices': '1',
                'receivepms': '1',
                'pmnotice': '1',
                'regcheck1': '',
                'regcheck2': 'true',
                'username': info[0],
                'password': info[1],
                'email': info[2],
                'g-recaptcha-response': captcha,
                'regtime': '1658090891',
                'step': 'registration',
                'action': 'do_register',
                'regsubmit': 'Submit Registration',
            }
            resp = requester.post('https://ogu.gg/member.php', data=data, proxies=proxies)
            if resp.status_code == 200:
                ogubb = requester.cookies.get_dict()
                ogumybbuser = (ogubb['ogumybbuser'])
                finder = re.findall(r'var my_post_key = .*;', resp.text)
                postkey = (finder[0].replace('var my_post_key = ', '').replace('"', '').replace(';', '').strip())
                return [resp, ogumybbuser, postkey]
            if resp.status_code == 503:
                # Ogu likes to shit itself
                # print(colored('[!] Ogu Error | Sleeping', 'red'))
                time.sleep(1)
                continue
            if 'This IP address is banned.' in resp.text:
                print(colored('[!] IP Banned ', 'red'))
                continue
            else:
                print(colored('[!] Blocked By CloudFlare | Sleeping', 'red'))
                time.sleep(10)
                continue
        except Exception as n:
            print(colored('[!] Proxy Error', 'red'))
            continue
