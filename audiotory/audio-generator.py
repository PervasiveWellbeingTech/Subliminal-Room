import libs
from wavebender import sine_wave, compute_samples, write_wavefile, super_sine_wave
import math

def sin(x):
    return math.sin(x)

def e_power(x):
    return math.exp(x)

def linear(x, a=1, b=0):
    return a * x + b

def exp(x, a):
    return math.pow(x, a) #returns x^a

def custom(x):
    a = exp(linear(e_power(sin(linear(x, a=2*math.pi*math.pi, b=-math.pi/2))), a=1/math.e), .5)
    b = exp(linear(sin(linear(x, a=.1*2*math.pi, b=-10*math.pi/2)), a=.5, b=.5), .5)
    return a * b
# args = [2, .5, .5]

channels = ((super_sine_wave(frequency = 100.0, amplitude=custom),),
            (super_sine_wave(frequency = 100.0, amplitude=custom),))

duration = 25
samples = compute_samples(channels, duration * 44100)

write_wavefile('/Users/kaandonbekci/dev/pervasivetech/Room/audiotory/audio/super_test.wav',samples)

# freqs = [20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140]
#
# oscs = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]
# for freq in freqs:
#     for osc in oscs:
#         amp = [math.sin, osc * 2 * math.pi, -math.pi/2, .5, .5]
#         channels = ((sine_wave(frequency = freq, amplitude=amp),),
#                     (sine_wave(frequency = freq, amplitude=amp),))
#         samples = compute_samples(channels, duration * 44100)
#         write_wavefile('/Users/kaandonbekci/dev/pervasivetech/Room/audiotory/audio/test/abi{}Hz_{}osc.wav'.format(freq, osc),samples)
#         print('finished {}Hz and {}osc.'.format(freq, osc))



# sine = [math.sin,   2 * 2 * math.pi,    -math.pi/2,     .5,     .5,     1]
#
# amp1 = [math.sin,   2 * 2 * math.pi,    -math.pi/2,     .5,     .5,     1]
# amp2 = [math.sin,   2 * 2 * math.pi,    -math.pi/2,     .5,     .5,     1]
#amp1 = c*f(ax+b)+d)^e
#amp1 = (amp[3]*amp[0](amp[1]*x + amp[2])+amp[4])^amp[5]
#amps = [amp1, amp2, amp3]
# sin(2 * pi * frequency) * amp[0][0]()
#       0           1                   2               3       4       5
