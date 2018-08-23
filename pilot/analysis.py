from __future__ import division
import libs
import json
import os

outputDir = libs.path + 'pilot/output'
participants = {}

def init():
    global participants
    for i in os.listdir(outputDir):
        if os.path.isdir(os.path.join(outputDir, i)) and not i == 'test':
            participants[i] = {
            'dir': os.path.join(outputDir, i) + '/',
            'experiment': {},
            'params': {},
            'analysis':{}
            }
    for i in participants:
        p = participants[i]
        with open(p['dir'] + 'experiment.json', 'r') as f:
            p['experiment'] = json.load(f)
        with open(p['dir'] + 'params.json', 'r') as f:
            p['params'] = json.load(f)

def colorToText(hsv):
    text = ''
    if hsv[1] == 1.0:
        text = text+'VIVID_'
    elif hsv[1] == .5:
        text = text + 'PALE_'
    elif hsv[1] == 0.0:
        text = 'WHITE'
        return text;
    else:
        raise ValueError('Saturation is not in one of 0.0, 0.5, 1.0!')
    if hsv[0] == 0.0:
        text = text + 'RED'
    elif hsv[0] == 120.0:
        text = text + 'GREEN'
    elif hsv[0] == 240.0:
        text = text + 'BLUE'
    else:
        raise ValueError('Hue is not in in one of 0.0, 120.0, 240.0!')
    return text

def populateColorAnalysisPerParticipant(p):
    accuracyAnalysis(p)
    responseTimeAnalysis(p)


init()
for i in participants:
    populateColorAnalysisPerParticipant(participants[i])
print colorToText([120.0, 0.5, 1.0])
