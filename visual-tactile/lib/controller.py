from rgbxy import Converter
from phue import Bridge, Group

bridge_ip = '192.168.1.2'
converter = Converter()
DEFAULT_TRANSITION = None
COMMAND_TEMPLATE = {
'R': 255,
'G': 255,
'B': 255,
'BRIGHTNESS': 255,
'TRANSITION': -1 #0 is continue
}

def set_group(group, command):
    if command['TRANSITION'] != 0:
        if command['TRANSITION'] > 0:
            group.transitiontime = command['TRANSITION']
        else:
            group.transitiontime = DEFAULT_TRANSITION
    group.xy = converter.rgb_to_xy(command['R'], command['G'], command['B'])
    group.brightness = command['BRIGHTNESS']

# def set_light(light, command):

def make_command(r, g, b, brightness = 255, transition = 0):
    command = {
    'R': r,
    'G': g,
    'B': b,
    'BRIGHTNESS': brightness,
    'TRANSITION': transition #0 is default
    }
    return command

# def test():
#     converter = Converter()
#     b = Bridge(bridge_ip)
#     # print(b.get_group()['1'])
#     g1 = Group(b, 1)
#     print(g1)
#     # g1.on = True
#     # print(g1.transitiontime)
#     cmds = []
#     cmds.append(make_command(255, 255, 255, 255, 1))
#     cmds.append(make_command(255, 0, 0))
#     cmds.append(make_command(0, 255, 0))
#     cmds.append(make_command(0, 0, 255))
#     i = 0
#     while True:
#         set_group(g1, cmds[i%3])
#         i += 1
#         print(i)
# test()
