import requests
import time
# import json

BASE_URL = 'https://rest.moodo.co/api'
AUTH_HEADER = None
DEVICE_KEY = None
STATE = {
    'device_key': None,
    'fan_volume': 0,
    'box_status': 0,
    'settings_slot0': {
    'fan_speed': 0,
    'fan_active': False
    },
    'settings_slot1': {
    'fan_speed': 0,
    'fan_active': False
    },
    'settings_slot2': {
    'fan_speed': 0,
    'fan_active': False
    },
    'settings_slot3': {
    'fan_speed': 0,
    'fan_active': False
    }}
# ON is 1, max speed is 100
def login(email, password):
    payload = {'email': email, 'password':password}
    r = requests.post(BASE_URL+'/login', json=payload)
    # print(r)
    token = r.json()['token']
    # print(r.json())
    if token:
        global AUTH_HEADER
        AUTH_HEADER = {'token': str(token)}
        return True
    else:
        return False

def update_state():
    cur = get_state()

def get_devices(name):
    global DEVICE_KEY
    r = requests.get(BASE_URL+'/boxes', headers=AUTH_HEADER)
    if name == None:
        DEVICE_KEY = r.json()['boxes'][0]['device_key']
        return True
    else:
        for box in r.json()['boxes']:
            if box['name'] == name:
                DEVICE_KEY = box['device_key']
                return True
        return False

def init(email, password, name=None):
    success = login(email, password)
    if not success:
        print('Error, could not log in.')
        return
    success = get_devices(name)
    if not success:
        print('Error, could not get devices.')
        return
    reset()
    print('Connected and resetted moodo device.')

def reset():
    change_state(fan_volume=0, box_status=1, fan_speeds=[0,0,0,0], fan_states=[False,False,False,False])

def power_off():
    r = requests.delete(BASE_URL+'/boxes/'+str(DEVICE_KEY), headers=AUTH_HEADER)

def get_state():
    r = requests.get(BASE_URL+'/boxes/'+str(DEVICE_KEY), headers=AUTH_HEADER)
    return r.json()

def change_state(fan_volume=None, box_status=None, fan_speeds=[None,None,None,None], fan_states=[None,None,None,None]):
    global STATE
    payload = {
    'device_key': DEVICE_KEY,
    'fan_volume': fan_volume if fan_volume is not None else STATE['fan_volume'],
    'box_status': box_status if box_status is not None else STATE['box_status'],
    'settings_slot0': {
    'fan_speed': fan_speeds[0] if fan_speeds[0] is not None else STATE['settings_slot0']['fan_speed'],
    'fan_active': fan_states[0] if fan_states[0] is not None else STATE['settings_slot0']['fan_active']
    },
    'settings_slot1': {
    'fan_speed': fan_speeds[1] if fan_speeds[1] is not None else STATE['settings_slot1']['fan_speed'],
    'fan_active': fan_states[1] if fan_states[1] is not None else STATE['settings_slot1']['fan_active']
    },
    'settings_slot2': {
    'fan_speed': fan_speeds[2] if fan_speeds[2] is not None else STATE['settings_slot2']['fan_speed'],
    'fan_active': fan_states[2] if fan_states[2] is not None else STATE['settings_slot2']['fan_active']
    },
    'settings_slot3': {
    'fan_speed': fan_speeds[3] if fan_speeds[3] is not None else STATE['settings_slot3']['fan_speed'],
    'fan_active': fan_states[3] if fan_states[3] is not None else STATE['settings_slot3']['fan_active']
    }}
    # print(json.dumps(payload))
    # print(payload)
    r = requests.post(BASE_URL+'/boxes', json=payload, headers=AUTH_HEADER)
    # print(r.json())
    STATE = payload

def test():
    init('kdonbekci@gmail.com', 'Donbek2003')
    change_state(fan_volume=80, box_status=1, fan_speeds=[0,0,0,0], fan_states=[True,False,False,False])
    print(get_state())
    time.sleep(3)
    change_state(fan_volume=80, box_status=1, fan_speeds=[0,0,0,0], fan_states=[False,True,False,False])
    time.sleep(3)
    change_state(fan_volume=80, box_status=1, fan_speeds=[0,0,0,0], fan_states=[False,False,True,False])
    time.sleep(3)
    change_state(fan_volume=80, box_status=1, fan_speeds=[0,0,0,0], fan_states=[False,False,False,True])
    print('a')
    # change_state(fan_speeds=[100,0,100,0], fan_states=[True,False,True,False])
    # time.sleep(5)
    print('b')
    # change_state(fan_speeds=[50,0,50,0], fan_states=[True,False,True,False])

# test()
