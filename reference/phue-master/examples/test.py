from phue import Bridge
import random
import time

b = Bridge("192.168.0.100") # Enter bridge IP here.
dx = .1
dy = .1
#If running for the first time, press button on bridge and run with b.connect() uncommented
# b.connect()

lights = b.get_light_objects()

left = lights[0]
right = lights[1]
left.brightness = 255
#MAX light.hue = 65535
hue = 0
dh = 200
HUE_MAX = 65535
left.hue = 0
interval = 0
while hue+dh < HUE_MAX:
	interval +=dh
	left.hue += dh
	hue = left.hue
	time.sleep(.5)
	if interval>1000:
		print(left.xy)
		print(left.hue)
		print(left.colormode)
		interval = 0
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
