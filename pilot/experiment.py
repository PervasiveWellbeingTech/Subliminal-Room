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
import copy
import os
import json
import pprint as pp
import sys
pprint = pp.PrettyPrinter(indent=4).pprint

testing = False
outputDir = libs.path + 'pilot/output/' + ('test/' if testing else '')
ongoing, newExperiment = True, True

def unixTime():
    return clock.getAbsTime()

def twiceFlip():
    win.flip()
    win.flip()

def setupStimuli():
    global stimuli
    stimuli = []
    # for c in params['nback']['letters']:
    #     stim = visual.TextStim(win, color=params['textColor'], colorSpace=params['colorSpace'],
    #     text=c.upper(), name=c+'-stimulus')
    #     stimuli.append(stim)
    for c in range(len(params['nback']['letters'])):
        f = params['inputDir'] + params['nback']['inputDir'] + params['nback']['stimDir'] + str(c) + '.png'
        # f = params['inputDir'] + params['nback']['inputDir'] + params['nback']['stimDir'] +  'a.svg'
        stim = visual.ImageStim(win, f, name=params['nback']['letters'][c])
        stimuli.append(stim)
    print('Stimuli done.')

def setupClocks():
    global clocks
    clocks = {
    'experiment': clock.Clock(),
    'block': clock.Clock(),
    'trial': clock.Clock(),
    'pause': clock.Clock()
    }
    print('Clocks done.')

def readMessageFile(msg, args = []):
    with open(params['path'] + params['promptDir'] + msg.name +'.txt') as f:
        data = f.read().strip()
        if len(args) is not 0:
            data=data.format(*args)
        msg.setText(data)

def createMessage(str):
    return visual.TextStim(win, pos=[0, 0], wrapWidth=1.5, color=params['textColor'], colorSpace=params['colorSpace'],
    alignHoriz='center', name=str)

def setupMessages(): #better way to do this.
    global msg
    msg = {
        'continue': createMessage('continue-message'),
        'welcome': createMessage('welcome-message'),
        'nback-instructions': createMessage('nback-instructions-message'),
        'pause': createMessage('pause-message'),
        'arithmetic-instructions': createMessage('arithmetic-instructions-message'),
        'completion': createMessage('completion-message'),
        'nback-alert': createMessage('nback-alert-message'),
        'arithmetic-alert': createMessage('arithmetic-alert-message'),
        'stress-questionaire' : createMessage('stress-questionaire-message'),
        'valence-questionaire' : createMessage('valence-questionaire-message'),
        'concentration-questionaire' : createMessage('concentration-questionaire-message'),
    }
    readMessageFile(msg['continue'], [params['continueKey'].upper()])
    readMessageFile(msg['welcome'], [params['nback']['blockTime'] / 60, params['arithmetic']['blockTime'] / 60, params['pauseDur'], params['continueKey'].upper()])
    readMessageFile(msg['nback-instructions'], [params['nback']['n'], params['continueKey'].upper()])
    readMessageFile(msg['arithmetic-instructions'])
    readMessageFile(msg['pause'], [params['pauseDur']])
    readMessageFile(msg['nback-alert'])
    readMessageFile(msg['arithmetic-alert'])
    readMessageFile(msg['stress-questionaire'])
    readMessageFile(msg['valence-questionaire'])
    readMessageFile(msg['concentration-questionaire'])
    print('Messages done.')

def setupFixation():
    global fixation
    fixation = visual.ShapeStim(win, lineWidth= 10, lineColor=[0, 0, 0],lineColorSpace='rgb255', vertices=((-.1, 0), (.1, 0), (0, 0), (0, .1), (0, -.1)), closeShape=False, name='fixation');
    print('Fixation done.')

def setupRatingScale():
    global ratingScale
    ratingScale = visual.RatingScale(win, low=1, high=10, noMouse=True, markerStart=5.5, lineColor='black', stretch=2.0, labels=('1','2','3','4','5','6','7','8','9','10'), markerColor='black', scale=None, acceptPreText='')

def setupCheckCross():
    global check
    global cross
    check = visual.ShapeStim(win, lineWidth= 10, lineColor=[0, 0, 0], lineColorSpace='rgb255', vertices=((0.0, 0.0), (.1, -.1), (.3, .3)), closeShape=False, name='check')
    cross = visual.ShapeStim(win, lineWidth= 10, lineColor=[0, 0, 0], lineColorSpace='rgb255', vertices=((-.1, .1), (.1, -.1), (0.0, 0.0), (-.1, -.1), (.1, .1)), closeShape=False, name='cross')
    print('Check and cross done.')

