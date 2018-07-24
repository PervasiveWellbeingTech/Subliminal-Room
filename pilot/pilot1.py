import libs
from multithread import Intervention
import controller as hue
import oscilliate_group as osc
import reset
import time

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
'brightness': 235,
'dbrightness': 20,
'ddbrightness': 5
}

hue.init()
# cmd = hue.make_command(255, 255, 255, 155, 5)
# hue.set_group(hue.group, cmd)

hue_int = Intervention('HUE', 1, [osc.oscilliate, print, time.sleep, osc.oscilliate, print, time.sleep, osc.updateOptions], [[hue.group, True], ['a'], [2], [hue.group, False], ['b'], [2], []])

hue_int.start()
time.sleep(100)
