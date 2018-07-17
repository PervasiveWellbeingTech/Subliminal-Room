# Heartbeat simulation
# calculate FIRST_TO_SECOND, SECOND_TO_FIRST table beforehand
import libs
import time
import sys
from pygame import mixer
from pygame import time as pgtime
import math

mixer.init()
first_beat = mixer.Sound('./audio/first-beat.ogg')

interval = 10
counter = 0

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
    # print('D: {}'.format(clock.tick()))
    # print('E: {}'.format(clock.tick()))
    sys.stdout.write('↓ ')
    sys.stdout.flush()
    # print('F: {}'.format(clock.tick()))
    # print('G: {}'.format(clock.tick()))
    if(counter == interval):
        print()
        counter = 0
        # print('H: {}'.format(clock.tick()))
