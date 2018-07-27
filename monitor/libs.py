import sys
import signal
sys.path.insert(0, '/Users/kaandonbekci/dev/pervasivetech/Room/visual/lib')
sys.path.insert(0, '/Users/kaandonbekci/dev/pervasivetech/Room/audiotory/lib')
sys.path.insert(0, '/Users/kaandonbekci/dev/pervasivetech/Room/tactile/lib')
sys.path.insert(0, '/Users/kaandonbekci/dev/pervasivetech/Room/olfactory/lib')
sys.path.insert(0, '/Users/kaandonbekci/dev/pervasivetech/Room/monitor/lib')
sys.path.insert(0, '/Users/kaandonbekci/dev/pervasivetech/Room/.common-lib')
def signal_handler(sig, frame):
    print
    print('Exiting')
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)
