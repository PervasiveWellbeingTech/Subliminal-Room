# Changing Hue colors with target
import libs
from phue import Bridge, Group
import time
import sys
import oscilliate_group as osc
import reset


bridge_ip = '192.168.1.2'
b = Bridge(bridge_ip)
g = Group(b, 1)
up = True
delay_mode = 'FAST'

osc.OPTIONS = {
'r': 255,
'g': 255,
'b': 255,
'dr': 0,
'dg': 0,
'db': 0,
'ddr': 0,
'ddg': -5,
'ddb': -6,
'brightness': 255,
'dbrightness': 0,
'ddbrightness': 0
}

osc.TARGET = {
'r': 255,
'g': 200,
'b': 104,
'brightness': 255,
'enabled': True,
'reached': False
}

osc.MODE = osc.MODES['COLOR']

reset.reset_group(g, osc.OPTIONS)
# exit()

while not osc.TARGET['reached']:
    if up:
        sys.stdout.write('↑ ')
    else:
        sys.stdout.write('↓ ')
    sys.stdout.flush()
    osc.oscilliate(g, up)
    up = not up
    if up: #after up, up is not up and DOWN_DELAY is needed
        time.sleep(osc.DELAYS[delay_mode][osc.UP])
    else:
        time.sleep(osc.DELAYS[delay_mode][osc.DOWN])
        osc.updateOptions()
