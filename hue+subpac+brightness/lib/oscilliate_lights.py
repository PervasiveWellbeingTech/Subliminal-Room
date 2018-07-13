# TODO: update TARGET['reached']
# TODO: migrate this to oscilliate_groups and make this for individual lights
# from phue import Bridge
import sys
from rgbxy import Converter
# import time

MODES = {
'COLOR': 1,
'BRIGHTNESS': 2,
'COLOR+BRIGHTNESS': 3,
'BRIGHTNESS+COLOR': 3
}
DELAYS = {
"BREATHING": [3.5, 4.5],
"NEUTRAL": [1.5, 1.5],
"FAST": [.5, .5]
}
UP = 0
DOWN = 1
MODE = MODES['BRIGHTNESS']
OPTIONS = {
'r': 255,
'g': 0,
'b': 0,
'dr': -30,
'dg': 50,
'db': 50,
'ddr': -30,
'ddg': 30,
'ddb': 50,
'brightness': 205,
'dbrightness': -50,
'ddbrightness': 0
}
TARGET = {
'r': 0,
'g': 0,
'b': 0,
'brightness': 0,
'enabled': False,
'reached': False
}
r_reached = False
g_reached = False
b_reached = False
brightness_reached = False


converter = Converter()
# bridge_ip = "192.168.1.2"
# bridge_ip = "128.12.141.85"

def oscilliate(light, up):
    if up:
        up = False
        return oscilliateUp(light)
    else:
        up = True
        return oscilliateDown(light)

def oscilliateUp(light):
    if MODE == MODES['COLOR']:
        light.xy = converter.rgb_to_xy(OPTIONS['r'] + OPTIONS['dr'], OPTIONS['g'] + OPTIONS['dg'], OPTIONS['b'] + OPTIONS['db'])
    elif MODE == MODES['BRIGHTNESS']:
        light.brightness = OPTIONS['brightness'] + OPTIONS['dbrightness']
    elif MODE == MODES['COLOR+BRIGHTNESS']:
        light.xy = converter.rgb_to_xy(OPTIONS['r'] + OPTIONS['dr'], OPTIONS['g'] + OPTIONS['dg'], OPTIONS['b'] + OPTIONS['db'])
        light.brightness = OPTIONS['brightness'] + OPTIONS['dbrightness']
    else:
        print('not supported MODE, check dictionary MODEs in "oscilliate-lights.py".')
        exit()

def oscilliateDown(light):
    if MODE == MODES['COLOR']:
        light.xy = converter.rgb_to_xy(OPTIONS['r'] - OPTIONS['dr'], OPTIONS['g'] - OPTIONS['dg'], OPTIONS['b'] - OPTIONS['db'])
    elif MODE == MODES['BRIGHTNESS']:
        light.brightness = OPTIONS['brightness'] - OPTIONS['dbrightness']
    elif MODE == MODES['COLOR+BRIGHTNESS']:
        light.xy = converter.rgb_to_xy(OPTIONS['r'] - OPTIONS['dr'], OPTIONS['g'] - OPTIONS['dg'], OPTIONS['b'] - OPTIONS['db'])
        light.brightness = OPTIONS['brightness'] - OPTIONS['dbrightness']
    else:
        print('not supported MODE, check dictionary MODEs in "oscilliate-lights.py".')
        exit()

