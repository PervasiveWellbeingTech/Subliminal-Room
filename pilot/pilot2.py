import libs
import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")
from psychopy import visual, core, clock, logging
from pygame import time as pgtime

# logging.console.setLevel(logging.CRITICAL)
# win = visual.Window()
# msg = visual.TextStim(win, text="Hola mundo!")


pygameClock = pgtime.Clock()
psycopyClock = clock.Clock()
monotonic = clock.MonotonicClock()
# msg.draw()
# win.flip()
clock.wait(.5)
pygameClock.tick()
psycopyClock.add(5)
while psycopyClock.getTime() < 0:
    pass
print(pygameClock.tick())
for i in range(10):
# print(clock.tick())
    core.wait(.5)
    print(pygameClock.tick())
    # win.flip()
    pygameClock.tick()
core.wait(2)
# win.close()
