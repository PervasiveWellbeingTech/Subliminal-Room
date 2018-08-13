# -*- coding: utf-8 -*-
from __future__ import division
import libs
import warnings
import datetime
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")
from psychopy import visual, core, sound, logging, event, clock
import controller as hue
import random
import os
import json
import pprint as pp

pprint = pp.PrettyPrinter(indent=4).pprint
win, msg, check, cross, fixation, clocks, stimuli, experiment, params, firstTask, secondTask = None, None, None, None, None, None, None, None, None, None, None
ongoing, newExperiment = True, True

def twiceFlip():
    win.flip()
    win.flip()

def setupStimuli():
    global stimuli
    stimuli = []
    for c in params['nback']['letters']:
        stim = visual.TextStim(win, color=params['textColor'], colorSpace=params['colorSpace'],
        text=c.upper(), name=c+'-stimulus')
        stimuli.append(stim)
    print('Stimuli ✓')

def setupClocks():
    global clocks
    clocks = {
    'experiment': clock.Clock(),
    'block': clock.Clock(),
    'trial': clock.Clock(),
    'pause': clock.Clock()
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
        'pause': createMessage('pause-message'),
        'arithmetic-instructions': createMessage('arithmetic-instructions-message'),
        'completion': createMessage('completion-message'),
    }
    readMessageFile(msg['continue'], [params['continueKey'].upper()])
    readMessageFile(msg['welcome'], [params['nback']['blockTime'], params['arithmetic']['blockTime'], params['pauseDur'], params['continueKey'].upper()])
    readMessageFile(msg['nback-instructions'])
    readMessageFile(msg['arithmetic-instructions'])
    readMessageFile(msg['pause'], [params['pauseDur']])
    print('Messages ✓')

def setupFixation():
    global fixation
    fixation = visual.ShapeStim(win, lineWidth= 10, lineColor=[0, 0, 0],lineColorSpace='rgb255', vertices=((-.1, 0), (.1, 0), (0, 0), (0, .1), (0, -.1)), closeShape=False, name='fixation');
    print('Fixation ✓')

def setupCheckCross():
    global check
    global cross
    check = visual.ShapeStim(win, lineWidth= 10, lineColor=[0, 0, 0], lineColorSpace='rgb255', vertices=((0.0, 0.0), (.1, -.1), (.3, .3)), closeShape=False, name='check')
    cross = visual.ShapeStim(win, lineWidth= 10, lineColor=[0, 0, 0], lineColorSpace='rgb255', vertices=((-.1, .1), (.1, -.1), (0.0, 0.0), (-.1, -.1), (.1, .1)), closeShape=False, name='cross')
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
    params['nback']['letters'] = data['letters']

def loadArithmeticSetup():
    pass

def setupParameters():
    global params
    if newExperiment:
        params = {
            'colorSpace': 'hsv',
            'continueKey': 't',        # key from scanner that says scan is starting
            'fullScreen': True,       # run in full screen mode?
            'hues': [0.0, 120.0, 240.0],
            'initialScreenColor':[0.0, 0.0, 1.0],
            'path': libs.path, # FIXME: get path of file not cwd
            'pauseDur': 5,
            'promptDir': '/pilot/prompts/',  # directory containing prompts and questions files
            'resolution': [1440, 900],
            'respAdvances': True,     # will a response end the stimulus?
            'responseKeys': ['space', 'backspace', 'q', 'r'],
            'saturations': [.5, 1.0],
            'screenToShow': 1,        # display on primary screen (0) or secondary (1)?
            'skipPrompts': False,     # go right to the scanner-wait page
            'textColor': [0.0, 0.0, 0.0],
            'units': 'norm',
            'values': [1.0],
            'white': [0.0, 0.0, 1.0],
            # 'pauseDur': 30,
        }
        params['nBlocks'] = len(params['hues']) * len(params['saturations']) * len(params['values']) + 1
        params['outputDir'] = params['path'] + 'pilot/output/'

        # params['nback']['blockTime'] = 5 * 60
        params['arithmetic'] = {}
        params['arithmetic']['blockTime'] = 5 * 60
        params['arithmetic']['firstStimDelay'] = 2
        params['arithmetic']['inputDir'] = 'arithmetic/'
        params['arithmetic']['inputNo'] = '1'
        params['arithmetic']['ISI'] = [None] * params['nBlocks']
        params['arithmetic']['stimDur'] = [None] * params['nBlocks']
        params['inputDir'] = params['path'] + 'pilot/input/'
        params['nback'] = {}
        params['nback']['blockTime'] = 10
        params['nback']['firstStimDelay'] = 2
        params['nback']['inputDir'] = 'nback/'
        params['nback']['inputNo'] = '1'
        params['nback']['ISI'] = [None] * params['nBlocks']
                #              0    1    2    3    4    5    6    7    8    9    10   11   12   13   14
        # params['nback']['letters'] = ['A', 'B', 'C', 'D', 'E', 'H', 'I', 'K', 'L', 'M', 'O', 'P', 'R', 'S', 'T']
        params['nback']['n'] = [None] * params['nBlocks']
        params['nback']['stimDur'] = [None] * params['nBlocks']

        for i in range(params['nBlocks']):
            params['arithmetic']['ISI'][i] = 1.5
            params['arithmetic']['stimDur'][i] = 6
            params['nback']['ISI'][i] = .5
            params['nback']['n'][i] = 2
            params['nback']['stimDur'][i] = 2

        loadNbackSetup()
    else:
        print('load parameters')

