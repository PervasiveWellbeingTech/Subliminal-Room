from __future__ import division
import libs
import json
import time
import os
import math
import pprint as pp
pprint = pp.PrettyPrinter(indent=4).pprint
import numpy as np
import matplotlib.pyplot as plt
import colorsys
import pandas
from calendar import timegm
outputDir = libs.path + 'pilot/output'
participants = {}
def epoch(str):
    return timegm(time.strptime(str, '%d/%m/%Y %H:%M:%S.%f')) + 7 * 60 * 60

def init():
    global participants
    for i in os.listdir(outputDir):
        if os.path.isdir(os.path.join(outputDir, i)) and not i == 'test':
            participants[i] = {
            'dir': os.path.join(outputDir, i) + '/',
            'experiment': {},
            'params': {},
            'analysis':{},
            'measurements': {}
            }
    for i in participants:
        p = participants[i]
        p['measurements']['nback'] = []
        data = pandas.read_csv(p['dir'] + 'measurements/summary.csv')
        data['Time'] = data['Time'].map(epoch)
        cur = 0
        with open(p['dir'] + 'experiment.json', 'r') as f:
            p['experiment'] = json.load(f)['experiment']
        with open(p['dir'] + 'params.json', 'r') as f:
            p['params'] = json.load(f)['params']
        for n in range(p['params']['nBlocks']):
            p['analysis'][colorToText(p['experiment']['colors'][n])] = {}
            inBounds = False
            begin, end = 0, 0
            while not inBounds:
                if data['Time'][cur] < p['experiment']['nback']['unixTimes'][n][0]:
                    cur += 1
                else:
                    begin = cur
                    inBounds = True
            while inBounds:
                if data['Time'][cur] < p['experiment']['nback']['unixTimes'][n][1]:
                    cur += 1
                else:
                    end = cur
                    inBounds = False
            p['measurements']['nback'].append(data[begin:end])
        # print p['measurements'].columns.values.tolist()

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

def accuracyAnalysis(p):
    p['analysis']['averageAccuracy'] = 0.0
    n = p['params']['nBlocks']
    for i in range(n):
        p['analysis'][colorToText(p['experiment']['colors'][i])]['accuracy'] = {
        'mean': 0.0,
        'sd': 0.0,
        }
        sum = 0.0
        c = 0
        for x in p['experiment']['nback']['responses']['corrected'][i]:
            sum += x
            c += 1
        mean = sum / c
        p['analysis'][colorToText(p['experiment']['colors'][i])]['accuracy']['mean'] = mean
        sum = 0.0
        for x in p['experiment']['nback']['responses']['corrected'][i]:
            sum += (x - mean) * (x- mean)
        sd = math.sqrt(sum/(c-1))
        p['analysis'][colorToText(p['experiment']['colors'][i])]['accuracy']['sd'] = sd

def responseTimeAnalysis(p):
    p['analysis']['averageResponseTime'] = 0.0
    n = p['params']['nBlocks']
    for i in range(n):
        p['analysis'][colorToText(p['experiment']['colors'][i])]['responseTimes'] = {
        'mean': 0.0,
        'sd': 0.0,
        }
        sum = 0.0
        c = 0
        for x in p['experiment']['nback']['responseTimes'][i]:
            sum += x
            c += 1
        mean = sum / c
        p['analysis'][colorToText(p['experiment']['colors'][i])]['responseTimes']['mean'] = mean
        sum = 0.0
        for x in p['experiment']['nback']['responseTimes'][i]:
            sum += (x - mean) * (x- mean)
        sd = math.sqrt(sum/(c-1))
        p['analysis'][colorToText(p['experiment']['colors'][i])]['responseTimes']['sd'] = sd

def populateColorAnalysisPerParticipant(p):
    accuracyAnalysis(p)
    responseTimeAnalysis(p)

init()
for i in participants:
    p = participants[i]
    populateColorAnalysisPerParticipant(p)
    # pprint(p['analysis'])
    # print
    f, ax = plt.subplots(p['params']['nBlocks'], 4, sharex='col')
    f.set_size_inches(10, 10)
    ax[0, 0].set_title('Response Time')
    ax[0, 1].set_title('Num. correct')
    ax[0, 2].set_title('HR')
    ax[0, 3].set_title('BR')
    ax[p['params']['nBlocks']-1, 0].set_xlabel('t (s)')
    ax[p['params']['nBlocks']-1, 1].set_xlabel('-1: missed, 0: wrong, 1: correct')
    ax[p['params']['nBlocks']-1, 2].set_xlabel('BPM')
    ax[p['params']['nBlocks']-1, 3].set_xlabel('BPM')
    f.suptitle(i, fontsize=12, y=1.0, x=0.05)
    f.tight_layout()
    for n in range(p['params']['nBlocks']):
        c = p['experiment']['colors'][n]
        rgb = colorsys.hsv_to_rgb(c[0]/360.0, c[1], c[2])
        # print rgb
        if rgb == (1.0, 1.0, 1.0):
            rgb = (0.0, 0.0, 0.0)
        ax[n, 0].hist(p['experiment']['nback']['responseTimes'][n], color=rgb, lw=0, bins=[-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0])
        ax[n, 0].axvline(x=p['analysis'][colorToText(p['experiment']['colors'][n])]['responseTimes']['mean'])
        ax[n, 1].hist(p['experiment']['nback']['responses']['corrected'][n], color=rgb, lw=0, bins=[-1.0, -0.75, -0.5, -0.25, 0.0, 0.25, 0.50, 0.75, 1.0])
        ax[n, 1].axvline(x=p['analysis'][colorToText(p['experiment']['colors'][n])]['accuracy']['mean'])
        ax[n, 2].hist(p['measurements']['nback'][n]['HR'], color='black', bins=[62, 64, 66, 68, 70, 72, 74, 76, 78, 80, 82, 84, 86, 88, 90, 92, 94, 96, 98, 100, 102, 104, 106, 108, 110])
        ax[n, 3].hist(p['measurements']['nback'][n]['BR'], color='black')
        ax[n, 0].set_ylim([0, 50])
        ax[n, 1].set_ylim([0, 120])
        ax[n, 2].set_ylim([0, 100])
        ax[n, 3].set_ylim([0, 150])
    # break
    # f.savefig('pilot/analysis/{}.png'.format(i))

plt.show()
# print colorToText([120.0, 0.5, 1.0])
