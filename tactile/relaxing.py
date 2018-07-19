import libs
from wavebender import *

channels = ((sine_wave(a = 1, frequency = .5, amplitude=.1),),
            (sine_wave(a = 1, frequency = .5, amplitude=.1),))


samples = compute_samples(channels, 1000000)

write_wavefile('./haptic-audio/test.wav', samples)
