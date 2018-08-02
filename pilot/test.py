from __future__ import division
import libs
import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")
from psychopy import visual, core, sound, logging, event
import controller as hue
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
    'initialScreenColor':(255,255,255), # in rgb255 space: (r,g,b) all between 0 and 255
    'resolution': [800, 800],
    'colorSpace': 'rgb255',
    'units': 'norm'
}

win, msg, fixation, clock, stimuli = None, None, None, None, None

def setupStimuli(*args):
    global stimuli
    global win
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
    global win
    fixation = visual.ShapeStim(win, lineWidth= 10, lineColor=[0, 0, 0],lineColorSpace='rgb255', vertices=((-.1, 0), (.1, 0), (0, 0), (0, .1), (0, -.1)), closeShape=False, name='fixCross');
    fixation.draw()

def setupWindow():
    global win
    win = visual.Window(params['resolution'], fullscr=params['fullScreen'], allowGUI=True, units=params['units'], color=params['initialScreenColor'], colorSpace=params['colorSpace'])

def init():
    setupWindow()
    setupFixation()
    setupMessages()
    setupClocks()
init()
msg['continue'].draw()
win.flip()
setupStimuli('a', 'b', 'c', 'd', 'e')

event.waitKeys(keyList=params['continueKey'])
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