def updateOptions():
    if MODE == MODES['COLOR']:
        if TARGET['enabled']:
            if OPTIONS['ddr'] > 0:
                if OPTIONS['r'] >= TARGET['r']:
                    OPTIONS['ddr'] = 0
                    OPTIONS['dr'] = 0
                if OPTIONS['r'] + abs(OPTIONS['dr']) > TARGET['r']:
                    OPTIONS['dr'] -= OPTIONS['ddr']
            elif OPTIONS['ddr'] < 0:
                if OPTIONS['r'] <= TARGET['r']:
                    OPTIONS['ddr'] = 0
                    OPTIONS['dr'] = 0
                if OPTIONS['r'] - abs(OPTIONS['dr']) < TARGET['r']:
                    OPTIONS['dr'] += OPTIONS['ddr']
            if OPTIONS['ddg'] > 0:
                if OPTIONS['g'] >= TARGET['g']:
                    OPTIONS['ddg'] = 0
                    OPTIONS['dg'] = 0
                if OPTIONS['g'] + abs(OPTIONS['dg']) > TARGET['g']:
                    OPTIONS['dg'] -= OPTIONS['ddg']
            elif OPTIONS['ddg'] < 0:
                if OPTIONS['g'] <= TARGET['g']:
                    OPTIONS['ddg'] = 0
                    OPTIONS['dg'] = 0
                if OPTIONS['g'] - abs(OPTIONS['dg']) < TARGET['g']:
                    OPTIONS['dg'] += OPTIONS['ddg']
            if OPTIONS['ddb'] > 0:
                if OPTIONS['b'] >= TARGET['b']:
                    OPTIONS['ddb'] = 0
                    OPTIONS['db'] = 0
                if OPTIONS['b'] + abs(OPTIONS['db']) > TARGET['b']:
                    OPTIONS['db'] -= OPTIONS['ddb']
            elif OPTIONS['ddb'] < 0:
                if OPTIONS['b'] <= TARGET['b']:
                    OPTIONS['ddb'] = 0
                    OPTIONS['db'] = 0
                if OPTIONS['b'] - abs(OPTIONS['db']) < TARGET['b']:
                    OPTIONS['db'] += OPTIONS['ddb']
        OPTIONS['r'] = min(max(OPTIONS['r'] + OPTIONS['ddr'], 0), 255)
        OPTIONS['g'] = min(max(OPTIONS['g'] + OPTIONS['ddg'], 0), 255)
        OPTIONS['b'] = min(max(OPTIONS['b'] + OPTIONS['ddb'], 0), 255)
    elif MODE == MODES['BRIGHTNESS']:
        if TARGET['enabled']:
            if OPTIONS['ddbrightness'] > 0:
                if OPTIONS['brightness'] >= TARGET['brightness']:
                    OPTIONS['ddbrightness'] = 0
                    OPTIONS['dbrightness'] = 0
                if OPTIONS['brightness'] + abs(OPTIONS['dbrightness']) > TARGET['brightness']:
                    OPTIONS['dbrightness'] -= OPTIONS['ddbrightness']
            elif OPTIONS['ddbrightness'] < 0:
                if OPTIONS['brightness'] <= TARGET['brightness']:
                    OPTIONS['ddbrightness'] = 0
                    OPTIONS['dbrightness'] = 0
                if OPTIONS['brightness'] - abs(OPTIONS['dbrightness']) < TARGET['brightness']:
                    OPTIONS['dbrightness'] += OPTIONS['ddbrightness']
        OPTIONS['brightness'] = min(max(OPTIONS['brightness'] + OPTIONS['ddbrightness'], 0), 255)
    elif MODE == MODES['COLOR+BRIGHTNESS']:
        if TARGET['enabled']:
            if OPTIONS['ddr'] > 0:
                if OPTIONS['r'] >= TARGET['r']:
                    OPTIONS['ddr'] = 0
                    OPTIONS['dr'] = 0
                if OPTIONS['r'] + abs(OPTIONS['dr']) > TARGET['r']:
                    OPTIONS['dr'] -= OPTIONS['ddr']
            elif OPTIONS['ddr'] < 0:
                if OPTIONS['r'] <= TARGET['r']:
                    OPTIONS['ddr'] = 0
                    OPTIONS['dr'] = 0
                if OPTIONS['r'] - abs(OPTIONS['dr']) < TARGET['r']:
                    OPTIONS['dr'] += OPTIONS['ddr']
            if OPTIONS['ddg'] > 0:
                if OPTIONS['g'] >= TARGET['g']:
                    OPTIONS['ddg'] = 0
                    OPTIONS['dg'] = 0
                if OPTIONS['g'] + abs(OPTIONS['dg']) > TARGET['g']:
                    OPTIONS['dg'] -= OPTIONS['ddg']
            elif OPTIONS['ddg'] < 0:
                if OPTIONS['g'] <= TARGET['g']:
                    OPTIONS['ddg'] = 0
                    OPTIONS['dg'] = 0
                if OPTIONS['g'] - abs(OPTIONS['dg']) < TARGET['g']:
                    OPTIONS['dg'] += OPTIONS['ddg']
            if OPTIONS['ddb'] > 0:
                if OPTIONS['b'] >= TARGET['b']:
                    OPTIONS['ddb'] = 0
                    OPTIONS['db'] = 0
                if OPTIONS['b'] + abs(OPTIONS['db']) > TARGET['b']:
                    OPTIONS['db'] -= OPTIONS['ddb']
            elif OPTIONS['ddb'] < 0:
                if OPTIONS['b'] <= TARGET['b']:
                    OPTIONS['ddb'] = 0
                    OPTIONS['db'] = 0
                if OPTIONS['b'] - abs(OPTIONS['db']) < TARGET['b']:
                    OPTIONS['db'] += OPTIONS['ddb']
            if OPTIONS['ddbrightness'] > 0:
                if OPTIONS['brightness'] >= TARGET['brightness']:
                    OPTIONS['ddbrightness'] = 0
                    OPTIONS['dbrightness'] = 0
                if OPTIONS['brightness'] + abs(OPTIONS['dbrightness']) > TARGET['brightness']:
                    OPTIONS['dbrightness'] -= OPTIONS['ddbrightness']
            elif OPTIONS['ddbrightness'] < 0:
                if OPTIONS['brightness'] <= TARGET['brightness']:
                    OPTIONS['ddbrightness'] = 0
                    OPTIONS['dbrightness'] = 0
                if OPTIONS['brightness'] - abs(OPTIONS['dbrightness']) < TARGET['brightness']:
                    OPTIONS['dbrightness'] += OPTIONS['ddbrightness']
        OPTIONS['r'] = min(max(OPTIONS['r'] + OPTIONS['ddr'], 0), 255)
        OPTIONS['g'] = min(max(OPTIONS['g'] + OPTIONS['ddg'], 0), 255)
        OPTIONS['b'] = min(max(OPTIONS['b'] + OPTIONS['ddb'], 0), 255)
        OPTIONS['brightness'] = min(max(OPTIONS['brightness'] + OPTIONS['ddbrightness'], 0), 255)
    else:
        print('not supported MODE, check dictionary MODEs in "oscilliate-lights.py".')
        exit()

# def test():
#     b = Bridge(bridge_ip)
#     converter = Converter()
#     lights = b.get_light_objects()
#     up = True
#     while True:
#         if up:
#         else:
#             time.sleep(DOWN_DELAY)
#         sys.stdout.flush()
#         for light in lights:
#             oscilliate(light, up)
#             # print(light.xy)
#             # print(light.brightness)
#         up = not up
#         if up: #after up, up is not up and DOWN_DELAY is needed
#             time.sleep(DOWN_DELAY)
#         else:
#             time.sleep(UP_DELAY)
#             updateOptions()
#         # print(OPTIONS)