def setupExperiment():
    global experiment
    if newExperiment:
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
            'saveCount': 0,
            'blockCount': 0,
            'nback': {
                'count': 0,
                'lastShown': 0,
                'responses': nbackResponses,
                'responseTimes': nbackResponseTimes,
                'stimShown': nbackStimShown
            },
            'arithmetic': {
                'count': 0,
                'lastShown': 0,
                'responses': arithmeticResponses,
                'responseTimes': arithmeticResponseTimes,
                'stimShown': arithmeticStimShown
            },
            'colors': colors,
            'participantNo': getParticipantNo(),
        }
        experiment['outputDir'] = createOutputDir()
        randomize()
    else:
        print('load experiment setup')

def randomize():
    global firstTask
    global secondTask
    global experiment
    experiment['firstArithmetic'] = random.random() < .5
    random.shuffle(experiment['colors'])
    (firstTask, secondTask) = (arithmetic, nback) if experiment['firstArithmetic'] else (nback, arithmetic)


def createOutputDir():
    dir = params['outputDir']+str(experiment['participantNo'])
    os.mkdir(dir)
    return dir + '/'

def getParticipantNo():
    cur = sum(os.path.isdir(os.path.join(params['outputDir'], i)) for i in os.listdir(params['outputDir']))
    if newExperiment:
        cur += 1
    return cur

def init():
    setupParameters()
    setupExperiment()
    setupClocks()
    setupWindow()
    setupFixation()
    setupCheckCross()
    setupMessages()
    setupStimuli()
    saveParameters('init complete')
    saveExperiment('init complete')
    print('init complete ✓')
    # print experiment

def saveParameters(note = None):
    saveFile = {}
    if note:
        saveFile['note'] = note
    saveFile['time'] = str(datetime.datetime.now())
    saveFile['params'] = params
    filename = experiment['outputDir']+'params.json'
    with open(filename, 'w') as f:
        json.dump(saveFile, f, indent=3)

def saveExperiment(note = None):
    global experiment
    saveFile = {}
    if note:
        saveFile['note'] = note
    saveFile['time'] = str(datetime.datetime.now())
    saveFile['experiment'] = experiment
    filename = '{}experiment_{}.json'.format(experiment['outputDir'], experiment['saveCount'])
    with open(filename, 'w') as f:
        json.dump(saveFile, f, indent=3)
    experiment['saveCount'] += 1

def showBeginningMessages():
    msg['welcome'].draw()
    win.flip()
    event.waitKeys(keyList=params['continueKey'])
    msg['continue'].draw()
    win.flip()
    event.waitKeys(keyList=params['continueKey'])

def wait(clock):
    while clock.getTime() < 0:
        pass
    return

