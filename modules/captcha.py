import time
import requests
import json

def solve_captcha():
    with open('./data/config.json') as json_file:
        data = json.load(json_file)
    proxydata = data['proxy'].split(':')
    data = {
        "clientKey": data['captcha_api_key'],
        "task": {
            "type": "NoCaptchaTask",
            "websiteURL": "https://ogu.gg/member.php",
            "websiteKey": "6LdiB7EfAAAAAINZVemfmxPWdbybsmCHC7yvMGPE",
            "proxyType": "http",
            "proxyAddress": proxydata[2],
            "proxyPort": proxydata[3],
            "proxyLogin": proxydata[0],
            "proxyPassword": proxydata[1],
            "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.132 Safari/537.36"
        }
    }
    resp = requests.get(url='https://api.capmonster.cloud/createTask', json=data)
    respdict = json.loads(resp.text)
    taskid = (respdict['taskId'])
    time.sleep(5)
    while True:
        with open('./data/config.json') as json_file:
            data = json.load(json_file)
        time.sleep(0.5)
        data = {
            "clientKey": data['captcha_api_key'],
            "taskId": taskid
        }

        resp = requests.get(url='https://api.capmonster.cloud/getTaskResult', json=data)
        respdict = json.loads(resp.text)
        if (respdict['status']) == 'processing':
            continue
        if (respdict['status']) == 'ready':
            break
    sol = (respdict['solution'])
    g_sol = (sol['gRecaptchaResponse'])
    return g_sol
