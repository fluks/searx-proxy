#!/usr/bin/env python3

from flask import Flask, redirect
from json import loads as json_loads
from urllib.request import urlopen
from urllib.parse import urlparse
from random import choices
import datetime

app = Flask(__name__)
instances_json = 'instances.json'
instance_load_time = datetime.datetime.now()
json = None

def only_http_instances(x):
    ''' '''
    u = urlparse(x['url'])[1].split('.')
    return u[-1] != 'onion' and u[-1] != 'i2p'

def dict_to_list(key, instances):
    d = instances[key]
    d['url'] = key
    return d

def has_timing(x):
    ''' '''
    return ('timing' in x and
        'search' in x['timing'] and
        'load' in x['timing']['search'] and
        'mean' in x['timing']['search']['load'])

def choose_instance(json):
    ''' '''
    instances = json['instances']
    instances = list(map(lambda k: dict_to_list(k, instances), instances.keys()))
    instances = list(filter(only_http_instances, instances))
    instances = list(filter(lambda x: x['http']['status_code'] == 200, instances))
    instances = list(filter(has_timing, instances))
    instances = sorted(instances, key=lambda i: i['timing']['search']['load']['mean'], reverse=True)
    weights = list(map(lambda x: x / len(instances), range(1, len(instances) + 1)))
    i = choices(instances, cum_weights=weights)[0]

    return i['url']

def fetch_instance_data():
    ''' '''
    instances_url = 'https://searx.space/data/instances.json'
    with urlopen(instances_url) as r:
        res = r.read().decode()
        with open(instances_json, 'w') as f:
            f.write(res)
        return json_loads(res)

@app.route('/', methods=['POST'])
def searx_proxy():
    ''' '''
    url = ''
    
    global instance_load_time, json, instances_json
    if datetime.datetime.now() - instance_load_time > datetime.timedelta(days=1):
        json = fetch_instance_data()
        instance_load_time = datetime.datetime.now()

    if not json:
        try:
            with open(instances_json, 'r') as f:
                json = json_loads(f.read())
        except FileNotFoundError:
            json = fetch_instance_data()
            instance_load_time = datetime.datetime.now()

    url = choose_instance(json)

    return redirect(url, code=307)