def nbackPractice():
    global experiment
    curStim = experiment['nback']['lastShown']
    stimShown = 0
    win.color = params['white']
    twiceFlip()
    msg['nback'].draw()
    clocks['trial'].reset()
    clocks['trial'].add(params['taskMessageTime'])
    win.flip()
    wait(clocks['trial'])
    clocks['trial'].add(params['nback']['firstStimDelay'])
    win.flip()
    wait(clocks['trial'])
    clocks['block'].reset()
    clocks['block'].add(params['practiceDur'])
    clocks['trial'].reset()
    clocks['trial'].addTime(params['nback']['ISI'][0])
    while clocks['block'].getTime() < 0:
        index = params['nback']['sequence'][curStim]
        stimuli[index].draw()
        keys = []
        wait(clocks['trial'])
        clocks['trial'].reset()
        clocks['trial'].add(params['nback']['stimDur'][0])
        win.flip()
        while clocks['trial'].getTime()<0 and len(keys) is 0:
            keys = event.getKeys(keyList=params['responseKeys'])
        responseTime = params['nback']['stimDur'][0] + clocks['trial'].getTime()
        clocks['trial'].reset()
        clocks['trial'].add(params['nback']['ISI'][0])
        resp = -1
        if len(keys) is 0: #did not respond
            responseTime = -1
            print('no response')
        else:
            if str(keys[0][0]) is 'q':
                saveExperiment('nback aborted')
                exit()
            if str(keys[0][0]) is 'r':
                print('skipping')
                return
            resp = 0
            if str(keys[0][0]) is 's':
                resp = 1
            if resp is params['nback']['correctResponses'][str(n)][curStim]: #correct
                print('correct')
                check.draw()
            else: #wrong
                print('wrong')
                cross.draw()
        win.flip()
        curStim += 1
        stimShown += 1
    experiment['nback']['lastShown'] = curStim #might be unneccesary as list is mallible

def nback(practice = False): # FIXME: first n stim should not have correct responses
    if practice:
        nbackPractice()
        return
    global experiment
    nbackCount = experiment['nback']['count']
    curStim = experiment['nback']['lastShown']
    stimShown = 0
    responses = []
    responseTimes = []
    win.color = experiment['colors'][nbackCount]
    twiceFlip()
    msg['nback'].draw()
    clocks['trial'].reset()
    clocks['trial'].add(params['taskMessageTime'])
    win.flip()
    wait(clocks['trial'])
    clocks['trial'].add(params['nback']['firstStimDelay'])
    win.flip()
    wait(clocks['trial'])
    clocks['block'].reset()
    clocks['block'].add(params['nback']['blockTime'])
    clocks['trial'].reset()
    clocks['trial'].add(params['nback']['ISI'][nbackCount])
    while clocks['block'].getTime() < 0:
        index = params['nback']['sequence'][curStim]
        stimuli[index].draw()
        keys = []
        wait(clocks['trial'])
        clocks['trial'].reset()
        clocks['trial'].add(params['nback']['stimDur'][nbackCount])
        win.flip()
        while clocks['trial'].getTime()<0 and len(keys) is 0:
            keys = event.getKeys(keyList=params['responseKeys'])
        responseTime = params['nback']['stimDur'][nbackCount] + clocks['trial'].getTime()
        clocks['trial'].reset()
        clocks['trial'].add(params['nback']['ISI'][nbackCount])
        resp = -1
        if len(keys) is 0: #did not respond
            responseTime = -1
            print('no response')
        else:
            if str(keys[0][0]) is 'q':
                saveExperiment('nback aborted')
                exit()
            if str(keys[0][0]) is 'r':
                print('skipping')
                return
            resp = 0
            if str(keys[0][0]) is 's':
                resp = 1
            if resp is params['nback']['correctResponses'][str(n)][curStim]: #correct
                print('correct')
                check.draw()
            else: #wrong
                print('wrong')
                cross.draw()
        win.flip()
        responses.append(resp)
        responseTimes.append(responseTime)
        curStim += 1
        stimShown += 1
    experiment['nback']['lastShown'] = curStim #might be unneccesary as list is mallible
    experiment['nback']['stimShown'][nbackCount] = stimShown
    experiment['nback']['responseTimes'][nbackCount] = responseTimes
    experiment['nback']['responses'][nbackCount] = responses
    experiment['nback']['count'] += 1
    saveExperiment('nback completed')

def arithmetic(practice = False):
    if practice:
        arithmeticPractice()
        return
    pass

def arithmeticPractice():
    pass

def practice():

def pause(sec):
    win.color = params['white']
    twiceFlip()
    msg['pause'].draw()
    clocks['pause'].reset()
    clocks['pause'].add(sec)
    win.flip()
    while clocks['pause'].getTime() < 0:
        pass
    msg['continue'].draw()
    win.flip()
    event.waitKeys(keyList=params['continueKey'])

init()
showBeginningMessages()
practice()
clocks['experiment'].reset()
while ongoing:
    firstTask()
    secondTask()
    experiment['blockCount'] += 1
    # pprint(experiment)
    # pause(5)
    pause(params['pauseDur'])
    if experiment['blockCount'] is params['nBlocks']:
        ongoing = False
# pprint(experiment)
saveExperiment('end of experiment')
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
