import libs
import sys
import controller as hue
from multithread import Intervention
from pygame import time as pgtime

hue.init(bridge_ip = "128.12.141.85")
hue.group.on = True
cmd1 = hue.make_command(255, 0, 0, 255, 10)
cmd2 = hue.make_command(255, 210, 100, 255, 1)
cmd3 = hue.make_command(0, 255, 0, 255, 10)
cmds = [cmd1, cmd2, cmd3]
# test1_int = Intervention('TEST', 1, [print, pgtime.delay, print, pgtime.delay], [['C'], [3000], ['D'], [3000]])
hue.set_group(cmd1)
clock = pgtime.Clock()
experiments = 10
delay = 0
total_delay = 0
count = 20
interval = 700
experiment_delay = 3000
minimum = 1000000
maximum = -1
for j in range(experiments):
    for i in range(count):
        sys.stdout.write('*')
        sys.stdout.flush()
        clock.tick()
        hue.set_group(cmds[i%3], hue.group)
        t = clock.tick()
        delay += t
        minimum = min(t, minimum)
        maximum = max(t, maximum)
        pgtime.delay(interval)
    sys.stdout.write('\t Average delay for run {}: {}'.format(j, delay/count))
    total_delay+=delay
    delay = 0
    pgtime.delay(experiment_delay)
    print()
print('Average delay after {} requests within {} milisecond intervals, repeated {} times with {} miliseconds in between: {}'.format(count, interval, experiments, experiment_delay, total_delay/(count * experiments)))
print('Minimum delay: {}. Maxmimum delay: {}.'.format(minimum, maximum))
# Average delay after 100 requests within 1000 milisecond intervals: 29.01
# Average delay after 50 requests within 500 milisecond intervals: 26.88
# Average delay after 50 requests within 500 milisecond intervals: 27.32
