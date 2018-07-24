import threading
# import time
# import random
from collections import deque

class Intervention(threading.Thread):
    def __init__(self, type, no, funcs, args, delay = None, delayFunc = None):
        if len(args) is not len(funcs):
            if len(args) + 1 is not len(funcs) or funcs[len(funcs)-1] is not None:
                print('{}_{} cannot be initiated, wrong number of funcs and params'.format(type, str(no)))
                return
        threading.Thread.__init__(self)
        self.name = type+'_'+str(no)
        self.funcs = deque()
        self.args = deque()
        self.delay = delay
        self.delayFunc = delayFunc
        # self.funcs = funcs
        # self.len = self.funcs(len)
        [self.funcs.append(i) for i in funcs]
        [self.funcs.append(i) for i in arg]
        # print(self.funcs)

    def run(self):
        index = 0
        next = self.funcs.popleft()
        while next is not None:
            params = self.args.popleft()
            next(*params)
            self.funcs.append(next)
            self.args.append(params)
            next = self.funcs.popleft()
            if self.delay is not None:
                delayFunc(delay)

# def getTime(thread):
#     print("{} sleeps at {}".format(thread.name,
#         time.strftime("%H:%M:%S", time.gmtime())))
#     randSleepTime = random.randint(1, 5)
#     time.sleep(randSleepTime)
#     print("{} wakes at {}".format(thread.name,
#         time.strftime("%H:%M:%S", time.gmtime())))
# def makeCoffee(thread):
#     print("{} is making coffe at {}".format(thread.name,
#         time.strftime("%H:%M:%S", time.gmtime())))
#     randSleepTime = random.randint(1, 5)
#     time.sleep(randSleepTime)
#     print("{} sips the coffe, yummy at {}".format(thread.name,
#         time.strftime("%H:%M:%S", time.gmtime())))
# def test():
#     funcs = [getTime, makeCoffee]
#     thread1 = Intervention('AUDIOTORY', 1, funcs)
#     thread2 = Intervention('VISUAL', 1, funcs)
#     thread3 = Intervention('OLFACTORY', 1, funcs)
#     thread1.start()
#     thread2.start()
#     thread3.start()
#     time.sleep(10)
#     thread1.funcs.appendleft(None)
#     thread2.funcs.appendleft(None)
#     thread3.funcs.appendleft(None)

# test()
