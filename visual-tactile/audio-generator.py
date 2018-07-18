import libs
from wavebender import *

channels = ((sine_wave(a = .1, frequency = 10.0, amplitude=1),),
            (sine_wave(a = .1, frequency = 10.0, amplitude=1),))

samples = compute_samples(channels, 1000000)

write_wavefile('./audio/test.wav', samples)
