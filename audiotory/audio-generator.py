import libs
from wavebender import *

channels = ((sine_wave(a = .4, frequency = 501.0, amplitude=.5),),
            (sine_wave(a = .4, frequency = 502.0, amplitude=1),))


samples = compute_samples(channels, 1000000)

write_wavefile('./audio/test.wav', samples)
