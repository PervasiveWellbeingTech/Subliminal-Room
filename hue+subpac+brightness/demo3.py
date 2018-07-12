# Hue lights + Subpac + Heartbeat

from phue import Bridge
import time
import sys
import oscilliate_lights as osc
import reset_lights as reset
import track_beats as trck
from pygame import mixer
from pygame import time as pgtime

bridge_ip = '192.168.1.2'
b = Bridge(bridge_ip)
lights = b.get_light_objects()
reset.reset(lights, [255, 255, 255], 255)
up = True
input = input('name of the file? \n')
audio_file = 'audio/'+input
mixer.init()
mixer.music.load(audio_file)

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
'brightness': 225,
'dbrightness': 15,
'ddbrightness': -5
}

osc.TARGET = {
'r': 255,
'g': 255,
'b': 255,
'brightness': 50,
'enabled': False,
'reached': False
}

osc.MODE = osc.MODES['BRIGHTNESS']
beat_table, tempo = trck.track_beats(audio_file)
counter = 0
DELAY_PER_CALL = .105 #seconds
THRESHOLD = 50
FIRST_TO_SECOND = 315 #ms
# SECOND_TO_FIRST = (tempo / 60) - FIRST_TO_SECOND
ERROR_MARGIN = 0
mixer.music.play()
clock = pgtime.Clock()
offset = pgtime.get_ticks()

while not osc.TARGET['reached']:
    if (pgtime.get_ticks() - offset + DELAY_PER_CALL)/1000>= beat_table[counter]:
        counter += 1
        for light in lights:
            osc.oscilliate(light, up)
        sys.stdout.write('↑ ')
        sys.stdout.flush()
        pgtime.delay(FIRST_TO_SECOND - THRESHOLD)
        for light in lights:
            osc.oscilliate(light, not up)
        sys.stdout.write('↓ ')
        sys.stdout.flush()
        osc.updateOptions()