import threading
import time
import random
from collections import deque
# TYPES = {
# 'AUDIOTORY': 1,
# 'OLFACTORY': 2,
# 'TACTILE': 3,
# 'VISUAL': 4,
# 'MONITOR': 5
# }

class Intervention(threading.Thread):
    def __init__(self, type, no, funcs, delay = None, delayFunc = None):
        threading.Thread.__init__(self)
        self.name = type+'_'+str(no)
        self.funcs = deque()
        self.delay = delay
        [self.funcs.append(i) for i in funcs]
        # print(self.funcs)

    def run(self):
        next = self.funcs.popleft()
        while next is not None:
            next(self)
            self.funcs.append(next)
            next = self.funcs.popleft()
            if self.delay is not None:
                delayFunc(delay)

def getTime(thread):
    print("{} sleeps at {}".format(thread.name,
        time.strftime("%H:%M:%S", time.gmtime())))
    randSleepTime = random.randint(1, 5)
    time.sleep(2)
    print("{} wakes at {}".format(thread.name,
        time.strftime("%H:%M:%S", time.gmtime())))
def makeCoffee(thread):
    print("{} is making coffe at {}".format(thread.name,
        time.strftime("%H:%M:%S", time.gmtime())))
    randSleepTime = random.randint(1, 5)
    time.sleep(2)
    print("{} sips the coffe, yummy at {}".format(thread.name,
        time.strftime("%H:%M:%S", time.gmtime())))
def test():
    funcs = [getTime, makeCoffee]
    thread1 = Intervention('AUDIOTORY', 1, funcs)
    thread2 = Intervention('VISUAL', 1, funcs)
    thread3 = Intervention('OLFACTORY', 1, funcs)
    thread1.start()
    thread2.start()
    thread3.start()
test()
