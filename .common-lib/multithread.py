import threading
import time
import random
# TYPES = {
# 'AUDIOTORY': 1,
# 'OLFACTORY': 2,
# 'TACTILE': 3,
# 'VISUAL': 4,
# 'MONITOR': 5
# }

class Intervention(threading.Thread):
    def __init__(self, type, no, func):
        threading.Thread.__init__(self)
        self.name = type+'_'+str(no)
        self.func = func
    def run(self):
        self.func(self)

# def getTime(thread):
#     print("Thread {} sleeps at {}".format(thread.name,
#         time.strftime("%H:%M:%S", time.gmtime())))
#     randSleepTime = random.randint(1, 5)
#     time.sleep(randSleepTime)
#     print("Thread {} wakes at {}".format(thread.name,
#         time.strftime("%H:%M:%S", time.gmtime())))

# def test():
#     thread1 = Intervention('AUDIOTORY', 1, getTime)
#     thread2 = Intervention('VISUAL', 1, getTime)
#     thread3 = Intervention('OLFACTORY', 1, getTime)
#     thread1.start()
#     thread2.start()
#     thread3.start()
# test()
