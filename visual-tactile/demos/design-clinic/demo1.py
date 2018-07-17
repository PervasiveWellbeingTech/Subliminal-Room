# Changing Hue Brightness with target
import libs
import sys
from phue import Bridge
import time
import oscilliate_lights as osc
import reset_lights as reset
# from tkinter import *
# from tkinter import messagebox
#
# messagebox.showwarning("Say Hello", "Hello World")
# bridge_ip = '192.168.1.2'
bridge_ip = "128.12.141.85"

b = Bridge(bridge_ip)
lights = b.get_light_objects()
up = True
delay_mode = 'BREATHING'

osc.OPTIONS = {
'r': 255,
'g': 200,
'b': 120,
'dr': 0,
'dg': 0,
'db': 0,
'ddr': 0,
'ddg': 0,
'ddb': 0,
'brightness': 215,
'dbrightness': 20,
'ddbrightness': 0
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

reset.reset(lights, osc.OPTIONS)

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
