#!/usr/bin/env python
from wavebender import *
from math import cos

channels = ((square_wave(440.0, amplitude=0.1),),)

samples = compute_samples(channels, 44100 * 60 * 1)
write_wavefile(stdout, samples, 44100 * 60 * 1, nchannels=1)
