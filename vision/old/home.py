import sys
sys.path.insert(0, '/Users/kaandonbekci/dev/pervasivetech/Room')
import oscilliate_lights as oscilliate
from phue import Bridge
import random
import time
import librosa
import pygame as pg
import os
from rgbxy import Converter
exit()
# SETUP
file_name = "audio/heartbeat.mp3"
bridge_ip = "192.168.1.2"
# bridge_ip = "128.12.141.85"

hue_delay = 200
temp = 155
LOW = 180
HIGH = 255
BRIGHTNESS = .99
delta = .05
DEFAULT_VOLUME = .02 #at max volume on laptop + subpac, .02 feels feint

def play_music(music_file, beat_times, tempo, volume=DEFAULT_VOLUME):
    freq = 44100     # audio CD quality
    # freq = 20000 # changing this will make it slower/faster
    bitsize = -16    # unsigned 16 bit
    channels = 2     # 1 is mono, 2 is stereo
    buffer = 2048    # number of samples (experiment to get best sound)
    pg.mixer.init(freq, bitsize, channels, buffer)
    # volume value 0.0 to 1.0
    pg.mixer.music.set_volume(volume)
    try:
        pg.mixer.music.load(music_file)
        print("Music file {} loaded!".format(music_file))
    except pg.error:
        print("File {} not found! ({})".format(music_file, pg.get_error()))
        return
    global clock
    pg.mixer.music.play()
    clock = pg.time.Clock()
    # while pg.mixer.music.get_busy():
    #     if
    search_frame_rate = 60/tempo * 1000 / 40 #in ms
    # found_frame_rate = 60/tempo * 1000 / 10
    print('Search frame rate: {:0.2f} miliseconds'.format(search_frame_rate))
    threshold = search_frame_rate
    beat_tracker = 0
    found = False
    while pg.mixer.music.get_busy() and not found:
        clock.tick(search_frame_rate)
        if beat_times[beat_tracker] * 1000 - pg.time.get_ticks() < threshold:
            # print(pg.time.get_ticks())
            beat_lights(True)
            beat_tracker += 1
            # search_frame_rate = found_frame_rate
            found = True
    while pg.mixer.music.get_busy():
        try:
            clock.tick(search_frame_rate)
            if beat_times[beat_tracker] * 1000 - pg.time.get_ticks() < threshold:
                # print(pg.time.get_ticks())
                beat_lights(True)
                beat_screen(True)
                beat_screen(False)
                beat_lights(False)
                beat_tracker +=1
        except IndexError:
            break
    print()

def beat_lights(decrease):
    # global left
    # global right
    # global back
    if decrease:
        left.brightness = LOW
        right.brightness = LOW
        back.brightness = LOW
    # clock.tick(hue_delay)
        global temp
        left.colortemp = right.colortemp = back.colortemp = temp
        temp+=5
    if not decrease:
        left.brightness = HIGH
        right.brightness = HIGH
        back.brightness = HIGH
        sys.stdout.write('♥')
        sys.stdout.flush()

def beat_screen(decrease):
    global BRIGHTNESS
    if decrease:
        os.system("brightness " + str(BRIGHTNESS-delta))
    else:
        BRIGHTNESS -= delta/5
        os.system("brightness " + str(BRIGHTNESS))

def beat_track(input_file):
    print('Loading ', input_file)
    y, sr = librosa.load(input_file, sr=22050)
    # Use a default hop size of 512 samples @ 22KHz ~= 23ms
    hop_length = 512
    # This is the window length used by default in stft
    print('Tracking beats')
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr, hop_length=hop_length)
    print('Estimated tempo: {:0.2f} beats per minute'.format(tempo))
    # save output
    # 'beats' will contain the frame numbers of beat events.
    beat_times = librosa.frames_to_time(beats, sr=sr, hop_length=hop_length)
    print("Beat table generated:")
    print(beat_times)
    return (beat_times, tempo)

def initialize_lights():
    left.brightness = right.brightness = back.brightness = 255
    left.colortemp = right.colortemp = back.colortemp = temp

converter = Converter()
converter.rgb_to_xy(255, 0, 0)
b = Bridge(bridge_ip)
lights = b.get_light_objects()
for light in lights:
    light.on = True
    light.xy = converter.rgb_to_xy(255, 0, 0)
    time.sleep(.5)
    light.xy = converter.rgb_to_xy(0, 255, 0)
    time.sleep(.5)
    light.xy = converter.rgb_to_xy(0, 0, 255)
    time.sleep(.5)
    light.on = False

# left = lights[0]
# right = lights[1]
# back = lights[2]
# clock = None
# initialize_lights()
# exit()
# beat_times, tempo = beat_track(file_name)
# play_music(file_name, beat_times, tempo)
# print("done!")



# INTERVENTION_SPEED = 1
# INTERVENTION_INTENSITY = 0.001
#
# # Script for brightness.
# curr_brightness = 0.99
# increasing_brightness = False
# while True:
# 	delta = 0.0
# 	if curr_brightness < 0.3:
# 		increasing_brightness = True
# 	if curr_brightness > 0.97:
# 		increasing_brightness = False
# 	if increasing_brightness:
# 		delta = INTERVENTION_INTENSITY
# 	else:
# 		delta = -1.0 * INTERVENTION_INTENSITY
# 	curr_brightness += delta
# 	print(curr_brightness)
# 	os.system("brightness " + str(curr_brightness))
# 	os.system("sleep " + str(INTERVENTION_SPEED))
#




# pick a MP3 music file you have in the working folder
# otherwise give the full file path
# (try other sound file formats too)
# music_file = "Hot80s.mp3"
#
# # optional volume 0 to 1.0
# volume = 0.8
#
# play_music(music_file, volume)

# dx = .1
# dy = .1
#If running for the first time, press button on bridge and run with b.connect() uncommented
# b.connect()

# lights = b.get_light_objects()
#
# left = lights[0]
# right = lights[1]
# left.brightness = 255
# #MAX light.hue = 65535
# hue = 0
# dh = 200
# HUE_MAX = 65535
# left.hue = 0
# interval = 0
# while hue+dh < HUE_MAX:
# 	interval +=dh
# 	left.hue += dh
# 	hue = left.hue
# 	time.sleep(.5)
# 	if interval>1000:
# 		print(left.xy)
# 		print(left.hue)
# 		print(left.colormode)
# 		interval = 0
# time.sleep(1)
# left.hue = 0
# time.sleep(1)
# left.hue = 180
# time.sleep(1)
# left.hue = 360
# time.sleep(1)
# left.hue = 65535

# left.xy = [.1, .1]
# while(True):
# 	time.sleep(50.0/1000.0)
# 	cur = left.xy
# 	if cur[0] + dx > 1 or cur[0] + dx < 0:
# 		dx = -dx
# 	if cur[1] + dy > 1 or cur[1] + dy < 0:
# 		dy = -dy
# 	left.xy = [cur[0] + dx, cur[1] + dy]


#
# left.brightness = 0
# left.xy = [.5, .5]
# left.brightness = 254

# print(left.name)
# print(left._on)
# print(left._brightness)
# print(left._colormode)
# print(left._hue)
# print(left._saturation)
# print(left._xy)
# print(left._colortemp)
# print(left._effect)
# print(left._alert)
# print(left.transitiontime)
# print(left._reset_bri_after_on)
# print(left._reachable)
# print(left._type)


# for light in lights:
# 	# light.on = False
# 	light.xy = [.1,.1]
# 	light.on = True
# 	light.brightness = 255
