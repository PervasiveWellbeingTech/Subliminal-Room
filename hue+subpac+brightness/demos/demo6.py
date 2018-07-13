# Heartbeat simulation
# calculate FIRST_TO_SECOND, SECOND_TO_FIRST table beforehand
import libs
import time
import sys
from pygame import mixer
from pygame import time as pgtime
import math

mixer.init()
first_beat = mixer.Sound('../audio/first-beat.ogg')
second_beat = mixer.Sound('../audio/second-beat.ogg')
bpm = 60
dpm = 1
interval = 5
counter = 0
FIRST_TO_SECOND = max(math.floor(60 / bpm * 1000 * 13/36 * 1076/1000), 0)
SECOND_TO_FIRST = max(math.floor(60 / bpm * 1000 * 23/36 * 1076/1000), 0)
print('BPM: {},  FIRST_TO_SECOND: {}, SECOND_TO_FIRST: {}, TOTAL: {}'.format(bpm, FIRST_TO_SECOND, SECOND_TO_FIRST, FIRST_TO_SECOND + SECOND_TO_FIRST))
ERROR_MARGIN = 0
clock = pgtime.Clock()
# offset = pgtime.get_ticks()
while True:
    counter += 1
    # print('0: {}'.format(clock.tick()))
    mixer.Sound.play(first_beat)
    # print('A: {}'.format(clock.tick()))
    # print('B: {}'.format(clock.tick()))
    sys.stdout.write('↑ ')
    sys.stdout.flush()
    # print('C: {}'.format(clock.tick()))
    # lag = clock.tick()
    # print(lag)
    pgtime.delay(FIRST_TO_SECOND)
    # print('D: {}'.format(clock.tick()))
    mixer.Sound.stop(first_beat)
    mixer.Sound.play(second_beat)
    # print('E: {}'.format(clock.tick()))
    sys.stdout.write('↓ ')
    sys.stdout.flush()
    # print('F: {}'.format(clock.tick()))
    pgtime.delay(SECOND_TO_FIRST)
    mixer.Sound.stop(second_beat)
    # print('G: {}'.format(clock.tick()))
    if(counter == interval):
        print()
        bpm += dpm
        FIRST_TO_SECOND = max(math.floor(60 / bpm * 1000 * 13/36 * 1076/1000), 0)
        SECOND_TO_FIRST = max(math.floor(60 / bpm * 1000 * 23/36 * 1076/1000), 0)
        print('Changing BPM to {},  FIRST_TO_SECOND: {}, SECOND_TO_FIRST: {}, TOTAL: {}'.format(bpm, FIRST_TO_SECOND, SECOND_TO_FIRST, FIRST_TO_SECOND + SECOND_TO_FIRST))
        counter = 0
        # print('H: {}'.format(clock.tick()))
