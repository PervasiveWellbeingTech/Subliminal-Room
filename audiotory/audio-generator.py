import libs
from wavebender import *
import math

amp1 = [math.sin, 2 * 2 * math.pi, -math.pi/2, .5, .5]
amp2 = [math.sin, 2 * 2 * math.pi, -math.pi/2, .5, .5]

channels = ((sine_wave(a = 1, frequency = 150.0, amplitude=amp1),),
            (sine_wave(a = 1, frequency = 150.0, amplitude=amp2),))

duration = 20
# samples = compute_samples(channels, duration * 44100)

# write_wavefile('/Users/kaandonbekci/dev/pervasivetech/Room/audiotory/audio/test.wav',samples)

freqs = [20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140]

oscs = [1, 1.5, 2, 2.5, 3, 3.5, 4]
for freq in freqs:
    for osc in oscs:
        amp = [math.sin, osc * 2 * math.pi, -math.pi/2, .5, .5]
        channels = ((sine_wave(a = 1, frequency = freq, amplitude=amp),),
                    (sine_wave(a = 1, frequency = freq, amplitude=amp),))
        samples = compute_samples(channels, duration * 44100)
        write_wavefile('/Users/kaandonbekci/dev/pervasivetech/Room/audiotory/audio/test/{}Hz_{}osc.wav'.format(freq, osc),samples)
        print('finished {}Hz and {}osc.'.format(freq, osc))
