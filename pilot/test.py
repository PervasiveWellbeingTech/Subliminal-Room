# -*- coding: utf-8 -*-
from __future__ import division
import libs
import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")
from psychopy import visual, core, sound, logging, event, clock
import controller as hue
import random
import os
import json
import pprint as pp
pprint = pp.PrettyPrinter(indent=4).pprint

params = {
    # Declare stimulus and response parameters
    # 'stimDur': {
    #     'nback': 2,
    #     'arithmetic': 5
    # },             # time when stimulus is presented (in seconds)
    # 'ISI':{
    #     'nback': .5,
    #     'arithmetic': 1
    # },                 # time between when one stimulus disappears and the next appears (in seconds)
    'tStartup': 2,            # pause time before starting first stimulus
    'continueKey': 't',        # key from scanner that says scan is starting
    'responseKeys': ['space', 'backspace'],           # keys to be used for responses (mapped to 1,2,3,4)
    'respAdvances': True,     # will a response end the stimulus?
    'skipPrompts': False,     # go right to the scanner-wait page
    'promptDir': '/pilot/prompts/',  # directory containing prompts and questions files
    'fullScreen': False,       # run in full screen mode?
    'screenToShow': 1,        # display on primary screen (0) or secondary (1)?
    'initialScreenColor':[0.0, 0.0, 1.0],
    'hues': [0.0, 120.0, 240.0],
    'saturations': [.5, 1.0],
    'values': [1.0],
    'white': [0.0, 0.0, 1.0],
    'textColor': [0.0, 0.0, 0.0],
    'nbackBlockTime': 10,
    'arithmeticBlockTime': 10,
    'resolution': [1440, 900],
    'colorSpace': 'hsv',
    'units': 'norm',
    'path': libs.path, # FIXME: get path of file not cwd
    'blockTimes': {
        # 'nback': 5.0 * 60, #in seconds, 5 min
        'nback': 10, #for testing
        # 'arithmetic': 5.0 * 60,
        'arithmetic': 20
    }
}




win, filters, msg, check, cross, fixation, clocks, stimuli, miniBlockOrder, experiment, participantNo = None, None, None, None, None, None, None, None, None, None, None

def twiceFlip():
    win.flip()
    win.flip()

def setupStimuli(stims = []):
    global stimuli
    stimuli = []
    for c in stims:
        stim = visual.TextStim(win, color=params['textColor'], colorSpace=params['colorSpace'],
        text=c.upper(), name=c+'-stimulus')
        stimuli.append(stim)
    print('Stimuli ✓')

def setupClocks():
    global clocks
    clocks = {
    'experiment': clock.Clock(),
    'block': clock.Clock(),
    'trial': clock.Clock()
    }
    print('Clocks ✓')

def readMessageFile(msg, args = []):
    with open(params['path'] + params['promptDir'] + msg.name +'.txt') as f:
        data = f.read().strip()
        if len(args) is not 0:
            data=data.format(*args)
        print('Read {}.txt'.format(msg.name))
    msg.setText(data)

def createMessage(str):
    return visual.TextStim(win, pos=[0,-.5], wrapWidth=1.5, color=params['textColor'], colorSpace=params['colorSpace'],
    alignHoriz='center', name=str)

def setupMessages():
    global msg
    msg = {
        'continue': createMessage('continue-message'),
        'welcome': createMessage('welcome-message'),
        'nback-instructions': createMessage('nback-instructions-message'),
        'arithmetic-instructions': createMessage('arithmetic-instructions-message'),
        'completion': createMessage('completion-message'),
    }
    readMessageFile(msg['continue'], [params['continueKey'].upper()])
    readMessageFile(msg['welcome'], [5, params['continueKey'].upper()])
    readMessageFile(msg['nback-instructions'])
    readMessageFile(msg['arithmetic-instructions'])
    print('Messages ✓')

