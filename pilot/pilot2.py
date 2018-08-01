import libs
import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")
from psychopy import visual, core, clock, logging

win = visual.Window()
# msg = visual.TextStim(win, text="Hola mundo!")


psycopyClock = clock.Clock()
monotonic = clock.MonotonicClock()
# msg.draw()
# win.flip()
clock.wait(.5)
psycopyClock.add(5)
while psycopyClock.getTime() < 0:
    pass
for i in range(10):
# print(clock.tick())
    core.wait(.5)
    # win.flip()
core.wait(2)
# win.close()
