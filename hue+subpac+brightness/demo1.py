# Changing Brightness with target

from phue import Bridge
import time
import sys
import oscilliate_lights as osc
import reset_lights as reset


bridge_ip = '192.168.1.2'
b = Bridge(bridge_ip)
lights = b.get_light_objects()
reset.reset(lights, [255, 255, 255], 255)
up = True
delay_mode = 'BREATHING'

osc.OPTIONS = {
'r': 255,
'g': 255,
'b': 255,
'dr': 0,
'dg': 0,
'db': 0,
'ddr': 0,
'ddg': 0,
'ddb': 0,
'brightness': 215,
'dbrightness': 15,
'ddbrightness': -5
}

osc.TARGET = {
'r': 255,
'g': 255,
'b': 255,
'brightness': 150,
'enabled': True,
'reached': False
}

osc.MODE = osc.MODES['BRIGHTNESS']
while True:
    if up:
        sys.stdout.write('↑ ')
    else:
        sys.stdout.write('↓ ')
    sys.stdout.flush()
    for light in lights:
        osc.oscilliate(light, up)
        # print(light.xy)
        # print(light.brightness)
    up = not up
    if up: #after up, up is not up and DOWN_DELAY is needed
        time.sleep(osc.DELAYS[delay_mode][osc.UP])
    else:
        time.sleep(osc.DELAYS[delay_mode][osc.DOWN])
        osc.updateOptions()