def setupWindow():
    global win
    win = visual.Window(params['resolution'], fullscr=params['fullScreen'], screen=params['screenToShow'], units=params['units'], color=params['initialScreenColor'], colorSpace=params['colorSpace'])
    print('Window done.')

def setupFilters():
    global filters
    filters = {
        'red': visual.Rect(win, width=3, height=3, fillColor=[255, 0, 0], fillColorSpace=params['colorSpace'])
    }

def loadNbackSetup():
    global params
    data = None
    with open(params['inputDir'] + params['nback']['inputDir'] + params['nback']['setupDir'] + params['nback']['inputNo'] + '.json', mode = 'r') as f:
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
            'fullScreen': False,       # run in full screen mode?
            'hues': [0.0, 120.0, 240.0],
            'initialScreenColor':[0.0, 0.0, 1.0],
            'path': libs.path,
            'pauseDur': 5 if testing else 30,
            'promptDir': '/pilot/prompts/',  # directory containing prompts and questions files
            'resolution': [1920, 1080],
            'respAdvances': True,     # will a response end the stimulus?
            'responseKeys': ['space', 'backspace', 'q', 'r'],
            'saturations': [.5, 1.0],
            'screenToShow': 1,        # display on primary screen (0) or secondary (1)?
            'skipPrompts': False,     # go right to the scanner-wait page
            'textColor': [0.0, 0.0, 0.0],
            'units': 'norm',
            'values': [1.0],
            'white': [0.0, 0.0, 1.0],
            'taskMessageTime': 2,
            'practiceDur': 10 if testing else 1 * 60,
            'questionaireDur': 20 if testing else 1 * 60,
            'preQuestionaireDur': 2,

        }
        params['nBlocks'] = len(params['hues']) * len(params['saturations']) * len(params['values']) + 1
        params['outputDir'] = params['path'] + 'pilot/output/' + ('test/' if testing else '')
        params['arithmetic'] = {}
        params['arithmetic']['blockTime'] = 10 if testing else 5 * 60
        params['arithmetic']['firstStimDelay'] = 1
        params['arithmetic']['inputDir'] = 'arithmetic/'
        params['arithmetic']['inputNo'] = '1'
        params['arithmetic']['ISI'] = 1
        params['arithmetic']['stimDur'] = 5
        params['inputDir'] = params['path'] + 'pilot/input/'
        params['nback'] = {}
        params['nback']['blockTime'] = 10 if testing else 5 * 60
        params['nback']['firstStimDelay'] = 1
        params['nback']['inputDir'] = 'nback/'
        params['nback']['setupDir'] = 'JSON/'
        params['nback']['stimDir'] = 'letters/'
        params['nback']['inputNo'] = '1'
        params['nback']['ISI'] = .5
                #                        0    1    2    3    4    5    6    7    8    9    10   11   12   13   14
        # params['nback']['letters'] = ['A', 'B', 'C', 'D', 'E', 'H', 'I', 'K', 'L', 'M', 'O', 'P', 'R', 'S', 'T']
        params['nback']['n'] = 2
        params['nback']['stimDur'] = 2
        loadNbackSetup()
    else:
        print('load parameters')

