import libs
from multithread import Intervention
import controller as hue
import oscilliate_group as osc
import reset
import time
from pygame import time as pgtime

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

hue.init(bridge_ip = "128.12.141.85")
# cmd = hue.make_command(255, 255, 255, 155, 5)
# hue.set_group(hue.group, cmd)
cmd1 = hue.make_command(255, 255, 255, 255, 0)
cmd2 = hue.make_command(255, 0, 0, 255, 0)
hue.group.on = True
print(cmd1)
test1_int = Intervention('TEST', 1,
    [hue.set_group, pgtime.delay, hue.set_group, pgtime.delay], [[cmd1, hue.group], [3000], [cmd2, hue.group], [3000]])
test2_int = Intervention('TEST', 2, [print, pgtime.delay, print, pgtime.delay], [['A'], [3000], ['B'], [3000]])
test3_int = Intervention('TEST', 2, [print, pgtime.delay, print, pgtime.delay], [['C'], [3000], ['D'], [3000]])
test4_int = Intervention('TEST', 2, [print, pgtime.delay, print, pgtime.delay], [['E'], [3000], ['F'], [3000]])
clock = pgtime.Clock()
delay = 0
for i in range(100):
    clock.tick()
    hue.set_group(cmd2, hue.group)
    delay += clock.tick()
    pgtime.delay(2000)

test1_int.start()
test2_int.start()
test3_int.start()
test4_int.start()
