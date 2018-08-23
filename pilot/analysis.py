from __future__ import division
import libs
import json
import os

outputDir = libs.path + 'pilot/output'
participants = {}

for i in os.listdir(outputDir):
    if os.path.isdir(os.path.join(outputDir, i)) and i is not 'test':
        participants[i] = {
        'dir': os.path.join(outputDir, i)
        }

for participant in participants:
    