def load(loadId):
    global params
    global experiment
    dir = outputDir + str(loadId) + '/'
    files = os.listdir(dir)
    files.sort()
    paramsFileLoc = dir + files.pop()
    experimentFileLoc = dir + files.pop()
    with open(paramsFileLoc) as paramsFile:
        params = json.load(paramsFile)['params']
    with open(experimentFileLoc) as experimentFile:
        experiment = json.load(experimentFile)['experiment']

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
        listNBlocks = [[]] * params['nBlocks']
        zeroNBlocks = [0] * params['nBlocks']
        questionaire = [None] * params['nBlocks']
        for i in range(params['nBlocks']):
            questionaire[i] = {
                'stress': -1,
                'valence': -1,
                'concentration': -1
            }
        experiment = {
            'saveCount': 0,
            'blockCount': 0,
            'nback': {
                'count': 0,
                'lastShown': 0,
                'responses': {
                    'corrected': copy.deepcopy(listNBlocks),
                    'raw': copy.deepcopy(listNBlocks)
                },
                'responseTimes': copy.deepcopy(listNBlocks),
                'stimShown': copy.deepcopy(zeroNBlocks),
                'questionaire': copy.deepcopy(questionaire)
            },
            'arithmetic': {
                'count': 0,
                'lastShown': 0,
                'rawResponses': copy.deepcopy(listNBlocks),
                'responseTimes': copy.deepcopy(listNBlocks),
                'stimShown': copy.deepcopy(zeroNBlocks),
                'questionaire': copy.deepcopy(questionaire)
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
    dir = params['outputDir'] + str(experiment['participantNo'])
    os.mkdir(dir)
    return dir + '/'

def getParticipantNo():
    cur = sum(os.path.isdir(os.path.join(params['outputDir'], i)) for i in os.listdir(params['outputDir'])) - (0 if testing else 1)
    if newExperiment:
        cur += 1
    return cur

def init():
    global testing
    loadId = None
    if len(sys.argv) > 1:
        sys.argv.reverse()
        sys.argv.pop()
        nextIsLoadFile = False
        while len(sys.argv) > 0:
            arg = sys.argv.pop()
            if nextIsLoadFile:
                loadId = arg
                nextIsLoadFile = False
            else:
                if arg  == 'test':
                    testing = True
                elif arg == 'load':
                    nextIsLoadFile = True
    print('Testing mode: {}'.format(testing))
    if loadId is not None:
        load(loadId)
    else:
        setupParameters()
        setupExperiment()
        saveParameters('init complete')
        saveExperiment('init complete')
    setupClocks()
    setupWindow()
    setupFixation()
    setupRatingScale()
    setupCheckCross()
    setupMessages()
    setupStimuli()
    print('init done.')

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

def wait(clock):
    while clock.getTime() < 0:
        pass
    return

def nbackPractice():
    global experiment
    curStim = experiment['nback']['lastShown']
    stimShown = 0
    # win.color = params['white']
    # twiceFlip()
    msg['nback-alert'].draw()
    clocks['trial'].reset()
    clocks['trial'].add(params['taskMessageTime'])
    win.flip()
    wait(clocks['trial'])
    clocks['block'].reset()
    clocks['block'].add(params['practiceDur'])
    clocks['trial'].reset()
    clocks['trial'].add(params['nback']['ISI'])
    win.flip()
    while clocks['block'].getTime() < 0:
        index = params['nback']['sequence'][curStim]
        stimuli[index].draw()
        keys = []
        wait(clocks['trial'])
        clocks['trial'].reset()
        clocks['trial'].add(params['nback']['stimDur'])
        win.flip()
        while clocks['trial'].getTime()<0 and len(keys) is 0:
            keys = event.getKeys(keyList=params['responseKeys'])
        responseTime = params['nback']['stimDur'] + clocks['trial'].getTime()
        clocks['trial'].reset()
        clocks['trial'].add(params['nback']['ISI'])
        resp = -1
        if len(keys) is 0: #did not respond
            responseTime = -1
        else:
            if str(keys[0][0]) is 'q':
                saveExperiment('nback aborted')
                exit()
            elif str(keys[0][0]) is 'r':
                return
            else:
                resp = 0
                if str(keys[0][0]) is 's':
                    resp = 1
                if resp is params['nback']['correctResponses'][str(params['nback']['n'])][curStim]: #correct
                    check.draw()
                else: #wrong
                    cross.draw()
        win.flip()
        curStim += 1
        stimShown += 1
    experiment['nback']['lastShown'] = curStim #might be unneccesary as list is mallible

def nback(practice = False):
    # FIXME: first n stim should not have correct rawResponses
    if practice:
        nbackPractice()
        return
    global experiment
    nbackCount = experiment['nback']['count']
    curStim = experiment['nback']['lastShown']
    stimShown = 0
    correct = 0
    wrong = 0
    rawResponses = []
    correctedResponses = []
    responseTimes = []
    win.color = experiment['colors'][nbackCount]
    twiceFlip()
    msg['nback-alert'].draw()
    clocks['trial'].reset()
    clocks['trial'].add(params['taskMessageTime'])
    win.flip()
    wait(clocks['trial'])
    clocks['block'].reset()
    clocks['block'].add(params['nback']['blockTime'])
    clocks['trial'].reset()
    clocks['trial'].add(params['nback']['ISI'])
    win.flip()
    while clocks['block'].getTime() < 0:
        index = params['nback']['sequence'][curStim]
        stimuli[index].draw()
        keys = []
        wait(clocks['trial'])
        clocks['trial'].reset()
        clocks['trial'].add(params['nback']['stimDur'])
        win.flip()
        while clocks['trial'].getTime()<0 and len(keys) is 0:
            keys = event.getKeys(keyList=params['responseKeys'])
        responseTime = params['nback']['stimDur'] + clocks['trial'].getTime()
        clocks['trial'].reset()
        clocks['trial'].add(params['nback']['ISI'])
        resp = -1
        corrected = -1
        if len(keys) is 0: #did not respond
            responseTime = -1
        else:
            if str(keys[0][0]) is 'q':
                saveExperiment('nback aborted')
                exit()
            else:
                resp = 0
                if str(keys[0][0]) is 's':
                    resp = 1
                if stimShown < params['nback']['n']:
                    if resp is 0:
                        check.draw()
                        corrected = 1
                        correct+=1
                    else:
                        cross.draw()
                        corrected = 0
                        wrong+=1
                elif resp is params['nback']['correctResponses'][str(params['nback']['n'])][curStim]: #correct
                    check.draw()
                    correct+=1
                    corrected = 1
                else: #wrong
                    cross.draw()
                    wrong+=1
                    corrected = 0
        win.flip()
        rawResponses.append(resp)
        correctedResponses.append(corrected)
        responseTimes.append(responseTime)
        curStim += 1
        stimShown += 1
    wait(clocks['trial'])
    clocks['trial'].reset()
    clocks['trial'].add(params['preQuestionaireDur'])
    win.flip()
    print("Correct ratio = {}%".format(correct/stimShown * 100))
    print("Wrong ratio = {}%".format(wrong/stimShown * 100))
    print("No response ratio = {}%".format((stimShown - correct - wrong)/stimShown * 100))
    wait(clocks['trial'])
    questionaire(nback=True)
    experiment['nback']['lastShown'] = curStim #might be unneccesary as list is mallible
    experiment['nback']['stimShown'][nbackCount] = stimShown
    experiment['nback']['responseTimes'][nbackCount] = responseTimes
    experiment['nback']['responses']['raw'][nbackCount] = rawResponses
    experiment['nback']['responses']['corrected'][nbackCount] = correctedResponses
    experiment['nback']['count'] += 1
    saveExperiment('nback completed')

def arithmetic(practice = False):
    if practice:
        arithmeticPractice()
        return
    pass

def arithmeticPractice():
    pass

def askRating(msg):
    while ratingScale.noResponse:
        msg.draw()
        ratingScale.draw()
        win.flip()
    rating = ratingScale.getRating()
    ratingScale.reset()
    return rating


def questionaire(nback):
    global experiment
    clocks['block'].reset()
    clocks['block'].add(params['questionaireDur'])
    answers = None
    if nback:
        answers = experiment['nback']['questionaire'][experiment['nback']['count']]
    else:
        answers = experiment['arithmetic']['questionaire'][experiment['arithmetic']['count']]
    answers['stress'] = askRating(msg['stress-questionaire'])
    answers['valence'] = askRating(msg['valence-questionaire'])
    answers['concentration'] = askRating(msg['concentration-questionaire'])

def practice():
    firstTask(practice = True)
    secondTask(practice = True)

def showBeginningMessages():
    msg['welcome'].draw()
    win.flip()
    event.waitKeys(keyList=params['continueKey'])
    msg['nback-instructions'].draw()
    win.flip()
    event.waitKeys(keyList=params['continueKey'])
    msg['continue'].draw()
    win.flip()
    event.waitKeys(keyList=params['continueKey'])

def pause(sec): #sliders for feedback
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

if __name__ == "__main__":
    init()
    showBeginningMessages()
    # practice()
    clocks['experiment'].reset()
    while ongoing:
        firstTask()
        secondTask()
        experiment['blockCount'] += 1
        pause(params['pauseDur'])
        if experiment['blockCount'] is params['nBlocks']:
            ongoing = False
    experiment['experimentDuration'] = clocks['experiment'].getTime()
    saveExperiment('end of experiment')
    msg['continue'].draw()
    win.flip()
    event.waitKeys(keyList=params['continueKey'])
