import sys
import signal
import platform
paths = {'Darwin': '/Users/kaandonbekci/dev/pervasivetech/Room/',
        'Windows': ''}
path = paths[platform.system()]
sys.path.insert(0, path+'visual/lib')
sys.path.insert(0, path+'audiotory/lib')
sys.path.insert(0, path+'tactile/lib')
sys.path.insert(0, path+'olfactory/lib')
sys.path.insert(0, path+'monitor/lib')
sys.path.insert(0, path+'.common-lib')
def signal_handler(sig, frame):
    print
    print('Exiting')
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)
