import libs
from wavebender import *
import math

amp = [math.sin, 1.0, .5, .5]

channels = ((sine_wave(a = 1, frequency = 100.0, amplitude=amp),),
            (sine_wave(a = 1, frequency = 100.0, amplitude=amp),))

samples = compute_samples(channels, 1000000)

write_wavefile('/Users/kaandonbekci/dev/pervasivetech/Room/audiotory/audio/test.wav',samples)