def setupFixation():
    global fixation
    fixation = visual.ShapeStim(win, lineWidth= 10, lineColor=[0, 0, 0],lineColorSpace='rgb255', vertices=((-.1, 0), (.1, 0), (0, 0), (0, .1), (0, -.1)), closeShape=False, name='fixation');
    print('Fixation ✓')

def setupCheckCross():
    global check
    global cross
    check = visual.ShapeStim(win, lineWidth= 10, lineColor=[0, 0, 0],lineColorSpace='rgb255', vertices=((-.1, 0), (.1, 0), (0, 0), (0, .1), (0, -.1)), closeShape=False, name='check');
    check = visual.ShapeStim(win, lineWidth= 10, lineColor=[0, 0, 0],lineColorSpace='rgb255', vertices=((-.1, 0), (.1, 0), (0, 0), (0, .1), (0, -.1)), closeShape=False, name='check');
    print('Check and cross ✓')

def setupWindow():
    global win
    win = visual.Window(params['resolution'], fullscr=params['fullScreen'], allowGUI=True, units=params['units'], color=params['initialScreenColor'], colorSpace=params['colorSpace'])
    print('Window ✓')

def setupFilters():
    global filters
    filters = {
        'red': visual.Rect(win, width=3, height=3, fillColor=[255, 0, 0], fillColorSpace=params['colorSpace'])
    }

def loadNbackSetup():
    global params
    data = None
    with open(params['inputDir'] + params['nback']['inputDir'] + params['nback']['inputNo'] + '.json', mode = 'r') as f:
         data = json.load(f)
    params['nback']['sequence'] = data['sequence']
    params['nback']['correctResponses'] = data['responses']

def setupParameters():
    global params
    params['inputDir'] = params['path'] + 'pilot/input/'
    params['outputDir'] = params['path'] + 'pilot/output/'
    params['nBlocks'] = len(params['hues']) * len(params['saturations']) * len(params['values']) + 1
    params['nback'] = {}
    params['arithmetic'] = {}
    params['nback']['n'] = [None] * params['nBlocks']
    params['nback']['inputNo'] = '1'
    params['nback']['inputDir'] = 'nback/'
    params['nback']['ISI'] = [None] * params['nBlocks']
    params['nback']['stimDur'] = [None] * params['nBlocks']
    params['arithmetic']['ISI'] = [None] * params['nBlocks']
    params['arithmetic']['stimDur'] = [None] * params['nBlocks']
    params['arithmetic']['inputNo'] = '1'
    params['arithmetic']['inputDir'] = 'arithmetic/'

    for i in range(params['nBlocks']):
        params['nback']['n'][i] = 2
        params['nback']['ISI'][i] = .5
        params['nback']['stimDur'][i] = 2
        params['arithmetic']['ISI'][i] = 1.5
        params['arithmetic']['stimDur'][i] = 6

def setupExperiment():
    global experiment
    colors = []
    for h in params['hues']:
        for s in params['saturations']:
            for v in params['values']:
                c = [h, s, v]
                colors.append(c)

    colors.append(params['white'])
    nbackResponseTimes = [None] * params['nBlocks']
    nbackResponses = [None] * params['nBlocks']
    nbackStimShown = [0] * params['nBlocks']
    arithmeticResponseTimes = [None] * params['nBlocks']
    arithmeticResponses = [None] * params['nBlocks']
    arithmeticStimShown = [0] * params['nBlocks']


    for i in range(params['nBlocks']):
        nbackResponseTimes[i] = []
        arithmeticResponseTimes[i] = []
        nbackResponses[i] = []
        arithmeticResponses[i] = []

    experiment = {
        'nback': {
            'count': 0,
            'responseTimes': nbackResponseTimes,
            'responses': nbackResponses,
            'lastShown': 0,
            'stimShown': nbackStimShown
        },
        'arithmetic': {
            'count': 0,
            'responseTimes': arithmeticResponseTimes,
            'responses': arithmeticResponses,
            'lastShown': 0,
            'stimShown': arithmeticStimShown
        },
        'colors': colors,
    }

