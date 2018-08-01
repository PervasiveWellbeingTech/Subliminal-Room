import libs
import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")
from psychopy import visual, core, sound
import controller as hue

# s = sound.backend_pyo.SoundPyo('/Users/kaandonbekci/dev/pervasivetech/Room/pilot/110Hz_1.0osc.wav', loops=1)
# s.play()

#setup stimulus
win=visual.Window([1440, 900], fullscr=False, monitor='macbookpro')
gabor = visual.GratingStim(win, tex='sin', mask='gauss', sf=5,
    name='gabor', autoLog=False)
fixation = visual.GratingStim(win, tex=None, mask='gauss', sf=0, size=0.02,
    name='fixation', autoLog=False)

clock = core.Clock()
#let's draw a stimulus for 200 frames, drifting for frames 50:100
init = clock.getTime()


for frameN in range(300):#for exactly 200 frames
    if 10 <= frameN < 250:  # present fixation for a subset of frames
        fixation.draw()
    if 50 <= frameN < 150:  # present stim for a different subset
        gabor.setPhase(0.1, '+')  # increment by 10th of cycle
        gabor.draw()
    win.flip()
print clock.getTime() - init
