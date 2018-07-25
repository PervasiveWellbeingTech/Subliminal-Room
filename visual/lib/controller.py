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

def init(bridge_ip = '192.168.1.2', gamut = GamutC):
    # print(bridge_ip)
    global converter, b, group
    converter = Converter(gamut)
    b = Bridge(bridge_ip)
    # print(b)
    group = Group(b, 1)
    # print(group)

def test():
    init()
    # g1.on = True
    # print(g1.transitiontime)
    cmds = []
    cmds.append(make_command(255, 230, 240, 255, 1))
    cmds.append(make_command(255, 0, 0))
    cmds.append(make_command(0, 255, 0))
    cmds.append(make_command(0, 0, 255))
    i = 0
    while True:
        set_group(group, cmds[i%3])
        i += 1
        print(i)
# test()
