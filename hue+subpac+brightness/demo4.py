# Screen brightness + Hue lights

from phue import Bridge
import time
import sys
import oscilliate_lights as osc
import reset_lights as reset
import screen_brightness as screen

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
'dg': 5,
'db': 5,
'ddr': 0,
'ddg': -2,
'ddb': -6,
'brightness': 245,
'dbrightness': 10,
'ddbrightness': -5
}
dsb = osc.OPTIONS['dbrightness']/255 * 2/3
ddsb = osc.OPTIONS['ddbrightness']/255 * 2/3
screen_brightness = osc.OPTIONS['brightness']/255
screen.reset(screen_brightness)


osc.TARGET = {
'r': 255,
'g': 200,
'b': 104,
'brightness': 100,
'enabled': True,
'reached': False
}

osc.MODE = osc.MODES['BRIGHTNESS']
while not osc.TARGET['reached']:
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
        screen.change(screen_brightness, -dsb)
        time.sleep(osc.DELAYS[delay_mode][osc.UP])
    else:
        screen.change(screen_brightness, dsb)
        screen_brightness += ddsb
        time.sleep(osc.DELAYS[delay_mode][osc.DOWN])
        osc.updateOptions()
