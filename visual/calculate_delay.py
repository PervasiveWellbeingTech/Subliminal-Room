import libs
import sys
import controller as hue
from multithread import Intervention
from pygame import time as pgtime

# hue.init(bridge_ip = "128.12.141.85")
hue.init()
hue.group.on = True
hue_delay = 0
cmd1 = hue.make_command(255, 200, 80, 255, hue_delay)
cmd2 = hue.make_command(255, 210, 100, 255, hue_delay)
cmd3 = hue.make_command(255, 230, 120, 255, hue_delay)
cmds = [cmd1, cmd2, cmd3]
# test1_int = Intervention('TEST', 1, [print, pgtime.delay, print, pgtime.delay], [['C'], [3000], ['D'], [3000]])
hue.set_group(cmd1)
clock = pgtime.Clock()
experiments = 100
delay = 0
total_delay = 0
count = 10
interval = 500
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
    sys.stdout.write('\t Average delay for run {}: {}'.format(j+1, delay/count))
    sys.stdout.flush()
    total_delay+=delay
    delay = 0
    pgtime.delay(experiment_delay)
    print()
print('Average delay after {} requests with transition time {} within {} milisecond intervals, repeated {} times with {} miliseconds in between: {}'.format(count, hue_delay, interval, experiments, experiment_delay, total_delay/(count * experiments)))
print('Minimum delay: {}. Maxmimum delay: {}.'.format(minimum, maximum))

#  RESULTS:
# Average delay after 20 requests with transition time 0 within 500 milisecond intervals, repeated 10 times with 3000 miliseconds in between: 93.01
# Minimum delay: 51. Maxmimum delay: 174.
#
# Average delay after 10 requests with transition time 0 within 500 milisecond intervals, repeated 10 times with 3000 miliseconds in between: 102.7
# Minimum delay: 63. Maxmimum delay: 700.
#
# Average delay after 5 requests with transition time 0 within 200 milisecond intervals, repeated 20 times with 3000 miliseconds in between: 95.48
# Minimum delay: 66. Maxmimum delay: 197.
