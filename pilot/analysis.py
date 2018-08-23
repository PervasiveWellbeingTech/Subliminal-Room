from __future__ import division
import libs
import json
import os

outputDir = libs.path + 'pilot/output'
# cur = sum(os.path.isdir(
# os.path.join(outputDir, i)) for i in os.listdir(outputDir))
# participants = []
for i in os.listdir(outputDir):
    if os.path.isdir(os.path.join(outputDir, i)) and i is not 'test':
        print i
