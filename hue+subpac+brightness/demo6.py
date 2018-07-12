# Hue lights + Subpac + Heartbeat

# from phue import Bridge
import time
import sys
# import oscilliate_lights as osc
# import reset_lights as reset
import pygame as pg
import math

mixer = pg.mixer
pgtime = pg.time
# pg.init()
# bridge_ip = '192.168.1.2'
# b = Bridge(bridge_ip)
# lights = b.get_light_objects()
# reset.reset(lights, [255, 255, 255], 255)
# up = True
# input = input('name of the file? \n')
# mixer.pre_init(44100, 16, 2, 4096)
mixer.init()
first_beat = mixer.Sound('audio/first-beat.ogg')
second_beat = mixer.Sound('audio/second-beat.ogg')

# osc.OPTIONS = {
# 'r': 255,
# 'g': 255,
# 'b': 255,
# 'dr': 0,
# 'dg': 0,
# 'db': 0,
# 'ddr': 0,
# 'ddg': -1,
# 'ddb': -4,
# 'brightness': 225,
# 'dbrightness': 15,
# 'ddbrightness': -3
# }
#
# osc.TARGET = {
# 'r': 255,
# 'g': 190,
# 'b': 50,
# 'brightness': 80,
# 'enabled': True,
# 'reached': False
# }
#
# osc.MODE = osc.MODES['BRIGHTNESS+COLOR']
bpm = 60
# counter = 0
# DELAY_PER_CALL = .105 #seconds
# THRESHOLD = 50
# EXEC_1 = 200
# EXEC_2 = 200
FIRST_TO_SECOND = max(math.floor(60 / bpm * 1000 * 11/36 * 1076/1000), 0)
# FIRST_TO_SECOND = math.floor(331/ 1076 * 1000)
SECOND_TO_FIRST = max(math.floor(60 / bpm * 1000 * 25/36 * 1076/1000), 0)
# SECOND_TO_FIRST = math.floor(745/ 1076 * 1000)

print('FIRST_TO_SECOND: {}'.format(FIRST_TO_SECOND))
print('SECOND_TO_FIRST: {}'.format(SECOND_TO_FIRST))
print('TOTAL: {}'.format(FIRST_TO_SECOND + SECOND_TO_FIRST))
# print(FIRST_TO_SECOND + SECOND_TO_FIRST)
ERROR_MARGIN = 0
clock = pgtime.Clock()
offset = pgtime.get_ticks()
while True:
    # mixer.music.play()
    print('0: {}'.format(clock.tick()))

    mixer.Sound.play(first_beat)
    print('A: {}'.format(clock.tick()))
    print('B: {}'.format(clock.tick()))

    sys.stdout.write('↑ ')
    sys.stdout.flush()
    print('C: {}'.format(clock.tick()))

    # lag = clock.tick()
    # print(lag)
    pgtime.delay(FIRST_TO_SECOND)
    print('D: {}'.format(clock.tick()))
    mixer.Sound.stop(first_beat)
    mixer.Sound.play(second_beat)
    print('E: {}'.format(clock.tick()))

    sys.stdout.write('↓ ')
    sys.stdout.flush()
    print('F: {}'.format(clock.tick()))
    pgtime.delay(SECOND_TO_FIRST)
    mixer.Sound.stop(second_beat)
    print('G: {}'.format(clock.tick()))
    bpm -= 0
    FIRST_TO_SECOND = max(math.floor(60 / bpm * 1000 * 13/36 * 1076/1000), 0)
    SECOND_TO_FIRST = max(math.floor(60 / bpm * 1000 * 23/36 * 1076/1000), 0)
    print('H: {}'.format(clock.tick()))

        # mixer.music.stop()