def randomize():
    global experiment
    experiment['firstArithmetic'] = random.random() < .5
    random.shuffle(experiment['colors'])

def init():
    setupWindow()
    setupFilters()
    setupFixation()
    setupCheckCross()
    setupMessages()
    setupClocks()
    setupParameters()
    setupExperiment()
    randomize()
    print('init complete ✓')
    # print experiment

def saveAfterBlock():
    pass
    # hue.init()

def showBeginningMessages():
    msg['welcome'].draw()
    win.flip()
    event.waitKeys(keyList=params['continueKey'])
    msg['continue'].draw()
    win.flip()
    event.waitKeys(keyList=params['continueKey'])

def nback(white = False):
    global experiment
    nbackCount = experiment['nback']['count']
    color = experiment['colors'][nbackCount]
    n = params['nback']['n'][nbackCount]
    ISI = params['nback']['ISI'][nbackCount]
    stimDur = params['nback']['stimDur'][nbackCount]
    blockDur = params['blockTimes']['nback']
    curStim = experiment['nback']['lastShown']
    stimShown = 0
    responses = []
    responseTimes = []
    win.color = color
    twiceFlip()
    print('Beginning miniblock nback {} with n: {}, stimDur: {}, ISI: {}, color: {}.'.format(nbackCount, n, stimDur, ISI, color))
    clocks['block'].reset()
    clocks['block'].add(blockDur)
    nbackStorage = []
    while(clocks['block'].getTime() < 0):
        # index = random.randint(0, len(stimuli) - 1)
        index = params['nback']['sequence'][curStim]
        stimuli[index].draw()
        keys = []
        while clocks['trial'].getTime()<0:
            pass
        clocks['trial'].reset()
        clocks['trial'].add(stimDur)
        win.flip()
        print(clocks['trial'].getTime())
        while clocks['trial'].getTime()<0 and len(keys) is 0:
            keys = event.getKeys(keyList=params['responseKeys'])
        responseTime = stimDur + clocks['trial'].getTime()
        clocks['trial'].reset()
        clocks['trial'].add(ISI)
        if len(keys) is 0: #did not respond
            responseTime = -1
            print('no response')
        else:
            resp = 0
            if str(keys[0][0]) is 's':
                resp = 1
            if resp is params['nback']['correctResponses'][str(n)][curStim]: #correct
                print('correct')
                # check.draw()
            else: #wrong
                print('wrong')
                # cross.draw()
        win.flip()
        responses.append(keys)
        responseTimes.append(responseTime)
        curStim += 1
        stimShown += 1
    experiment['nback']['lastShown'] = curStim #might be unneccesary as list is mallible
    experiment['nback']['stimShown'][nbackCount] = stimShown
    experiment['nback']['responseTimes'][nbackCount] = responseTimes
    experiment['nback']['responses'][nbackCount] = responses
    experiment['nback']['count'] += 1
    saveAfterBlock()


init()
loadNbackSetup()
#              0    1    2    3    4    5    6    7    8    9    10   11   12   13   14
setupStimuli(['A', 'B', 'C', 'D', 'E', 'H', 'I', 'K', 'L', 'M', 'O', 'P', 'R', 'S', 'T'])
showBeginningMessages()
clocks['experiment'].reset()
nback()
# hue.set_group(hue.make_command([255,255,255]))
pprint(experiment)
msg['continue'].draw()
win.flip()
event.waitKeys(keyList=params['continueKey'])


# # for frameN in range(100):#for exactly 100 frames
#     win.flip()

# s = sound.backend_pyo.SoundPyo('/Users/kaandonbekci/dev/pervasivetech/Room/pilot/110Hz_1.0osc.wav', loops=1)
# s.play()



# for i in range(65, 91):
#     c = chr(i)
#
#     print(chr(i))
