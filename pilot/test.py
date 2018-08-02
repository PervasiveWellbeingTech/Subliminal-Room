from __future__ import division
import libs
import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")
from psychopy import visual, core, sound, logging, event
import controller as hue
import random
params = {
    # Declare stimulus and response parameters
    'nTrials': 3,            # number of trials in this session
    'stimDur': 1,             # time when stimulus is presented (in seconds)
    'ISI': 2,                 # time between when one stimulus disappears and the next appears (in seconds)
    'tStartup': 2,            # pause time before starting first stimulus
    'continueKey': 't',        # key from scanner that says scan is starting
    'respKeys': 'space',           # keys to be used for responses (mapped to 1,2,3,4)
    'respAdvances': True,     # will a response end the stimulus?
    'imageDir': 'Faces/',    # directory containing image stimluli
    'imageSuffix': '.jpg',   # images will be selected randomly (without replacement) from all files in imageDir that end in imageSuffix.
    # declare prompt and question files
    'skipPrompts': False,     # go right to the scanner-wait page
    'promptDir': 'Text/',  # directory containing prompts and questions files
    'promptFile': 'SamplePrompts.txt', # Name of text file containing prompts
    # declare display parameters
    'fullScreen': False,       # run in full screen mode?
    'screenToShow': 1,        # display on primary screen (0) or secondary (1)?
    'initialScreenColor':[255,255,255], # in rgb255 space: (r,g,b) all between 0 and 255
    'resolution': [1440, 900],
    'colorSpace': 'rgb255',
    'units': 'norm'
}

win, filters, msg, fixation, clock, stimuli = None, None, None, None, None, None


def twiceFlip():
    win.flip()
    win.flip()

def setupStimuli(*args):
    global stimuli
    stimuli = []
    for c in args:
        stim = visual.TextStim(win, color=[0, 0, 0], colorSpace=params['colorSpace'],
        text=c.upper(), name=c+'-stimulus')
        stimuli.append(stim)

def setupClocks():
    global clock
    clock = {
    'global': core.Clock(),
    'block': core.Clock()
    }

def setupMessages():
    global msg
    msg = {
        'continue': visual.TextStim(win, pos=[0,-.5], wrapWidth=1.5, color='#000000',
        alignHoriz='center', name='continue-message', text='Press "{}" to continue'
        .format(params['continueKey'].upper()))
    }

def setupFixation():
    global fixation
    fixation = visual.ShapeStim(win, lineWidth= 10, lineColor=[0, 0, 0],lineColorSpace='rgb255', vertices=((-.1, 0), (.1, 0), (0, 0), (0, .1), (0, -.1)), closeShape=False, name='fixCross');
    fixation.draw()

def setupWindow():
    global win
    win = visual.Window(params['resolution'], fullscr=params['fullScreen'], allowGUI=True, units=params['units'], color=params['initialScreenColor'], colorSpace=params['colorSpace'])

def setupFilters():
    global filters
    filters = {
        'red': visual.Rect(win, width=3, height=3, fillColor=[255, 0, 0], fillColorSpace=params['colorSpace'])
    }
def init():
    setupWindow()
    setupFilters()
    setupFixation()
    setupMessages()
    setupClocks()
    hue.init()


def v1():
    # filters['red'].draw()
    colors = [[255, 0, 0], [0, 255, 0], [0, 0, 255]]
    cmds = [hue.make_command(colors[0]), hue.make_command(colors[1]), hue.make_command(colors[2])]
    for j in range(len(colors)):

        win.color = colors[j]
        hue.set_group(cmds[j])
        twiceFlip()
        for i in range(5):
            # win.flip(False)
            clock['block'].add(2)
            index = random.randint(0, len(stimuli)-1)
            # filters['red'].draw()
            stimuli[index].draw()
            win.flip()
            while clock['block'].getTime()<0:
                pass
            win.flip()
            clock['block'].add(.500)
            while clock['block'].getTime()<0:
                pass

init()
setupStimuli('a', 'b', 'c', 'd', 'e')
msg['continue'].draw()
win.flip()
event.waitKeys(keyList=params['continueKey'])
v1()
win.color = [255, 255, 255]
twiceFlip()
hue.set_group(hue.make_command([255,255,255]))
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
