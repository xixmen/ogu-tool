from faker import Faker
import random
import json

def geninfo():
    with open('./data/config.json') as json_file:
        data = json.load(json_file)
    if data['custom_names'] == 'true':
        lines = open('./data/names.txt').readlines()
        line = random.choice(lines)
        name = line.rstrip()
    if data['custom_names'] == 'false':
        name = random.randint(000000, 999999)
    fake = Faker(['en_CA'])
    password = fake.password()
    email = f'{random.randint(100000000, 999999999)}@gmail.com'
    info = [name, password, email]
    return info

