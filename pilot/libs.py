import sys
import signal
import platform
import getpass
username = getpass.getuser()
print username
paths = {'Darwin': '/Users/kaandonbekci/dev/pervasivetech/Room/',
        'Windows': '',
        'Linux': '/home/kaan/dev/pervasivetech/Room/'}
operatingSys = platform.system()
path = paths[operatingSys]
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
    exit()
signal.signal(signal.SIGINT, signal_handler)
