from rgbxy import Converter, GamutC
from phue import Bridge, Group

converter = None
DEFAULT_TRANSITION = 2
COMMAND_TEMPLATE = {
'R': 255,
'G': 255,
'B': 255,
'BRIGHTNESS': 255,
'TRANSITION': -1 #0 is continue
}
b = None
group = None
go = None

def set_light(command, hlight = None):
    if hlight is None:
        hlight = go
    if command['TRANSITION'] != 0:
        if command['TRANSITION'] > 0:
            hlight.transitiontime = command['TRANSITION']
        else:
            hlight.transitiontime = DEFAULT_TRANSITION
    hlight.xy = converter.rgb_to_xy(command['R'], command['G'], command['B'])
    hlight.brightness = command['BRIGHTNESS']

def set_group(command, hgroup = None):
    if hgroup is None:
        hgroup = group
    # print(group)
    # print(hgroup)
    if command['TRANSITION'] != 0:
        if command['TRANSITION'] > 0:
            hgroup.transitiontime = command['TRANSITION']
        else:
            hgroup.transitiontime = DEFAULT_TRANSITION
    hgroup.xy = converter.rgb_to_xy(command['R'], command['G'], command['B'])
    hgroup.brightness = command['BRIGHTNESS']


def make_command(rgb, brightness = 255, transition = 0):
    command = {
    'R': rgb[0],
    'G': rgb[1],
    'B': rgb[2],
    'BRIGHTNESS': brightness,
    'TRANSITION': transition #0 is default
    }
    return command

def init(bridge_ip = '192.168.1.2', gamut = GamutC):
    # print(bridge_ip)
    global converter, b, group, go
    converter = Converter(gamut)
    b = Bridge(bridge_ip)
    # print(b)
    group = Group(b, 1)
    # go = Group(b, 2)
    go = b['portable']
    # print(go)
    # print(group)

# def test():
#     init()
#     # g1.on = True
#     # print(g1.transitiontime)
#     cmds = []
#     cmds.append(make_command(255, 230, 240, 255, 1))
#     cmds.append(make_command(255, 0, 0))
#     cmds.append(make_command(0, 255, 0))
#     cmds.append(make_command(0, 0, 255))
#     i = 0
#     while True:
#         set_group(cmds[i%3], group)
#         i += 1
#         print(i)
# test()
